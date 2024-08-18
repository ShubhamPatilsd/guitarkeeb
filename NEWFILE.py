import pyaudio
import sys
import numpy as np
import aubio
import csv
from pynput import keyboard 
from pynput import mouse 
import pyautogui
import time
import os

# Initialize the stuff relating to audio
p = pyaudio.PyAudio()
buffer_size = 4096
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 44100
stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)
outputsink = None
record_duration = None
tolerance = 0.8
win_s = 4096 # fft size
hop_s = buffer_size # hop size
pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)


# Initialize mappings
table = {}
with open("minecraft.csv", 'r') as data:
    for line in csv.DictReader(data):
        line = dict(line)
        table.update({line.get("pitch"):line.get("key")})
specialKeys = {"space":keyboard.Key.space, "enter":keyboard.Key.enter, "delete": keyboard.Key.delete}
mouseClick = {"leftclick": mouse.Button.left, "rightclick":mouse.Button.right}
mouseMove = {"mouseright": 88, "mouseleft":86, "mousedown":84,"mouseup":91}



# Declare methods

def getPitch():
    audiobuffer = stream.read(buffer_size, exception_on_overflow=False)
    signal = np.fromstring(audiobuffer, dtype=np.float32)
    print("{} signal".format(signal))
    pitch = pitch_o(signal)[0]
    return pitch

def convertPitchToCommand(pitch, table):
    return table.get(str(pitch)) or None;

def executeCommand(letter):
    letter = str(letter)
    keyboardControl = keyboard.Controller()
    mouseControl = mouse.Controller()
    
    if(letter in specialKeys.keys()):
        keyboardControl.press(specialKeys.get(letter))
        time.sleep(0.1)
        keyboardControl.release(specialKeys.get(letter))
        
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

    else:
        keyboardControl.press(letter)
        time.sleep(0.1)
        keyboardControl.release(letter)



# ------------------------------------------------------------------- #
while True:
    pitch = getPitch()
    if not pitch:
        continue
    else:
        command = convertPitchToCommand(int(pitch), table)
        if command and pitch>=39 and pitch <=85:
            executeCommand(command)

stream.stop_stream()
stream.close()
p.terminate()