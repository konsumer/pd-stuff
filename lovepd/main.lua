require("inputmap")
local socket = require('socket')
local instruments = require("general_midi")


local currentInstrument = 1
local lastNote = -1

local tcp = assert(socket.tcp())

tcp:connect("127.0.0.1", 13000)
tcp:settimeout(0)


function setInstrument(num)
  currentInstrument = tonumber(num)
  tcp:send("instrument "..num..";")
end

function round(num, numDecimalPlaces)
  local mult = 10^(numDecimalPlaces or 0)
  return math.floor(num * mult + 0.5) / mult
end

function input_pressed(button)
  if button == "up" and currentInstrument < 128 then
    setInstrument(currentInstrument + 1)
  end
  if button == "down" and currentInstrument > 1 then
    setInstrument(currentInstrument - 1)
  end
end

function input_released(button)
end

local notes = {
  "C",
  "C#",
  "D",
  "D#",
  "E",
  "F",
  "F#",
  "G",
  "G#",
  "A",
  "A#",
  "B"
}

function noteName(num)
  local octave = math.floor(num / 12)
  return notes[ (num % 12) + 1 ] .. octave
end

function noteFreq(num)
  return round(523.25 * (2^((num-60)/12)), 2)
end

function love.load()
  setInstrument(1)
  fontHuge = love.graphics.newFont(100)
  fontBig = love.graphics.newFont(20)
  fontNormal = love.graphics.newFont(10)
end

function love.update()
  local msg = tcp:receive()
  if msg then
    local cmd, p1, p2
    cmd, p1 = string.match(msg, '(%a+) (%d+);')
    if not cmd then
      cmd, p1, p2 = string.match(msg, '(%a+) (%d+) (%d+);')
    end

    if cmd == "instrument" then
      currentInstrument = tonumber(p1)
    end
    
    if cmd == "note" then
      if (p2 ~= '0') then
        lastNote = tonumber(p1)
      end
    end
  end
end

function love.draw()
  love.graphics.setFont(fontNormal)
  love.graphics.printf( instruments:category(currentInstrument) .. ": " .. currentInstrument, 0, 10, 320, "center")

  love.graphics.setFont(fontBig)
  love.graphics.printf(instruments[currentInstrument], 0, 28, 320, "center" )

  if lastNote ~= -1 then
    love.graphics.setFont(fontHuge)
    love.graphics.printf( noteName(lastNote), 0, 80, 320, "center")
    love.graphics.setFont(fontNormal)
    love.graphics.printf( noteFreq(lastNote) .. " Hz", 0, 200, 320, "center")
  end
end
