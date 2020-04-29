import keyboard as kbo
import random
import time
from tkinter import StringVar, Button,Label,Entry,Tk,DoubleVar
from queue import Queue
import threading
from pynput import keyboard as kbi

#gui Root
root = Tk()
FileGUI=StringVar()
timeBetweenPresses=DoubleVar()
timeBetweenPresses.set(.3)
keys=StringVar()
keys.set("5555566676789")
row=0
keysLB=Label(root, text="Key Weights")

keyControlq=Queue()
current = set()

# The key combination to check
COMBINATIONS = [
    {kbi.Key.shift, kbi.KeyCode(char='r')},
    {kbi.Key.shift, kbi.KeyCode(char='R')}]

def selectRandomKey():
    kbo.press_and_release(random.choice(keys.get()))

def mainLoop():
    pressKey=False
    while 1:
        time.sleep(timeBetweenPresses.get())
        if pressKey:
            selectRandomKey()
        if not keyControlq.empty():
            print("Toggling Key Randomizer")
            pressKey=not pressKey
            with keyControlq.mutex:
                keyControlq.queue.clear()
def toggle():
    keyControlq.put("toggleKeyPressing")
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

mainKeyControl = threading.Thread(target=mainLoop)
mainKeyControl.start()
keylistener = threading.Thread(target=keyboardListener)
keylistener.start()
keysEntry = Entry(root,textvariable=keys)

keysLB.grid(row=row,column=0)
keysEntry.grid(row=row,column=1)
row+=1
startStop=Button(root,text="Start/Stop (ctrl=shift+r)",command=toggle)
startStop.grid(row=row,column=1)

root.mainloop()
listener.stop()


