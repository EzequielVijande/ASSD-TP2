import scipy.fftpack as fft
import scipy.signal as signal
import numpy as np
from scipy.io import wavfile

def wavSpectralAnalysis(wavPath):
    fs, data = wavfile.read(wavPath)
    nMax = 100000
    signalTime = np.arange(0,nMax/fs,1/fs)
    intSize = 16.
    signalData = data[:nMax]
    print("Frequency sampling", fs)
    k = np.arange(nMax)
    T = nMax/fs
    fftF = k/(T)  
    fftData = fft.rfft(signalData)
    stftF, stftT, stftData = signal.spectrogram(signalData,fs, nperseg=256)
    return fs, signalTime, signalData, fftF, fftData, stftF, stftT, stftData

def findHarmonic(fftData,fftF):
    fHarmonic = []
    amplitude = []
    fundamentalAmp = np.amax(fftData)
    fundamentalFreq = fftF[np.argmax(fftData)]
    fHarmonic.append(fundamentalFreq)
    amplitude.append(fundamentalAmp)
    n = np.int_(np.floor(20000/fundamentalFreq))
    for i in range(2,n):
        freqI = i*fundamentalFreq-(fundamentalFreq/2) 
        freqF = i*fundamentalFreq+(fundamentalFreq/2)
        ni = np.int_(np.floor(freqI*1000/441))
        nf = np.int_(np.ceil(freqF*1000/441))
        auxArray = fftData[ni:nf]
        for j in range(ni,nf):
            if fftData[j] == max(auxArray):
                fHarmonic.append(fftF[j])
                break
        amplitude.append(max(auxArray))
    return fHarmonic , amplitude

def findEnvelopes(fHarmonic,signalData,fs):
    envelopes = [] # arreglo de arreglos cada arreglo contiene una envolvente para el armonico correspondiente 
    hilbertTransform = signal.hilbert(signalData)
    amplitude_envelope = np.abs(hilbertTransform)
    return amplitude_envelope


    #fftData = fft.rfft(signalData)
    #k = np.arange(len(signalData))
    #T = nMax/fs
    #fftF = k/T 
    #for i in range(0,len(fHarmonic)):
    #    auxData = fftData
    #    freqI = fHarmonic[i]-(fHarmonic[0]/2) 
    #    freqF = fHarmonic[i]+(fHarmonic[0]/2)
    #    for j in range(0,len(fftData)):
    #        if 