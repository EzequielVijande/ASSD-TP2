import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import random
from pathlib import Path

# Asume duracion total igual al largo de la envolvente
# Suma armonicos con su envolvente correspondiente
# Recibe dos arrays, con las frecuencias y su envolvente correspondiente en el mismo indice del arreglo.
# Recibe la frecuencia de sampleo. Recibe si se quiere desnormalizar la funcion.
# Devuelve una arreglo con la funcion final sintetisada
def additiveSynthesis(frequencies,envelope, fs, desnorm = True):
    signals = [] # arreglo con arreglos de cada senoidal de frecuencia armonica
    synthFunction = [] # arreglo final
    maxLength = 0
    normalizer = 0
    for i in range(0,len(envelope)): # busco envolvente mas larga
        if maxLength < len(envelope[i]):
            maxLength = len(envelope[i])
    for i in range(0,len(envelope)):
        if maxLength > len(envelope[i]):
            zeroArray = np.zeros(maxLength - len(envelope[i])) #
            envelope[i] = np.concatenate([envelope[i], zeroArray])
    t = len(envelope[0])/fs # duracion de la nota
    samples = np.arange(len(envelope[0])) / fs
    for i in range(0,len(frequencies)):
        auxSignal = np.sin(2*np.pi*frequencies[i]*samples) # creo señal
        auxSignal = np.multiply(auxSignal,envelope[i]) # aplico la envolvente
        normalizer = normalizer + np.amax(envelope[i]) # agrego amplitud maxima al coef de normalizacion
        signals.append(auxSignal)
    for i in range(0,len(signals[0])):
        auxValue = 0
        for j in range(0,len(signals)):
            auxValue = auxValue + signals[j][i]
        synthFunction.append(auxValue)
    synthFunction = [i*(1/normalizer) for i in synthFunction] # normalizo en (-1,1)
    if desnorm:
        synthFunction = [i*32767 for i in synthFunction] # desnormalizo a formato wav int16
        synthFunction = np.int16(synthFunction)
    return synthFunction

# Crea un wav con la info de un numpy array de formato int16
# Recibe el arreglo (synthFunction, el nombre del archivo wav (wavName) y la frecuencia de sampleo (fs)
def createWav(synthFunction, wavName, fs):
    wavfile.write(wavName, fs, synthFunction)
    return

# ta = Attack Time
# td = Decay Time
# s  = Sustain Level (0<s<1)
# tr = Release Time
# tt = Total Time (lo que deseo que dure la nota)
# fs = Sampling Frequency
def adsrEnvelope(ta,td,s,tr,tt,fs):
    envelope = []
    totalSamples = tt*fs # duracion de la nota
    t = np.arange(totalSamples) / fs
    if s<0 or s>1:
        print("error in s parameter")
        return envelope
    if ta+td+tr<tt:
        ts = tt - ta - td - tr
        i = 0
        if ta != 0:
            while t[i] <= ta:
                envelope.append(t[i]/ta)
                i += 1
        if td != 0:
            while t[i] <= ta+td:
                envelope.append(((s-1)/td)*(t[i]-ta)+1)
                i += 1
        while t[i] <= ta+td+ts:
            envelope.append(s)
            i += 1
        if tr != 0:
            while t[i] < tt and i<len(t)-1:
                envelope.append((s/tr)*(tt-t[i]))
                i += 1
    else:
        print("caso turbio")
    return envelope

def scaleEnvelope(envelope,k):
    scaledEnvelope = []
    scaledEnvelope = np.multiply(k,envelope)
    return scaledEnvelope

def adsrSynthGuitar(fo,tt):
    fs = 44100
    envelopes = []
    harmonics = 12
    guitarFrequencies = np.arange(fo,fo*harmonics+1,fo)
    guitarEnvelope = adsrEnvelope(0.07,0.038,0.6,2.7,tt,fs)
    maxAmplitude = -7
    relativeAmplitudes = [-7,-16,-16,-15,-18,-20,-26,-25,-25,-22,-25,-30]
    for i in range(0,len(guitarFrequencies)):
        auxEnvelope = scaleEnvelope(guitarEnvelope,10**((relativeAmplitudes[i]-maxAmplitude)/20))
        envelopes.append(auxEnvelope)
    synthFunction = additiveSynthesis(guitarFrequencies,envelopes, fs)
    plt.figure("Guitar Signal")
    plt.plot(synthFunction)
    createWav(synthFunction, "adsrGuitar.wav", fs)
    return

