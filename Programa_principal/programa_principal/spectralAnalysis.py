import scipy.fftpack as fft
import scipy.signal as signal
import numpy as np
from scipy.io import wavfile

import matplotlib.pyplot as plt


def wavSpectralAnalysis(wavPath):
    fs, data = wavfile.read(wavPath)
    data=[(ele/2**16.)*2 for ele in data] # normalizo a (-1,1)
    if type(data[0]) == type(np.array([0,0])):
        # convierto en mono
        auxData = []
        for i in range(0,len(data)):
            auxData.append(data[i][0])
        data = auxData   
    data = np.array(data)
    nMax = 100000
    if len(data) < nMax:
        nMax = len(data)
    signalTime = np.arange(0,nMax/fs,1/fs)
    intSize = 16.
    signalData = data[:nMax]
    k = np.arange(nMax)
    T = (2*nMax)/fs
    fftF = k/T 
    fftData = fft.rfft(signalData)
    fftData = abs(fftData[:])
    return fs, signalTime, signalData, fftF, fftData, nMax

def findHarmonic(fftData,fftF,nMax):
    fMax = 22050
    fftData = abs(fftData[:])
    fHarmonic = []
    amplitude = []
    sampleConv = nMax/fMax
    maxAmp = np.amax(fftData) # la maxima puede no ser la fundamental
    threshold = 0.2*maxAmp
    maxAmpFreq = fftF[np.argmax(fftData)]
    foundFund = False
    currentMaxIndex = np.argmax(fftData)
    fundamentalFreq = maxAmpFreq
    fundamentalAmp = maxAmp
    while(not foundFund): # busco la verdadera fundamental (primer pico con por lo menos 10% de la maxima amplitud)
        if currentMaxIndex>40:
            auxData = fftData[0:currentMaxIndex-40]
            auxMaxAmp = np.amax(auxData) # la maxima puede no ser la fundamental
            auxMaxAmpFreq = fftF[np.argmax(auxData)]
        else:
            auxMaxAmp = 0
        if auxMaxAmp < threshold:
            # termino de buscar fundamental
            foundFund = True
        else:
            # sigo buscando fundamental
            fundamentalFreq = auxMaxAmpFreq
            fundamentalAmp = auxMaxAmp
            currentMaxIndex = np.argmax(auxData)
    fHarmonic.append(fundamentalFreq)
    n = np.int_(np.floor(20000/fundamentalFreq))
    for i in range(2,n):
        freqI = i*fundamentalFreq-(fundamentalFreq/2) 
        freqF = i*fundamentalFreq+(fundamentalFreq/2)
        ni = np.int_(np.floor(freqI*sampleConv))
        nf = np.int_(np.ceil(freqF*sampleConv))
        auxArray = fftData[ni:nf]
        for j in range(ni,nf):
            if fftData[j] == max(auxArray):
                fHarmonic.append(fftF[j])
                break
    return fHarmonic

def findEnvelopes(fHarmonic,signalData,fs,nMax):
    envelopes = [] # arreglo de arreglos cada arreglo contiene una envolvente para el armonico correspondiente
    stftF, stftT, stftData = signal.spectrogram(signalData,fs, nperseg=2000,noverlap = 1800,nfft = 4000)
    signalTime = np.arange(0,nMax/fs,1/fs)
    index = 0
    for i in range(0,len(fHarmonic)):
        for j in range(index,len(stftF)):
            if stftF[j]<=fHarmonic[i] and stftF[j+1]> fHarmonic[i]:
                auxEnvelope = np.interp(signalTime,stftT,stftData[j])
                envelopes.append(auxEnvelope)
                index = j
                break
    return envelopes