# lovepd

This is a small example of a love2d-based GUI for a pd patch.

```sh
pd -nogui main.pd &
love .
```

The love program will wait for a connection before opening.

## note

Spawning an instamce of fluidsynth CLI or binding to libfluidsynth might work better:

- [sockets](https://fluid-dev.nongnu.narkive.com/ovSZ8tNW/how-to-send-manual-midi-commands-to-fluidsynth-from-another-program)
- [c program](https://forums.raspberrypi.com/viewtopic.php?t=235717)
- [pyhton-based bank manager](https://geekfunklabs.com/2020/06/10/headless-pi-synth/)
