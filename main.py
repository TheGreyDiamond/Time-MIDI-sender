from __future__ import print_function
import pygame
import time
import mido
from mido import Message
import tkinter
from tkinter import filedialog
import easygui
pygame.mixer.init()

print("Welcome")
isOkay = False
configY = None
guiEn = False
#markerObj = None
notSaved = True
def exitProg():
    if(notSaved):
        ot = easygui.buttonbox('There are unsaved changes', 'Quit', ('Save', 'Cancle', 'Quit'))
        if(ot == "Save"):
            print("Saving whats that?")
        elif(ot == "Cancle"):
            print("Canceling")
        else:
            print("Quiting")
            exit()
    else:
        exit()

def openConfig():
    global portname
    global musicFile
    global markerFile
    path = filedialog.askopenfilename(initialdir = "/",title = "Select config file",filetypes = (("Config","*.conf"),("all files","*.*")))
    co = open(path, "r")
    confLines = co.readlines()
    co.close()
    confAtr = {}
    for c in confLines:
        if(not c.startswith("#")):
            c = c.replace("\n","")
            cp = c.split(":")
            confAtr[cp[0]] = cp[1]
    portname = confAtr["port"]
    musicFile = confAtr["music"]
    markerFile = confAtr["marker"]
    pygame.mixer.music.load(musicFile)    
    
def saveConfig():
    print("save conf")

while not isOkay:
    qu = input("Do you want to use GUI (Y/N) WARNING GUI IS UNSTABLE => ")
    if(qu == "Y"):
        isOkay = True
        guiEn = True
    else:
        print("Not using GUI.")
        isOkay = True
        guiEn = False
if(guiEn == False):  
    isOkay = False
    while not isOkay:
        conf = input("Do you want to load a config file (Y/N) => ")
        if(conf == "Y"):
            configF = input("Configfile name => ")
            try:
                co = open(configF, "r")
                confLines = co.readlines()
                co.close()
            except FileNotFoundError:
                print("Unable to load config file. Retry.")
            else:
                configY = True
                isOkay = True
        elif(conf == "N"):
            print("Okay, not loading a config file")
            configY = False
            isOkay = True
        else:
            print("Invalid answer")
    if(configY):
        confAtr = {}
        for c in confLines:
            if(not c.startswith("#")):
                c = c.replace("\n","")
                cp = c.split(":")
                confAtr[cp[0]] = cp[1]
        portname = confAtr["port"]
        musicFile = confAtr["music"]
        markerFile = confAtr["marker"]
        pygame.mixer.music.load(musicFile)
    else:
        portname = input("Port => ")
        
            
            #pygame.mixer.music.load(musicFile)
            
        #portname = "testLoopback 2"
        isOkay = False
        while not isOkay:
            try:
                musicFile = input("Music file=> ")
                pygame.mixer.music.load(musicFile)
                isOkay = True
            except pygame.error:
                print("Unable to open music file. Retry.")
                
        isOkay = False
        while not isOkay:
            try:
                markerFile = input("Marker file=> ")
                markerObj = open(markerFile, "r")
                markerObj.close()
                isOkay = True
            except FileNotFoundError:
                print("Unable to open marker file. Retry.")

else:
    print("Do GUI stuff here")
    window = tkinter.Tk()
    window.title("Time MIDI Sender")
    window.geometry('800x300')
    window["bg"] = "white"
    menu = tkinter.Menu(window)
    window.config(menu=menu)
    file = tkinter.Menu(menu)
    file.add_command(label="Open", command=openConfig)
    file.add_command(label="Save", command=saveConfig)
    file.add_command(label="Exit", command=exitProg)
    
    menu.add_cascade(label="File", menu=file)
    edit = tkinter.Menu(menu)
    #edit.add_command(label="Undo")
    menu.add_cascade(label="Edit", menu=edit)
    markerFile = "points.dat" ### JUST FOR DEBUG

markerObj = open(markerFile, "r")
raw = markerObj.readlines()
markerObj.close()
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
    pygame.mixer.music.stop()
    exitProg()
    print(points)
