from __future__ import print_function
import pygame
import time
import matplotlib
matplotlib.use('TkAgg')

import mido
from mido import Message
import tkinter
from tkinter import filedialog
from tkinter.messagebox import showinfo
from threading import Thread
import easygui
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.lines as mlines
from scipy.io import wavfile

pygame.mixer.init()

version = "1.2.0"

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
playTime = None
playTimeMillis = None
timeToolTip = None
window = None
a = None
f = None
canvas = None
curve = None
ti = 0
p = True
mainRunning = True
def exitProg():
    global window
    global mainRunning
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
            if(loaded):   
                unload()
            mainRunning = False
            window.destroy()
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
    global a
    global f
    global curve
    global p 
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
        
        samplingFrequency, signalData = wavfile.read(musicFile[0:len(musicFile)-4]+ ".wav")
        curve = tkinter.Frame(window, borderwidth = 1,width=40, height=20, bg="gray64", relief=tkinter.SUNKEN)
        
        f = Figure(figsize=(4, 3), dpi=100)
        a = f.add_subplot(211)
        a.plot(signalData)
        #a.set_title('Tk embedding')
        #a.set_xlabel('X axis label')
        #a.set_ylabel('Y label')
        curve.grid(row=20, column=10)
        
        #t = f.add_plot(signalData)
        
        portObj = mido.open_output(portname, autoreset=True)
        loaded = True
        p = True
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
        portObj = None
        pygame.mixer.music.unload() ## Will fail with old pygame version (needs pygame>=2.0.0dev6)
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

def updateTimeText():
    global playTime
    global playTimeMillis
    global ti
    global mainRunning

    pre = str(ti%1000)
    while(len(pre) < 3):
        pre = "0" + str(pre)
    formTime = "Time: " + time.strftime('%H:%M:%S:{}'.format(pre), time.gmtime(ti/1000.0))# + " (Milliseconds: " + str(ti) + ")"
    playTime["text"] = formTime
    playTimeMillis["text"] = "Milliseconds: " + str(ti)


def newline(p1, p2):
    ax = plt.gca()
    xmin, xmax = ax.get_xbound()

    if(p2[0] == p1[0]):
        xmin = xmax = p1[0]
        ymin, ymax = ax.get_ybound()
    else:
        ymax = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmax-p1[0])
        ymin = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmin-p1[0])

    l = mlines.Line2D([xmin,xmax], [ymin,ymax])
    ax.add_line(l)
    return l

def sendMidis(Mdict):
    
    global ti
    global portObj
    global mainRunning
    global p
    global points
    print("Started sendMidi function")
    
    while(mainRunning):
        if(p):
            print( " UPDATE: " + str(points))
            p = False
        ti = pygame.mixer.music.get_pos()
        #print(ti)
        tempTi = ti
        if( tempTi in points):
            print("Called update")
            #if(ti <= 1001 and ti >= 999): print("WARNING : " + str(ti))
            if(str(points[tempTi]).endswith(".0") == True):
                print("Note on")
                msg = Message('note_on', note=int(str(points[tempTi]).split(".")[0]), channel = 1, velocity = 60)
                print('Sending {}'.format(msg))
                portObj.send(msg)
            else:
                print("Note off")
                msg = Message('note_off', note=int(str(points[tempTi]).split(".")[0]), channel = 1)
                print('Sending {}'.format(msg))
                portObj.send(msg)
        #time.sleep(0.05)

