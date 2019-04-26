import matplotlib.pyplot as plt
import scipy.fftpack as fft
import spectralAnalysis as sa
import scipy.signal as signal
import numpy as np
from scipy.io import wavfile
from pathlib import Path

def main():
    data_folder = Path("all-samples/")
    file_to_open = data_folder / "8403__speedy__clean-g-str-pluck.wav"
    fs, signalTime, signalData, fftF, fftData, stftF, stftT, stftData = sa.wavSpectralAnalysis(file_to_open)
    fHarmonic , amplitude = sa.findHarmonic(fftData,fftF)
    envelopes = sa.findEnvelopes(fHarmonic,signalData,fs)
    for i in range(0,len(fHarmonic)):
        print("Harmonic %s: %s  Amplitude: %s" % (i,fHarmonic[i],amplitude[i]))
    plt.figure("Original Signal")
    plt.xlabel("Time [sec]")
    plt.ylabel("Amplitude")
    plt.plot(signalTime,signalData,color='b',label='signal')
    plt.plot(signalTime,envelopes,color = 'orange', label='envelope')
    plt.legend(loc='upper right')
    plt.figure("Fourier Transform")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude")
    plt.yscale('log')
    plt.plot(fftF,abs(fftData[:]),'r')
    plt.figure("Spectrogram")
    plt.pcolormesh(stftT,stftF,stftData)
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [sec]")
    plt.show()

if __name__== "__main__":
  main()

