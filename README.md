# Time MIDI sender
Sends MIDI notes according to a file. Made for use with DasLight


## Setup in DasLight
First open dasLight and setup MIDI in the settings.
Then right click on the scene you want to time trigger and select Shortcut>Edit midi-mapping

![Here is an image][img1]

A popup will appear. Select the options like shown in the image below.

![Here is an image][img2]

Then edit your points.dat (you can rename it). The syntax is easy: `time:yourNr.0/5` So `time` is the time in milliseconds counted from song start. yourNr is the "Amount" (or Anzahl in german). If you want to turn a scene on use `yourNr.0`, if you want to turn it off use `yourNr.5`. You can comment your code with #. When using #, you should be aware that `1500:60.5 # Test` will fail. Example file:
```
# Valid comment
1500:60.0
2500:60.5  # Invalid comment
```
This file will start the scene "60" and turn it off after one second.

## How to use config files
There are three atributes in a config file. The file should end with `*.conf`. All files(config, marker and music) **need** to be in the same folder. The folder needs to have the same name as the config and the makerfile (excpet for the fileending) Example file (when the file is called `myProject.conf`):
```
port:testLoopback 3
music:Eyes_of_Glory.mp3
marker:myProject.dat
```
`music` is your music file. `port` is your digital MIDI port. `marker` is your marker file.

## How to use the GUI
![The main GUI][main]

To start playing a project click File>Open and select you config file. Then click on load, to load the project. Now you can use the Play, Pause and Stop button to control playback.

## Features
Already avaible:
- Sending midi notes
- Configfiles
- Pause/Play
- Loading/Unloading projects

WIP:
- GUI

Not yet avaiable:
- "Live" Marker editing
- Update checker
- Command line arguments

### Branches
There is a main branch, the main branch is kinda stable, it's called `master`. There is an unstable development branch, called `dev`.

[img1]: https://github.com/TheGreyDiamond/Time-MIDI-sender/blob/master/screenshots/dasLightselection.png?raw=truee "MiDi trigger"
[img2]: https://github.com/TheGreyDiamond/Time-MIDI-sender/blob/master/screenshots/dasLightMidi2.png?raw=true "MiDi trigger"
[main]: https://github.com/TheGreyDiamond/Time-MIDI-sender/blob/master/screenshots/Time-midi-sender-main.png?raw=true "Main window"
