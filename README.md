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
[img1]: https://github.com/TheGreyDiamond/Time-MIDI-sender/blob/master/screenshots/dasLightselection.png?raw=truee "MiDi trigger"
[img2]: https://github.com/TheGreyDiamond/Time-MIDI-sender/blob/master/screenshots/dasLightMidi2.png?raw=true "MiDi trigger"
