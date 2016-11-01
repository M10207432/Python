import sys
import wave
from pylab import *

def show_wave(path):
    spf=wave.open(path,'r')
    sound_info=spf.readframes(-1)
    sound_info=fromstring(sound_info,'int16')

    f=spf.getframerate()

    subplot(211)
    plot(sound_info)
    title("Wave")

    subplot(212)
    spectrogram=specgram(sound_info, Fs=f, scale_by_freq=True, sides='default')

    show()
    spf.close()

def main():
    path='1.wav'
    show_wave(path)
        
if __name__=="__main__":
    main()
