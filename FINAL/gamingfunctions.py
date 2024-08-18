import csv
from pynput.keyboard import Key, Controller
from pynput import mouse 
import pyautogui
import time
import os

specialKeys = {"space":Key.space, "enter":Key.enter, "delete": Key.delete}
mouseClick = {"leftclick": mouse.Button.left, "rightclick":mouse.Button.right}
mouseMove = {"mouseright": 88, "mouseleft":86, "mousedown":84,"mouseup":91}
             
            #   "mouseup":28, "mousedown":40}
# gameKeys = ['w', 'a', 's', 'd']

def key_pitch_tuning():
    pitchToKey ={}

    with open("minecraft.csv", 'r') as data:
        for line in csv.DictReader(data):

            line = dict(line)
            pitchToKey.update({line.get("pitch"):line.get("key")})

    return pitchToKey

def get_key(pitch):
    pitchToKey = key_pitch_tuning()

    return pitchToKey.get(str(pitch)) or None;
    
def type_key(letter):

    letter = str(letter)
    keyboard = Controller()

    mouseControl = mouse.Controller()
    
    if(letter in specialKeys.keys()):
        keyboard.press(specialKeys.get(letter))
        time.sleep(0.1)
        keyboard.release(specialKeys.get(letter))
        
    elif(letter in mouseClick.keys()):
        mouseControl.press(mouseClick.get(letter))
        time.sleep(0.6)
        mouseControl.release(mouseClick.get(letter))
    
    elif(letter in mouseMove):
        
        print("move mouse")
        cmd=""" osascript -e '
            repeat 500 times
                tell application "System Events" to key code {} --right
            end repeat'
        """.format(mouseMove.get(letter))

        success = os.system(cmd)

        screenSize = pyautogui.size()

        mouseControl.position=(screenSize[0]/2,screenSize[1]/2)
        print("success", success)
        # keyboard.press("o")

        
        # time.sleep(2)

        # keyboard.release("o")

    else:
        keyboard.press(letter)
        time.sleep(0.1)
        keyboard.release(letter)

   