from random import choice
from time import sleep
from win32api import keybd_event, GetAsyncKeyState
from win32con import KEYEVENTF_KEYUP
from tkinter import StringVar, Button,Label,Entry,Tk,DoubleVar
from queue import Queue
from threading import Thread


root = Tk()
FileGUI=StringVar()
timeBetweenPresses=DoubleVar()
timeBetweenPresses.set(.01)
keys=StringVar()
keys.set("55555566667789")
row=0
keysLB=Label(root, text="Key Weights")
timeLB=Label(root, text="Delay After Click")
ButtonMasherLB=Label(root, text="Delay After Click")
root.title("Madhatter's Button Masher")
current = set()
pressKey=False

class controller:
    def __init__(self):
        self.keyControlq=Queue()
        self.prevLeftClick=False
        self.prevRightClick=False
        self.startLiseners()
        
    def selectRandomKey(self):
        key=choice(keys.get())
        print(key)
        sleep(timeBetweenPresses.get())
        keybd_event(VK_CODE[key],0,0,0)
        sleep(0.01)
        keybd_event(VK_CODE[key],0 ,KEYEVENTF_KEYUP ,0)
    def startLiseners(self):
        self.hotkeys=Thread(target=self.hotkeyListener)
        self.hotkeys.start()
        
        self.click=Thread(target=self.clickListener)
        self.click.start()
        
    def clickListener(self):
        while True:
            sleep(0.01)
            if not self.keyControlq.empty():
                leftClickState=GetAsyncKeyState(VK_CODE["leftClick"])
                rightClickState=GetAsyncKeyState(VK_CODE["rightClick"])
                if self.prevRightClick and not rightClickState:
                    print("Right Click Released")
                    self.selectRandomKey()
                if self.prevLeftClick and not leftClickState:
                    print("Right Click Released")
                    self.selectRandomKey()
                self.prevLeftClick=leftClickState
                self.prevRightClick = rightClickState
    def hotkeyListener(self):
        depressed=False
        while True:
            sleep(0.01)
            shift=GetAsyncKeyState(VK_CODE['shift'])
            r=GetAsyncKeyState(VK_CODE['r'])
            keyCombo=shift and r
            if  keyCombo:
                if not depressed:
                    print("hotkey Toggle")
                    self.toggle()
                    depressed=True
                    shift=GetAsyncKeyState(VK_CODE['shift'])
            elif depressed:
                depressed=False
                
    def toggle(self):
        if self.keyControlq.empty():
            self.keyControlq.put("toggleKeyPressing")
            timeEntry.config({"background": "Green"})
        else:
            timeEntry.config({"background": "White"})
            with self.keyControlq.mutex:
                self.keyControlq.queue.clear()
    def close():
        self.hotkeys.stop()
        self.click.stop()

ctr=controller()
VK_CODE = {'leftClick':0x01,
           'rightClick':0x02,
            'backspace':0x08,
           'shift':0x10,
           '0':0x30,
           '1':0x31,
           '2':0x32,
           '3':0x33,
           '4':0x34,
           '5':0x35,
           '6':0x36,
           '7':0x37,
           '8':0x38,
           '9':0x39,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A,
           '+':0xBB,
           ',':0xBC,
           '-':0xBD,
           '.':0xBE,
           '/':0xBF,
           '`':0xC0,
           ';':0xBA,
           '[':0xDB,
           '\\':0xDC,
           ']':0xDD,
           "'":0xDE,
           '`':0xC0}


keysEntry = Entry(root,textvariable=keys)
timeEntry = Entry(root,textvariable=timeBetweenPresses)

keysLB.grid(row=row,column=0)
keysEntry.grid(row=row,column=1)
row+=1
timeLB.grid(row=row,column=0)
timeEntry.grid(row=row,column=1)
row+=1
startStop=Button(root,text="Start/Stop (shift+r)",command=ctr.toggle)
startStop.grid(row=row,column=1)

root.mainloop()


ctr.stop()