def adsrDesvSynthGuitar(fo,tt):
    fs = 44100
    envelopes = []
    harmonics = 12
    guitarFrequencies = np.arange(fo,fo*harmonics+1,fo)
    pob = 19
    signProb = 1
    for i in range(0,len(guitarFrequencies)):
        desv = random.randint(0,93)/10000.0
        sign = random.randint(1,pob)
        if sign > signProb:
            desv = desv*(-1)
        guitarFrequencies[i] = guitarFrequencies[i]*(1+desv)
    guitarEnvelope = adsrEnvelope(0.07,0.038,0.6,2.7,tt,fs)
    maxAmplitude = -7
    relativeAmplitudes = [-7,-16,-16,-15,-18,-20,-26,-25,-25,-22,-25,-30]
    for i in range(0,len(guitarFrequencies)):
        auxEnvelope = scaleEnvelope(guitarEnvelope,10**((relativeAmplitudes[i]-maxAmplitude)/20))
        envelopes.append(auxEnvelope)
    synthFunction = additiveSynthesis(guitarFrequencies,envelopes, fs)
    plt.figure("Guitar Signal")
    plt.plot(synthFunction)
    createWav(synthFunction, "adsrDesvGuitar.wav", fs)
    return

def adsrSynthViolin(fo,tt):
    fs = 44100
    envelopes = []
    harmonics = 12
    violinFrequencies = np.arange(fo,fo*harmonics+1,fo)
    violinEnvelope =  adsrEnvelope(0.5,0,1,0.5,tt,fs)
    maxAmplitude = -22
    relativeAmplitudes = [-34,-24,-22,-28,-26,-26,-35,-34,-35,-32,-35,-37]
    for i in range(0,len(violinFrequencies)):
        auxEnvelope = scaleEnvelope(violinEnvelope,10**((relativeAmplitudes[i]-maxAmplitude)/20))
        envelopes.append(auxEnvelope)
    synthFunction = additiveSynthesis(violinFrequencies,envelopes, fs)
    plt.figure("Violin Signal")
    plt.plot(synthFunction)
    createWav(synthFunction, "adsrViolin.wav", fs)
    return

def adsrDesvSynthViolin(fo,tt):
    fs = 44100
    envelopes = []
    harmonics = 12
    violinFrequencies = np.arange(fo,fo*harmonics+1,fo)
    pob = 12
    signProb = 8
    for i in range(0,len(violinFrequencies)):
        desv = random.randint(0,79)/10000.0
        sign = random.randint(1,pob)
        if sign > signProb:
            desv = desv*(-1)
        violinFrequencies[i] = violinFrequencies[i]*(1+desv)
    violinEnvelope =  adsrEnvelope(0.5,0,1,0.5,tt,fs)
    maxAmplitude = -22
    relativeAmplitudes = [-34,-24,-22,-28,-26,-26,-35,-34,-35,-32,-35,-37]
    for i in range(0,len(violinFrequencies)):
        auxEnvelope = scaleEnvelope(violinEnvelope,10**((relativeAmplitudes[i]-maxAmplitude)/20))
        envelopes.append(auxEnvelope)
    synthFunction = additiveSynthesis(violinFrequencies,envelopes, fs)
    plt.figure("Violin Signal")
    plt.plot(synthFunction)
    createWav(synthFunction, "adsrDesvViolin.wav", fs)
    return

