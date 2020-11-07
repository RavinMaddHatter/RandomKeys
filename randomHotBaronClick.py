from random import choice
from time import sleep
from win32api import keybd_event, GetAsyncKeyState
from win32con import KEYEVENTF_KEYUP
from tkinter import StringVar, Button,Label,Entry,Tk,DoubleVar, Toplevel,messagebox, ttk

from queue import Queue
from threading import Thread
from os import path
import json


root = Tk()
FileGUI=StringVar()
timeBetweenPresses=DoubleVar()
timeBetweenPresses.set(.01)
keys=StringVar()
selection=StringVar()
toggleHotKey=StringVar()
stopHotkey=StringVar()
print(path.exists("config.json"))
data={}
if path.exists("config.json"):
    with open("config.json") as f:
        data = json.load(f)
    
    
else:
    data={"default":"55555566667789"}
    keys.set("55555566667789")
settings={}
if path.exists("settings.json"):
    with open("settings.json") as f:
        settings = json.load(f)
    print(settings.keys())
else:
    settings={"toggleKey":'r',"stopKey":"="}




toggleHotKey.set(settings["toggleKey"])
toggleHotKey.trace("w", lambda *args: character_limit(toggleHotKey))

stopHotkey.set(settings["stopKey"])
stopHotkey.trace("w", lambda *args: character_limit(stopHotkey))
row=0
keysLB=Label(root, text="Key Weights")
timeLB=Label(root, text="Delay After Click")
nameLB=Label(root, text="Save Name")
selectLB=Label(root, text="Save Select")


ButtonMasherLB=Label(root, text="Delay After Click")
root.title("Madhatter's Button Masher")
current = set()
pressKey=False

def character_limit(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[-1])

class settingsMenu:
    def __init__(self,master,toggleStrVar,stopStrVar):
        self.top=Toplevel(master)
        self.top.protocol("WM_DELETE_WINDOW", self.cleanup)
        self.startingToggleKey=toggleStrVar.get()
        self.toggleHotKey=toggleStrVar
        self.startingEndKey=stopStrVar.get()
        self.stopHotkey=stopStrVar
        rt=0
        self.l=Label(self.top,text="stop Randomizer:").grid(row=rt,column=1)
        Entry(self.top,textvariable=self.stopHotkey,width=2,borderwidth=1).grid(row=rt,column=2)
        rt+=1
        Label(self.top,text="Toggle Randomizer (shift+):").grid(row=rt,column=1)
        Entry(self.top,textvariable=self.toggleHotKey,width=2,borderwidth=1).grid(row=rt,column=2)
    def sanitizeDataThenExit(self):
        keysValid=True
        toggleKeySetting=self.toggleHotKey.get().lower()
        if toggleKeySetting in list(VK_CODE.keys()):
            self.toggleHotKey.set(toggleKeySetting)
        else:
            keysValid=False
            self.toggleHotKey.set(self.startingToggleKey )
        stopKeySetting=self.stopHotkey.get().lower()
        if stopKeySetting in list(VK_CODE.keys()):
            self.stopHotkey.set(stopKeySetting)
        else:
            keysValid=False
            self.stopHotkey.set(self.startingEndKey)
        
        if not keysValid:
            messagebox.showerror("Key Selection Error", "The selected keys could not be used as hot keys. Not all settings were saved.")
        pass
    def cleanup(self):
        self.sanitizeDataThenExit()
        self.top.destroy()


class controller:
    def __init__(self,saveData):
        self.keyControlq=Queue()
        self.stopQueue=Queue()
        self.prevLeftClick=False
        self.prevRightClick=False
        self.startLiseners()

        self.options=list(saveData.keys())
        self.save_dict=saveData
        keys.set(data["default"])
        selection.set("default")
        
    def selectRandomKey(self):
        key=choice(keys.get())
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
        while self.stopQueue.empty():
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

        print("click listener stopped")
    def changeHotkeys(self):
        window=settingsMenu
        w=settingsMenu(root,toggleHotKey,stopHotkey)
        settingsButton["state"]="disabled"
        root.wait_window(w.top)
        settingsButton["state"]="normal"
    def hotkeyListener(self):
        depressed=False
        while self.stopQueue.empty():
            sleep(0.01)
            shift=GetAsyncKeyState(VK_CODE['shift'])
            ##toggleHotKey
            toogleKeyState=GetAsyncKeyState(VK_CODE[toggleHotKey.get()])
            keyCombo=shift and toogleKeyState
            stopKeyState=GetAsyncKeyState(VK_CODE[stopHotkey.get()])
            if stopKeyState:
                with self.keyControlq.mutex:
                    self.keyControlq.queue.clear()
                    timeEntry.config({"background": "White"})
            if  keyCombo:
                if not depressed:
                    print("hotkey Toggle")
                    self.toggle()
                    depressed=True
                    shift=GetAsyncKeyState(VK_CODE['shift'])
                    lastUsed=keys.get()
            
            elif depressed:
                depressed=False

        print("key listener stopped")
    def save(self):
        self.save_dict[selection.get()]=keys.get()
        with open("config.json", 'w') as json_file:
            json.dump(self.save_dict, json_file)
        settings={"toggleKey":toggleHotKey.get(),"stopKey":stopHotkey.get()}
        
        with open("settings.json", 'w') as json_file:
            json.dump(settings, json_file)
        saveMenu['values'] = tuple(self.save_dict.keys())
    def removeAll(self):
        saveMenu['menu'].delete(0,'end')
    def changeSave(self, value):
        value=selection.get()
        keys.set(self.save_dict[value])

    def delete(self):
        if selection.get()!="default":
            self.save_dict.pop(selection.get())
            selection.set("default")
            keys.set(self.save_dict["default"])
            selection.set("default")
            saveMenu['values'] = tuple(self.save_dict.keys())

            with open("config.json", 'w') as json_file:
                json.dump(self.save_dict, json_file)            
    def toggle(self):
        if self.keyControlq.empty():
            self.keyControlq.put("toggleKeyPressing")
            timeEntry.config({"background": "Green"})
        else:
            timeEntry.config({"background": "White"})
            with self.keyControlq.mutex:
                self.keyControlq.queue.clear()
    def close(self):
        self.stopQueue.put("stop")

ctr=controller(data)
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
           '=':0xBB,
           '`':0xC0,
           ';':0xBA,
           '[':0xDB,
           '\\':0xDC,
           ']':0xDD,
           "'":0xDE,
           '`':0xC0}


keysEntry = Entry(root,textvariable=keys)
timeEntry = Entry(root,textvariable=timeBetweenPresses)
startStop=Button(root,text="Start/Stop",command=ctr.toggle)
saveButton=Button(root,text="Save Settings",command=ctr.save)
settingsButton=Button(root,text="Change Hotkeys",command=ctr.changeHotkeys)

deleteButton=Button(root,text="delete Settings",command=ctr.delete)
saveMenu  = ttk.Combobox(root, width=27, textvariable = selection)
saveMenu.bind("<<ComboboxSelected>>",ctr.changeSave)
saveMenu['values'] = tuple(ctr.save_dict.keys())
selectLB.grid(row=row,column=0)
saveMenu.grid(row=row,column=1)

row+=1
keysLB.grid(row=row,column=0)
keysEntry.grid(row=row,column=1)
row+=1
timeLB.grid(row=row,column=0)
timeEntry.grid(row=row,column=1)
row+=1
deleteButton.grid(row=row,column=0)
saveButton.grid(row=row,column=1)
row+=1
startStop.grid(row=row,column=1)
settingsButton.grid(row=row,column=0)
root.mainloop()


ctr.close()
