#!/usr/bin/env python

from subprocess import check_output
import re
import pprint
from os import mkdir

pp = pprint.PrettyPrinter(indent=2)

plugins=[]

for plugfile in re.findall(r'(/.+):', check_output(["listplugins"]).decode('utf-8')):
  all_plugin_text = check_output(["analyseplugin", plugfile]).decode('utf-8')
  names = re.findall(r'Plugin Name: "(.+)"', all_plugin_text)
  labels = re.findall(r'Plugin Label: "(.+)"', all_plugin_text)
  ids = re.findall(r'Plugin Unique ID: (.+)', all_plugin_text)
  makers = re.findall(r'Maker: "(.+)"', all_plugin_text)
  copyrights = re.findall(r'Copyright: "(.+)"', all_plugin_text)
  ports = re.findall(r'(Ports:(\t.+\n)+)', all_plugin_text)
  for i in range(len(names)):
    plugin = {'name': names[i], 'label': labels[i], 'id': ids[i], 'maker': makers[i], 'copyright': copyrights[i], 'ports': [], 'file': plugfile}
    if (len(ports[i]) > 0):
      plugin['ports'] = {'audio':{'input':[], 'output':[]}, 'control':{'input':[], 'output':[]}}
      for portinfo in re.findall(r'"(.+)" (input|output), (control|audio)(.+)?', ports[i][0]):
        port = {'name': portinfo[0], 'range':[0, 0]}
        r = re.findall(r'([0-9.]+) to ([0-9.]+)', portinfo[3])
        if (len(r)):
          if (r[0][0] != '...'):
            port['range'][0] = float(r[0][0])
          else:
            port['range'][0] = -999
          if (r[0][1] != '...'):
            port['range'][1] = float(r[0][1])
          else:
            port['range'][1] = 999
        plugin['ports'][ portinfo[2] ][ portinfo[1] ].append(port)
    plugins.append(plugin)


pp.pprint(plugins)

try:
  mkdir('puredata')
except:
  pass

try:
  mkdir('puredata/ladspa')
except:
  pass

for plugin in plugins:
  controls=''
  guts = """
#N canvas 381 276 546 300 10;
#X obj -288 214 plugin~ %s;
#N canvas 3 26 450 300 controls 0;
#X obj -3 227 outlet;""" % (plugin['label'])
  cin_count=0
  cin_c_count=1
  c_count=1
  ain_count=0
  aout_count=0
  cout_count=0
  for interface in plugin['ports']['control']['input']:
    cin_count+=1
    crange = interface['range']
    if (len(crange) != 2):
      crange = [0,0]
    # if both zero, just set it to a "big" range
    if (crange[0] == 0 and crange[1] == 0):
      crange[0] = -999
      crange[1] = 999
    controls+= "#X obj 105 %d hsl 126 15 0 126 0 0 \$0/control/%d \$1/control/%d %s 0 8 0 10 -260097 -1 -1 0 1;\n" %((100+(cin_count*17)), cin_count, cin_count, interface['name'].replace(' ','_'))
    guts+= "#X obj %d 0 r \$0/control/%d;\n" % ((cin_count*130), cin_count)
    guts+= "#X obj %d 20 / 127;\n" % (cin_count*130)
    guts+= "#X obj %d 40 hid/notescale %f %f;\n" % ((cin_count*130), crange[0], crange[1])
    guts+= "#X msg %d 60 control #%d \$1;\n" % ((cin_count*130), cin_count)
    guts+= "#X connect %d 0 %d 0;\n" % (cin_c_count, cin_c_count+1)
    guts+= "#X connect %d 0 %d 0;\n" % (cin_c_count+1, cin_c_count+2)
    guts+= "#X connect %d 0 %d 0;\n" % (cin_c_count+2, cin_c_count+3)
    guts+= "#X connect %d 0 0 0;\n" % (cin_c_count+3)
    cin_c_count+=4
    c_count+=1

  for interface in plugin['ports']['audio']['input']:
    ain_count+=1
    c_count+=1
    controls+='#X obj %d 132 inlet~ %s;\n' % ((ain_count*100) - 350, interface['name'])
    controls+="#X connect %d 0 0 %d;\n" % (c_count, ain_count)

  for interface in plugin['ports']['audio']['output']:
    aout_count+=1
    c_count+=1
    controls+='#X obj %d 300 outlet~ %s;\n' % ((aout_count*100) - 350, interface['name'])
    controls+="#X connect 0 %d %d 0;\n" % (aout_count, c_count)

  for interface in plugin['ports']['control']['output']:
    cout_count+=1
    c_count+=1
    controls+='#X obj %d 250 outlet %s;\n' % ((cout_count*100) - 350, interface['name'])
    controls+="#X connect 0 1 %d 0;\n" % (c_count)

  f=open('puredata/ladspa/%s.pd' % plugin['label'],'w')
  f.write(guts + "\n#X restore -288 189 pd controls;\n" + controls + "\n#X connect 1 0 0 0;\n#X coords 0 -1 1 1 137 %d 1 100 100;\n" % (12+(cin_count*20)) )
  f.close()