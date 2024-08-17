import gamingfunctions as keeb
import pyaudio
import sys
import numpy as np
import aubio
import os
import time

def initializeAudio():
    # setup audio
    pyaudio_obj = pyaudio.PyAudio()
    buffer_size = 4096
    pyaudio_format = pyaudio.paFloat32
    n_channels = 1
    samplerate = 44100
    stream = PYAUDIOVAR.open(format=pyaudio_format,
                    channels=n_channels,
                    rate=samplerate,
                    input=True,
                    frames_per_buffer=buffer_size)
    outputsink = None
    record_duration = None

    # setup pitch
    tolerance = 0.8
    win_s = 4096 # fft size
    hop_s = buffer_size # hop size
    pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    return PYAUDIOVAR

def getPitch():
    audiobuffer = stream.read(buffer_size, exception_on_overflow=False)
    signal = np.fromstring(audiobuffer, dtype=np.float32)
    print("{} signal".format(signal))
    pitch = pitch_o(signal)[0]
    return pitch

def execute(pyaudio_obj):
    print("*** starting recording")
    while True:
        pitch = getPitch()
        while pitch is None:
            pitch = getPitch()
        letter = keeb.get_key(int(pitch))

        print("{} / {}".format(int(pitch),letter))

        
        if letter and pitch>=39 and pitch <=85:
            keeb.type_key(letter)

        if outputsink:
            outputsink(signal, len(signal))

        if record_duration:
            total_frames += len(signal)
            if record_duration * samplerate < total_frames:
                break

    print("*** done recording")
    stream.stop_stream()
    stream.close()
    pyaudio_obj.terminate()

if __name__ == '__main__':
    pyaudio_obj = initializeAudio()
    execute()