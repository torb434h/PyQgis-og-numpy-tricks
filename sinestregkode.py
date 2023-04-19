# -*- coding: utf-8 -*-

import numpy as np
import struct
import wave


Fs = 44100
sample = 44100
volume = 50

BPM = 140

nullBitFreq = 440
trueFreq = 220
falseFreq = 110
besked = 'her er en tekststreng'
title = 'lydfil.wav¨'


y = [0]

def toBinary(a):
    """Den her funktion laver en tekstreng om til et boolean array, altså true false, ud fra ASCII tabellen"""
    l, m = [], []
    for i in a:
        l.append(ord(i))
        for i in l:
            m.append(int(bin(i)[2:]))
    m = list(''.join(map(str, m)))
    m = np.in1d(m, '1')  # numpy funktion
    return m




def createWaveArray(besked):
    """laver et numpy array vi kan arbejde med"""
    

    x = np.arange(sample * 60 / int(BPM) * len(besked)) # np.arange laver et numpy array der har længden af sample, dvs samples pr sekund gange 60 divideret med BPM gange antalet af binære værdier. Altså 7 beats pr bogstav
    y = x
    for i in range(len(besked)): # man kan ikke loope gennem et bolean arr, så den bliver wrappet i len()
        a = i*sample * 60 // BPM # værdi til at slice array med. for loopet kører arrayet igennem. Værd at bemærke den dobbelte //. Når man bruger[:] til at slice skal den være intigers, altså hele tal, i modsætning til floats, decimal tal
        b = a + sample * 60 // BPM
        if besked[i] == True:
            y[a:b] = volume * np.sin(2 * np.pi * trueFreq * x[a:b] // Fs)
            print(trueFreq,a,b)
        else:
            y[a:b] = volume * np.sin(2 * np.pi * falseFreq * x[a:b] // Fs)
            print(falseFreq,a,b)
    return y

def writeWaveFile(title,waveArray):
    """Skriver wave filen"""
    f = wave.open(title,'wb')
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sample)
    f.setcomptype('NONE','Not Compressed')
    for i in waveArray:
        #print(i)
        f.writeframesraw(struct.pack('b',int(i)))
    f.close()


# ide til interface:

# besked = input("hvad er din besked? :")

# BPM = input("hvor mange BPM? :")

# trueFreq = input("Hvad skal frekvensen være til 1? :")
# falseFreq = input("og til 0? :")
# title = input('hvad skal filen hedde?, husk at skrive .wav bagefter navnet:')
# print('super, jeg får en lille kineser til at lave en fil til dig')
a = toBinary(besked)
y = createWaveArray(a)
writeWaveFile(title,y)