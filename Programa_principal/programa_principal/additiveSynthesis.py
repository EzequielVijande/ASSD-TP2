import synth
import numpy as np
import random
from pathlib import Path
import spectralAnalysis as sa
import OLA as ola

import matplotlib.pyplot as plt

# envelope files
GUITAR_ENVELOPE = "guitarSample.wav"
VIOLIN_ENVELOPE = "violinSample.wav"
SAXO_ENVELOPE = "saxophoneSample.wav"
TRUMPET_ENVELOPE = "trumpetSample.wav"

# envelope index
GUITAR = 0
VIOLIN = 1
SAXO = 2
TRUMPET = 3

def getNperseg(instrument):
    nperseg = 0
    if instrument == GUITAR:
        nperseg = 256
    elif instrument == VIOLIN:
        nperseg = 512
    elif instrument == SAXO:
        nperseg = 512
    elif instrument == TRUMPET:
        nperseg = 512
    return nperseg

def getInstNumber(instrument):
    instNumb = 0
    if instrument == synth.GUITAR:
        instNumb = GUITAR
    elif instrument == synth.VIOLIN:
        instNumb = VIOLIN
    elif instrument == synth.SAXO:
        instNumb = SAXO
    elif instrument == synth.TRUMPET:
        instNumb = TRUMPET
    return instNumb

def initEnvelopes(files,maxNumber):
    originalEnvelopes = []
    for i in range(0,len(files)):
        npg = getNperseg(i)
        data_folder = Path("all-samples/")
        file_to_open = data_folder / files[i]
        fs, signalTime, signalData, fftF, fftData, stftF, stftT, stftData, nMax = sa.wavSpectralAnalysis(file_to_open)
        fHarmonic = sa.findHarmonic(fftData,fftF, nMax)
        auxEnvelopes = sa.findEnvelopes(fHarmonic,signalData,fs,nMax,npg)
        if len(auxEnvelopes) > maxNumber:
            auxEnvelopes = auxEnvelopes[:maxNumber] 
        originalEnvelopes.append(auxEnvelopes)
        print("Envelope %s Initialized Successfully" % (i))
    print("Additive Synthesis Envelopes Initialized Successfully")
    return originalEnvelopes

class envelope():
    def __init__(self, envelopes,instrumentString,asample,ssamplei,ssamplef,rsample):
        self.AllEnvelopes = envelopes
        self.instrument = getInstNumber(instrumentString)
        self.attackSample = asample
        self.sustainSamples = [ssamplei,ssamplef]
        self.releaseSample = rsample
        
    def newResizedEnv(self,sampleNumber):
        newEnvelope = self.AllEnvelopes
        #reshape
        return newEnvelope


class additiveSynthesis(synth.Synthesizer):
    def __init__(self, resolution):
        self.set_create_notes_callback(self.create_note_array)
        super(additiveSynthesis, self).__init__(resolution)
        files = []
        files.append(GUITAR_ENVELOPE)
        files.append(VIOLIN_ENVELOPE)
        files.append(SAXO_ENVELOPE)
        files.append(TRUMPET_ENVELOPE)
        self.originalEnvelopes = initEnvelopes(files,30)
        self.guitarEnvelope = envelope(self.originalEnvelopes[GUITAR],'guitar',1248,0,0,3936)
        self.violinEnvelope = envelope(self.originalEnvelopes[VIOLIN],'violin',8340,11847,18163,18163)
        self.saxoEnvelope = envelope(self.originalEnvelopes[SAXO],'saxophone',2508,2508,26663,26663)
        self.trumpetrEnvelope = envelope(self.originalEnvelopes[TRUMPET],'trumpet',15049,25777,92525,92525)

    # Asume duracion total igual al largo de la envolvente
    # Suma armonicos con su envolvente correspondiente
    # Recibe dos arrays, con las frecuencias y su envolvente correspondiente en el mismo indice del arreglo.
    # Recibe la frecuencia de sampleo. Recibe si se quiere desnormalizar la funcion.
    # Devuelve una arreglo con la funcion final sintetisada
    def additiveSynthesis(self,frequencies,envelope, fs, desnorm = True):
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

    def scaleEnvelope(self,envelope,k):
        scaledEnvelope = []
        scaledEnvelope = np.multiply(k,envelope)
        scaledEnvelope = np.int16(scaledEnvelope)
        return scaledEnvelope

    def defineFrequencies(self,fundamentalFreq,instrument):
        frequencies = []
        harmonics = 30
        frequencies = np.arange(fundamentalFreq,fundamentalFreq*harmonics+1,fundamentalFreq)
        return frequencies

    def getEnvelopes(self,amount_of_ns,instrument):
        instNumber = getInstNumber(instrument)
        envelopes = self.originalEnvelopes[instNumber]
        envLength = len(envelopes[0])
        t = np.linspace(0,envLength,envLength)
        scale = amount_of_ns/envLength
        t_func = scale*t
        for i in range(0,len(envelopes)):
            envelopes[i] = ola.OLA(envelopes[i],np.ones(250),t_func,0)
        #plt.plot(envelopes[0])
        #plt.show()
        return envelopes

    def create_note_array(self, pitch, amount_of_ns: int, velocity, instrument):
        fundamentalFreq =  2**((pitch - 69) / 12)*440
        intensity = velocity/127
        fs = self.frame_rate
        frequencies = self.defineFrequencies(fundamentalFreq,instrument)
        envelopes = self.getEnvelopes(amount_of_ns,instrument)
        note = self.additiveSynthesis(frequencies,envelopes, fs)
        if intensity < 1:
            note = self.scaleEnvelope(note,intensity)
        return note