## Will force usage of GUI since 1.0.6
guiEn = True
isOkay = True
    
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
    print("Building GUI")
    mFontB = ("Helvetica", 12, "bold")
    mFont= ("Helvetica", 12)
    window = tkinter.Tk()
    window.title("Time MIDI Sender")
    window.geometry('800x300')
    window["bg"] = "#1b1b1b"
    window.protocol("WM_DELETE_WINDOW", exitProg)
    menu = tkinter.Menu(window)
    window.config(menu=menu)
    file = tkinter.Menu(menu)
    file.add_command(label="Open", command=openConfig)
    file.add_command(label="Save", command=saveConfig)
    file.add_command(label="Load", command=load)
    file.add_command(label="Unload", command=unload)
    file.add_command(label="Exit", command=exitProg)
    
    opendFile = tkinter.Label(window, text = projectName, bg="#1b1b1b", fg="gray77", font=mFont)
    opendFile.grid(row=0, column=0)
    loadB = tkinter.Button(window, text="Load", command = load, bg="#1b1b1b", fg="gray99", font=mFont)
    loadB.grid(row=0, column = 1, padx=2)
    unloadB = tkinter.Button(window, text="Unload", command = unload, bg="#1b1b1b", fg="gray99", font=mFont)
    unloadB.grid(row=0, column = 2, padx=2)

    
    playControls = tkinter.Frame(window, borderwidth = 1,width=100, height=100, bg="#282828", relief=tkinter.SUNKEN)
    control = tkinter.Label(playControls, text = "Play control", bg="#282828", fg="gray99")
    control.grid(row=1, column = 2)
    
    timeFrame = tkinter.Frame(window, borderwidth = 1,width=40, height=50, bg="#282828", relief=tkinter.SUNKEN) ## timeframe, get it?
    
    playTime = tkinter.Label(timeFrame, text = "Time: 00:00:00.000", bg="#282828", fg="gray99", font=mFontB)   # Format HH:MM:SS.ms-
    playTime.grid(row=1, column = 1)
    playTimeMillis = tkinter.Label(timeFrame, text = "Milliseconds: 0", bg="#282828", fg="gray99", font=mFontB)
    playTimeMillis.grid(row=2, column = 1)
    
    timeFrame.grid(row=11, column = 4)
    
    play = tkinter.Button(playControls, text="Play", command = myPlay, bg="#282828", fg="gray99", font=mFont)
    play.grid(row=2, column = 1, padx = 2)
    pause = tkinter.Button(playControls, text="Pause", command = myPause, bg="#282828", fg="gray99", font=mFont)
    pause.grid(row=2, column = 2, padx = 2)
    stop = tkinter.Button(playControls, text="Stop", command = myStop, bg="#282828", fg="gray99", font=mFont)
    stop.grid(row=2, column = 3, padx = 2)
    playControls.grid(row=10, column=4)
    
    
    menu.add_cascade(label="File", menu=file)
    edit = tkinter.Menu(menu)
    #edit.add_command(label="Undo")
    menu.add_cascade(label="Edit", menu=edit)
    pbc = tkinter.Menu(menu)
    pbc.add_command(label="Play", command=myPlay)
    pbc.add_command(label="Pause", command=myPause)
    pbc.add_command(label="Stop", command=myStop)
    menu.add_cascade(label="Playback", menu=pbc)
    helpM = tkinter.Menu(menu)
    helpM.add_command(label="About", command=aboutPopup)
    menu.add_cascade(label="Help", menu=helpM)

    #curve = tkinter.Frame(window, borderwidth = 1,width=40, height=20, bg="#282828", relief=tkinter.SUNKEN)
    #curve.grid(row=20, column=10)
    window.update()

    
    window.update()




if(guiEn == False):
    try:
        with mido.open_output(portname, autoreset=True) as port:
            print(port)
            while True:
                #print("Time: " + str(pygame.mixer.music.get_pos()/1000) + " Seconds")
                    #print(" !!!!!!!!!!! " + str(str(points[pygame.mixer.music.get_pos()]).endswith(".0")))
                ti = pygame.mixer.music.get_pos()
                                
    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        exitProg()
        print(points)
else:
    t = Thread(target=sendMidis, args=(points,))
    t.setDaemon(True)
    t.start()
    mT = False
    while True:
        window.update()
        updateTimeText()
        window.update()
        #if(mT):
            #canvas._tkcanvas.pack_forget()
        if(loaded):
            
            ti = pygame.mixer.music.get_pos()
            a.set_xlim(ti,ti+60000)
            #canvas = None
            #canvas = FigureCanvasTkAgg(f, master=curve)
            #canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

            #canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
            window.update()
            mT = True
            window.update()
            #window.update()
            #canvas._tkcanvas.pack_forget()
            #if(evt != 0): print(evt)
            #if(playing):
                 #print("Stuff")
                #start_new_thread(updateTimeText,())
                #if( ti in points):
                #    if(str(points[ti]).endswith(".0") == True):
                #        print("Note on")
                #        msg = Message('note_on', note=int(str(points[ti]).split(".")[0]), channel = 1, velocity = 60)
                #        print('Sending {}'.format(msg))
                #        portObj.send(msg)
                #    else:
                #        print("Note off")
                #        msg = Message('note_off', note=int(str(points[ti]).split(".")[0]), channel = 1)
                #        print('Sending {}'.format(msg))
                #        portObj.send(msg)