def adsrSynthSaxophone(fo,tt):
    fs = 44100
    envelopes = []
    harmonics = 19
    saxoFrequencies = np.arange(fo,fo*harmonics+1,fo)
    saxoEnvelope = adsrEnvelope(1/125,0.055,0.5,0.2,tt,fs)
    maxAmplitude = -18
    relativeAmplitudes = [-22,-32,-21,-18,-19,-22,-23,-37,-25,-32,-32,-25,-26,-26,-28,-30,-26,-30,-27]
    for i in range(0,len(saxoFrequencies)):
        auxEnvelope = scaleEnvelope(saxoEnvelope,10**((relativeAmplitudes[i]-maxAmplitude)/20))
        envelopes.append(auxEnvelope)
    synthFunction = additiveSynthesis(saxoFrequencies,envelopes, fs)
    plt.figure("Saxo Signal")
    plt.plot(synthFunction)
    createWav(synthFunction, "adsrSaxo.wav", fs)
    return

def adsrDesvSynthSaxophone(fo,tt):
    fs = 44100
    envelopes = []
    harmonics = 19
    saxoFrequencies = np.arange(fo,fo*harmonics+1,fo)
    pob = 19
    signProb = 1
    for i in range(0,len(saxoFrequencies)):
        desv = random.randint(0,93)/10000.0
        sign = random.randint(1,pob)
        if sign > signProb:
            desv = desv*(-1)
        saxoFrequencies[i] = saxoFrequencies[i]*(1+desv)
    saxoEnvelope = adsrEnvelope(1/125,0.055,0.5,0.2,tt,fs)
    maxAmplitude = -18
    relativeAmplitudes = [-22,-32,-21,-18,-19,-22,-23,-37,-25,-32,-32,-25,-26,-26,-28,-30,-26,-30,-27]
    for i in range(0,len(saxoFrequencies)):
        auxEnvelope = scaleEnvelope(saxoEnvelope,10**((relativeAmplitudes[i]-maxAmplitude)/20))
        envelopes.append(auxEnvelope)
    synthFunction = additiveSynthesis(saxoFrequencies,envelopes, fs)
    plt.figure("Saxo Signal")
    plt.plot(synthFunction)
    createWav(synthFunction, "adsrDesvSaxo.wav", fs)
    return


def adsrSynthTrumpet(fo,tt):
    fs = 44100
    envelopes = []
    harmonics = 11
    trumpetFrequencies = np.arange(fo,fo*harmonics+1,fo)
    trumpetEnvelope = adsrEnvelope(0.276-0.226,0,1,0.786-0.624,tt,fs)
    maxAmplitude = -15
    relativeAmplitudes = [-17,-15,-20,-22,-19,-24,-25,-24,-22,-26,-30]
    for i in range(0,len(trumpetFrequencies)):
        auxEnvelope = scaleEnvelope(trumpetEnvelope,10**((relativeAmplitudes[i]-maxAmplitude)/20))
        envelopes.append(auxEnvelope)
    synthFunction = additiveSynthesis(trumpetFrequencies,envelopes, fs)
    plt.figure("Trumpet Signal")
    plt.plot(synthFunction)
    createWav(synthFunction, "adsrTrumpet.wav", fs)
    return

def adsrDesvSynthTrumpet(fo,tt):
    fs = 44100
    envelopes = []
    harmonics = 11
    trumpetFrequencies = np.arange(fo,fo*harmonics+1,fo)
    pob = 19
    signProb = 1
    for i in range(0,len(trumpetFrequencies)):
        desv = random.randint(0,93)/10000.0
        sign = random.randint(1,19)
        if sign > signProb:
            desv = desv*(-1)
        trumpetFrequencies[i] = trumpetFrequencies[i]*(1+desv)
    trumpetEnvelope = adsrEnvelope(0.276-0.226,0,1,0.786-0.624,tt,fs)
    maxAmplitude = -15
    relativeAmplitudes = [-17,-15,-20,-22,-19,-24,-25,-24,-22,-26,-30]
    for i in range(0,len(trumpetFrequencies)):
        auxEnvelope = scaleEnvelope(trumpetEnvelope,10**((relativeAmplitudes[i]-maxAmplitude)/20))
        envelopes.append(auxEnvelope)
    synthFunction = additiveSynthesis(trumpetFrequencies,envelopes, fs)
    plt.figure("Trumpet Signal")
    plt.plot(synthFunction)
    createWav(synthFunction, "adsrDesvTrumpet.wav", fs)
    return