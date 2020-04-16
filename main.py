from __future__ import print_function
import pygame
import time
import mido
from mido import Message
import tkinter
from tkinter import filedialog
from tkinter.messagebox import showinfo
import easygui
pygame.mixer.init()

version = "1.0.6"

print("Welcome")
isOkay = False
configY = None
guiEn = False
#markerObj = None
notSaved = True
loaded = False
portObj = None
playing = False
paused = False
projectName = "Project: ---"
opendFile = None
points = {}
def exitProg():
    if(notSaved):
        ot = easygui.buttonbox('There are unsaved changes', 'Quit', ('Save', 'Cancle', 'Quit'))
        if(ot == "Save"):
            saveConfig()

            # When saveing is done
            if(play == True or loaded == True):
                pygame.mixer.music.stop()
        elif(ot == "Cancle"):
            print("Canceling")
        else:
            print("Quiting")
            if(play == True or loaded == True):
                pygame.mixer.music.stop()
            exit()
    else:
        exit()

def openConfig():
    global portname
    global musicFile
    global markerFile
    global projectName
    global opendFile
    file = filedialog.askopenfilename(initialdir = "/",title = "Select config file",filetypes = (("Config","*.conf"),("all files","*.*")))
    print(file)
    co = open(file, "r")
    rawpath = file.split("/")
    projectName = "Project: " + str(rawpath[len(rawpath)-1])[0:len(str(rawpath[len(rawpath)-1]))-5]
    opendFile["text"] = "Project: " + str(rawpath[len(rawpath)-1])[0:len(str(rawpath[len(rawpath)-1]))-5]
    path = ""
    for p in rawpath:
        if(not p.endswith(".conf")):
           path += p + "/"
    print(path)
    confLines = co.readlines()
    co.close()
    confAtr = {}
    for c in confLines:
        if(not c.startswith("#")):
            c = c.replace("\n","")
            cp = c.split(":")
            confAtr[cp[0]] = cp[1]
    portname = confAtr["port"]
    rawmusicFile = confAtr["music"]
    musicFile = path + rawmusicFile
    rawmarkerFile = confAtr["marker"]
    markerFile = path + rawmarkerFile
     


def load():
    global musicFile
    global markerFile
    global portObj
    global portname
    global loaded
    global points
    if( not loaded):
        pygame.mixer.music.load(musicFile)
        markerObj = open(markerFile, "r")
        raw = markerObj.readlines()
        markerObj.close()
        points = {}
        for o in raw:       # convert to dict
            if(not o.startswith("#")):
                p = o.split(":")
                points[int(p[0])] = float(p[1])
        print(points)
        loaded = True
        portObj = mido.open_output(portname, autoreset=True)
    else:
        showinfo("Info", "Project is already loaded!")

def unload():
    global musicFile
    global markerFile
    global portObj
    global portname
    global loaded
    global paused
    if(loaded == True):
        musicFile = ""
        markerFile = ""
        portObj = None
        portname = ""
        pygame.mixer.music.unload()
        loaded = False
        paused = False
    else:
        showinfo("Info", "There is no loaded project")

def myPlay():
    global paused
    global playing
    playing = True
    if(not paused):
        pygame.mixer.music.play()
        print("playing")
    else:
        print("unpausing")
        pygame.mixer.music.unpause()
        paused = False

def myPause():
    global paused
    global playing
    playing = False
    print("Pasuing")
    pygame.mixer.music.pause()
    paused = True

def myStop():
    global playing
    playing = False
    pygame.mixer.music.stop()
    paused= False
def saveConfig():
    print("save conf")

def aboutPopup():
    message  = '''Thank you for using Time MIDI sender!\nUsing version: ''' + version + '''\nAuthors: TheGreydiamond(thgreydiamond.de)'''
    showinfo("About", message)

## Will force usage of GUI since 1.0.6
guiEn = True
    
#while not isOkay:
#    qu = input("Do you want to use GUI (Y/N) WARNING GUI IS UNSTABLE => ")
#    if(qu == "Y"):
#        isOkay = True
#        guiEn = True
#    else:
#        print("Not using GUI.")
#        isOkay = True
#        guiEn = False


        
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
    load()
    pygame.mixer.music.play()

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
    
    opendFile = tkinter.Label(window, text = projectName)
    opendFile.grid(row=0, column=0)
    loadB = tkinter.Button(window, text="Load", command = load)
    loadB.grid(row=2, column = 1, padx=2)
    unloadB = tkinter.Button(window, text="Unload", command = unload)
    unloadB.grid(row=2, column = 2, padx=2)

    playControls = tkinter.Frame(window, borderwidth = 1,width=100, height=100, bg="White", relief=tkinter.SUNKEN)
    control = tkinter.Label(playControls, text = "Play control")
    control.grid(row=1, column = 5)
    play = tkinter.Button(playControls, text="Play", command = myPlay)
    play.grid(row=2, column = 1, padx = 2)
    pause = tkinter.Button(playControls, text="Pause", command = myPause)
    pause.grid(row=2, column = 2, padx = 2)
    stop = tkinter.Button(playControls, text="Stop", command = myStop)
    stop.grid(row=2, column = 3, padx = 2)
    playControls.grid(row=10, column=0, rowspan=5, columnspan = 1)
    
    
    
    menu.add_cascade(label="File", menu=file)
    edit = tkinter.Menu(menu)
    #edit.add_command(label="Undo")
    menu.add_cascade(label="Edit", menu=edit)
    helpM = tkinter.Menu(menu)
    helpM.add_command(label="About", command=aboutPopup)
    menu.add_cascade(label="Help", menu=helpM)
    window.update()
    
    window.update()
    #markerFile = "points.dat" ### JUST FOR DEBUG




if(guiEn == False):
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
else:
    
    while True:
        window.update()
        if(loaded):
            #print(portObj)
            evt = pygame.mixer.music.get_endevent()
            if(evt != 0): print(evt)
            if(playing):
                ti = pygame.mixer.music.get_pos()
                if( ti in points):
                    if(str(points[ti]).endswith(".0") == True):
                        print("Note on")
                        msg = Message('note_on', note=int(str(points[ti]).split(".")[0]), channel = 1, velocity = 60)
                        print('Sending {}'.format(msg))
                        portObj.send(msg)
                    else:
                        print("Note off")
                        msg = Message('note_off', note=int(str(points[ti]).split(".")[0]), channel = 1)
                        print('Sending {}'.format(msg))
                        portObj.send(msg)
            #if(play):
            #    pygame.mixer.music.play()
            #else:
            #    pygame.mixer.music.pause()
