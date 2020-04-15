from __future__ import print_function
import pygame
import time
import mido

from mido import Message
pygame.mixer.init()
portname = "maOut 2"
temp = input("Music file=> ")
if(temp == "m"):
    pygame.mixer.music.load("Eyes_of_Glory.mp3")
else:
    pygame.mixer.music.load(temp)
temp2 = input("Marker file=> ")
if(temp2 == "m"):
    f = open("points.dat","r")
else:
    f = open(temp2, "r")

raw = f.readlines()
points = {}
for o in raw:       # convert to dict
    if(not o.startswith("#")):
        p = o.split(":")
        points[int(p[0])] = float(p[1])
print(points)
pygame.mixer.music.play()

try:
    with mido.open_output(portname, autoreset=True) as port:
        print(port)
        while True:
            #print("Time: " + str(pygame.mixer.music.get_pos()/1000) + " Seconds")
            
            

                #print(" !!!!!!!!!!! " + str(str(points[pygame.mixer.music.get_pos()]).endswith(".0")))
            ti = pygame.mixer.music.get_pos()
            if( ti in points):
                if(str(points[ti]).endswith(".0") == True):
                    print("Note on")
                    msg = Message('note_on', note=int(str(points[ti]).split(".")[0]), channel = 1, velocity = 60)
                    print('Sending {}'.format(msg))
                    port.send(msg)
                else:
                    print("Note off")
                    msg = Message('note_off', note=int(str(points[ti]).split(".")[0]), channel = 1)
                    print('Sending {}'.format(msg))
                    port.send(msg)

            
except KeyboardInterrupt:
    f.close()
    pygame.mixer.music.stop()
    print(points)
