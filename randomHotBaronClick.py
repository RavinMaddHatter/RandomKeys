import random
import time
import win32api
import win32con
from tkinter import StringVar, Button,Label,Entry,Tk,DoubleVar
from queue import Queue
from threading import Thread


root = Tk()
FileGUI=StringVar()
timeBetweenPresses=DoubleVar()
timeBetweenPresses.set(.1)
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
        key=random.choice(keys.get())
        print(key)
        time.sleep(timeBetweenPresses.get())
        win32api.keybd_event(VK_CODE[key],0,0,0)
        time.sleep(0.05)
        win32api.keybd_event(VK_CODE[key],0 ,win32con.KEYEVENTF_KEYUP ,0)
    def startLiseners(self):
        self.hotkeys=Thread(target=self.hotkeyListener)
        self.hotkeys.start()
        
        self.click=Thread(target=self.clickListener)
        self.click.start()
        
    def clickListener(self):
        while True:
            time.sleep(0.01)
            if not self.keyControlq.empty():
                leftClickState=win32api.GetAsyncKeyState(VK_CODE["leftClick"])
                rightClickState=win32api.GetAsyncKeyState(VK_CODE["rightClick"])
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
            time.sleep(0.01)
            keyCombo=win32api.GetAsyncKeyState(VK_CODE['shift']) and win32api.GetAsyncKeyState(VK_CODE['shift']) and win32api.GetAsyncKeyState(VK_CODE['r'])
            if  keyCombo:
                if not depressed:
                    print("hotkey Toggle")
                    self.toggle()
                    depressed=True
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

ctr=controller()
VK_CODE = {'leftClick':0x01,
           'rightClick':0x02,
            'backspace':0x08,
            'tab':0x09,
            'clear':0x0C,
           'enter':0x0D,
           'shift':0x10,
           'ctrl':0x11,
           'alt':0x12,
           'pause':0x13,
           'caps_lock':0x14,
           'esc':0x1B,
           'spacebar':0x20,
           'page_up':0x21,
           'page_down':0x22,
           'end':0x23,
           'home':0x24,
           'left_arrow':0x25,
           'up_arrow':0x26,
           'right_arrow':0x27,
           'down_arrow':0x28,
           'select':0x29,
           'print':0x2A,
           'execute':0x2B,
           'print_screen':0x2C,
           'ins':0x2D,
           'del':0x2E,
           'help':0x2F,
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
           'numpad_0':0x60,
           'numpad_1':0x61,
           'numpad_2':0x62,
           'numpad_3':0x63,
           'numpad_4':0x64,
           'numpad_5':0x65,
           'numpad_6':0x66,
           'numpad_7':0x67,
           'numpad_8':0x68,
           'numpad_9':0x69,
           'multiply_key':0x6A,
           'add_key':0x6B,
           'separator_key':0x6C,
           'subtract_key':0x6D,
           'decimal_key':0x6E,
           'divide_key':0x6F,
           'F1':0x70,
           'F2':0x71,
           'F3':0x72,
           'F4':0x73,
           'F5':0x74,
           'F6':0x75,
           'F7':0x76,
           'F8':0x77,
           'F9':0x78,
           'F10':0x79,
           'F11':0x7A,
           'F12':0x7B,
           'F13':0x7C,
           'F14':0x7D,
           'F15':0x7E,
           'F16':0x7F,
           'F17':0x80,
           'F18':0x81,
           'F19':0x82,
           'F20':0x83,
           'F21':0x84,
           'F22':0x85,
           'F23':0x86,
           'F24':0x87,
           'num_lock':0x90,
           'scroll_lock':0x91,
           'left_shift':0xA0,
           'right_shift ':0xA1,
           'left_control':0xA2,
           'right_control':0xA3,
           'left_menu':0xA4,
           'right_menu':0xA5,
           'browser_back':0xA6,
           'browser_forward':0xA7,
           'browser_refresh':0xA8,
           'browser_stop':0xA9,
           'browser_search':0xAA,
           'browser_favorites':0xAB,
           'browser_start_and_home':0xAC,
           'volume_mute':0xAD,
           'volume_Down':0xAE,
           'volume_up':0xAF,
           'next_track':0xB0,
           'previous_track':0xB1,
           'stop_media':0xB2,
           'play/pause_media':0xB3,
           'start_mail':0xB4,
           'select_media':0xB5,
           'start_application_1':0xB6,
           'start_application_2':0xB7,
           'attn_key':0xF6,
           'crsel_key':0xF7,
           'exsel_key':0xF8,
           'play_key':0xFA,
           'zoom_key':0xFB,
           'clear_key':0xFE,
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







