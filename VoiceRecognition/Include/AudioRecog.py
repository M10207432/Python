import sys
import wave
import numpy as np
from pylab import *

from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav

def show_wave(path):
    spf=wave.open(path,'r')
    
    #Reads and returns at most n frames of audio, as a string of bytes.
    sound_info=spf.readframes(-1)
    sound_info=fromstring(sound_info,'int16')

    print sound_info,len(sound_info)

    #Returns sampling frequency
    f=spf.getframerate()

    '''=================
        Show Data
    ================='''
    subplot(211)
    plot(sound_info)
    title("Wave")

    subplot(212)
    spectrogram=specgram(sound_info, Fs=f, scale_by_freq=True, sides='default')
    print spectrogram

    show()
    spf.close()

def MCFF_Feature(path):
    (rate,sig) = wav.read(path)
    print rate,sig
    mfcc_feat = mfcc(sig,rate)
    fbank_feat = logfbank(sig,rate)

    print(fbank_feat[1:3,:])

def func():
    x=10
    def inn():
        print x
    inn()
    x=20
    return inn

def MFCC_Test():
    print "MFCC Testing"
    a=np.array([[1,2],[4,6]])
    b=np.array([[5,6],[9,1]])
    pad=np.concatenate((a,b))
    print pad
        
    c=np.tile([0,1],5)
    print c

    x=func()()
    
    
def main():
    '''
    path='./Raw_data/3.wav'
    MCFF_Feature(path)
    #show_wave(path)
    '''
    MFCC_Test()
    
if __name__=="__main__":
    main()
