import csv
from pynput.keyboard import Key, Controller
from pynput import mouse 

specialKeys = {"space":Key.space, "enter":Key.enter, "delete": Key.delete}
mouseClick = {"leftclick": mouse.Button.left, "rightclick":mouse.Button.right}
mouseMove = {"mouseright": (20,0), "mouseleft":(-20, 0), "mouseup":(0, 20), "mousedown":(0,-20)}

def key_pitch_tuning():
    pitchToKey ={}

    with open("tuning.csv", 'r') as data:
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

    if(letter in specialKeys):
        keyboard.press(specialKeys.get(letter))
        keyboard.release(specialKeys.get(letter))
    elif(letter in mouseClick):
        mouseControl.press(mouseClick.get(letter))
        mouseControl.release(mouseClick.get(letter))

    elif(letter in mouseMove):
        mouseControl.move(mouseControl.get(letter)[0], mouseControl.get(letter)[1])
    else:
        keyboard.press(letter)
        keyboard.release(letter)