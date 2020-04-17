import matplotlib
import pygame
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.io import wavfile
import time

samplingFrequency, signalData = wavfile.read('Eyes_of_Glory.wav')

pygame.mixer.init()

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk


def destroy(e):
    sys.exit()

root = Tk.Tk()
root.wm_title("Embedding in TK")


f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(211)
a.plot(signalData)
a.set_title('Tk embedding')
a.set_xlabel('X axis label')
a.set_ylabel('Y label')
#t = f.add_plot(signalData)

print(type(a))


button = Tk.Button(master=root, text='Quit', command=sys.exit)
button.pack(side=Tk.BOTTOM)
pygame.mixer.music.load("Eyes_of_Glory.wav")
asd
pygame.mixer.music.play()

while True:

    ti = pygame.mixer.music.get_pos()
    a.set_xlim(ti,ti+60000)


    # a tk.DrawingArea
    canvas = None
    canvas = FigureCanvasTkAgg(f, master=root)
    #canvas.show()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
    root.update()
    canvas._tkcanvas.pack_forget()
    time.sleep(0.1)
#Tk.mainloop()
