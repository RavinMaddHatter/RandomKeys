import keyboard 
from pyautogui import keyDown, keyUp
from win32api import keybd_event, GetAsyncKeyState
import time
import json
import mouse
trackedKeys=["a","s","w","d","j","y","k","l",";","i","o","p","shift",0x01,0x02]
#trackedMouse=["left","right","middle"]
lockKey="alt"
unlockKey="esc"
import win32api
import threading
import queue

with open("keylockConfig.json") as file:
    data=json.load(file)
    trackedKeys=data["keyboard"]
    lockKey=data["lockKey"]
    unlockKey=data["unlockKey"]
    leftMouseProxy=data["leftMouseProxy"]
    rightMoseProxy=data["rightMoseProxy"]
    print(trackedKeys)
def keyboardRepress(keyEvent):
    
    print("keyup")
    
    keyboard.unhook_all()

    time.sleep(0.1)
    
    keyboard.on_release_key(lockKey, unlock)
    keyboard.on_press_key(unlockKey, unlock)
def keyboardMouseReleaseRight(keyEvent):
    print("keyup-right hold")
    
    keyboard.unhook_all()

    time.sleep(0.1)
    mouse.press(button='right')
    keyboard.on_release_key(lockKey, unlock)
    keyboard.on_press_key(unlockKey, unlock)

def keyboardMouseReleaseLeft(keyEvent):
    print("keyup-left hold")
    
    keyboard.unhook_all()

    time.sleep(0.1)
    mouse.press(button='left')
    keyboard.on_release_key(lockKey, unlock)
    keyboard.on_press_key(unlockKey, unlock)
    
def keyLock(keyEvent):
    print(keyEvent.name)
    keys=[]
    buttons=[]
    for key in trackedKeys:
        if keyboard.is_pressed(key):
            keyboard.on_release_key(key, keyboardRepress)
            print("holding {}".format(key))
    if keyboard.is_pressed(leftMouseProxy):
        keyboard.on_release_key(leftMouseProxy, keyboardMouseReleaseLeft)
        pass
    if keyboard.is_pressed(rightMoseProxy):
        keyboard.on_release_key(rightMoseProxy, keyboardMouseReleaseRight)
        pass
    
def unlock(keyEvent):
    print("unlock")
    keyboard.unhook_all()
    for key in trackedKeys:
        keyboard.release(key)
    mouse.release(button='right')
    mouse.release(button='left')
    keyboard.on_release_key(lockKey, keyLock)
    


keyboard.on_release_key(lockKey, keyLock)
keyboard.on_press_key(unlockKey, unlock)



keyboard.wait()



