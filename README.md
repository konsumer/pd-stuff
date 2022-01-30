# pure-data patches

This is my small collection of puredata patches for general use. I use [purr-data](https://agraef.github.io/purr-data/) for easy setup/install, which you might need to get all the pd extensions. There is a `-help` patch for all of these. You can open this directly for an example, or later get a refresher on how to use it by adding the patch you want to your thing, then right-click and choosing "Help". You can also open demo.pd to check most of them out.

## scalegen

This is a little piano that lets you select a pool of notes, and it will fire them when you send it a trigger. You can use this to make nice random music in scales and things.

## banger

This is just a simple `metro` with bpm on it. It has all the stuff I end up re-creating all the time (step counter, time-conversion, etc.)

## indicator

This just indicates current step.

## numpat

A step-sequencer for a series of numbers


## trigpat

A step-sequencer for a series of bangs.


## wrap_ladspa.py

This is a little script to automate wrapping all your ladspa plugins with puredata patches, to make them easier to use. It will add a little GUI and in/outs for controls/audio. You will need `ladspa-sdk` installed, and should have `listplugiuns` in your path. If you run it, you should see a hige list. If not, you might need to do this first:

```
export LADSPA_PATH=/usr/lib/ladspa
```

I included my plugins, but you probably want to generate all the wrappers for yourself. Not all of them work, so you will probably have to tune them, but this should help you get started.

You can see demo_ladspa.pd to see what it looks like.