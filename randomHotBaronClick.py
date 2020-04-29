import keyboard as kbo
import random
import time
from tkinter import StringVar, Button,Label,Entry,Tk,DoubleVar
from queue import Queue
import threading
from pynput import keyboard as kbi

from pynput.mouse import Listener

root = Tk()
FileGUI=StringVar()
timeBetweenPresses=DoubleVar()
timeBetweenPresses.set(.1)
keys=StringVar()
masher=StringVar()
masher.set("Off")
keys.set("444444555566789")
row=0
keysLB=Label(root, text="Key Weights")
timeLB=Label(root, text="Delay After Click")
ButtonMasherLB=Label(root, text="Delay After Click")
root.title("Madhatter's Button Masher")

keyControlq=Queue()
current = set()
pressKey=False


COMBINATIONS = [
    {kbi.Key.shift, kbi.KeyCode(char='r')},
    {kbi.Key.shift, kbi.KeyCode(char='R')}]

def selectRandomKey():
    key=random.choice(keys.get())
    kbo.press_and_release(key)

def on_click(x, y, button, pressed):
    if not pressed:
        print("click")
        print(not keyControlq.empty())
        if not keyControlq.empty():
            selectRandomKey()

def toggle():
    if keyControlq.empty():
        masher.set("On")
        keyControlq.put("toggleKeyPressing")
    else:
        masher.set("Off")
        with keyControlq.mutex:
            keyControlq.queue.clear()
def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            toggle()
def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        if key in current:
            current.remove(key)

def keyboardListener():
    with kbi.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
def mouseListener():
    with Listener(on_click=on_click) as listener:
        listener.join()

mouseControl = threading.Thread(target=mouseListener)
mouseControl.start()

keylistener = threading.Thread(target=keyboardListener)
keylistener.start()
keysEntry = Entry(root,textvariable=keys)
timeEntry = Entry(root,textvariable=timeBetweenPresses)

keysLB.grid(row=row,column=0)
keysEntry.grid(row=row,column=1)
row+=1
timeLB.grid(row=row,column=0)
timeEntry.grid(row=row,column=1)
row+=1
startStop=Button(root,text="Start/Stop (shift+r)",command=toggle)
startStop.grid(row=row,column=1)

root.mainloop()




listener.stop()


