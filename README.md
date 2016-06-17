![OnionLauncher Logo](logo.png)
# OnionLauncher

A launcher for Tor written in Python and PyQt5.

## Dependencies

 * Python (I usually work with 2, but did test with 3)
 * [Stem](https://stem.torproject.org/)
 * [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5)

## OnionLauncher vs. TorNova

While OnionLauncher is similar to a previous project I have done,
[TorNova](https://github.com/neelchauhan/TorNova), it is fundamentally
different in the following:

 * OnionLauncher uses Qt and PyQt5. TorNova uses GTK 3 and PyGObject.
  * The reason why I chose Qt instead of GTK is because GTK support on Windows
    and OS X (soon to be called macOS) is awful.
 * Both TorNova and OnionLauncher use Stem.
 * OnionLauncher lets users add arbitary options (anything in `torrc` is
   supported). TorNova only let users select options which are defined in the
   code.
 * TorNova has logfile and circuit viewing. OnionLauncher would require third
   party programs (like [arm](https://www.torproject.org/projects/arm.html.en)
   to get this functionality).
 * TorNova automatically saves preferences. OnionLauncher does not (at the
   current moment).
