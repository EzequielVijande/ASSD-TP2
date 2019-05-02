import matplotlib.pyplot as plt
import additiveSynthesis as addsyn
import spectralAnalysis as sa
from pathlib import Path

def plotSample(fileNameOrigin):
    data_folder = Path("all-samples/")
    file_to_open = data_folder / fileNameOrigin
    fs, signalTime, signalData, fftF, fftData, stftF, stftT, stftData, nMax = sa.wavSpectralAnalysis(file_to_open)
    plt.figure("Original Signal")
    plt.xlabel("Samples [n]")
    plt.ylabel("Amplitude")
    plt.plot(signalData)
    plt.figure("FFT")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude")
    plt.plot(fftF,abs(fftData[:]), label = "Original Signal FFT")


def main():
    fs = 44100
    nMax = 100000
    addsyn.adsrSynthGuitar(195.584,nMax/fs)
    addsyn.adsrDesvSynthGuitar(195.584,nMax/fs)
    plotSample("8403__speedy__clean-g-str-pluck.wav")
    plt.legend(loc='upper right')
    plt.show()
    addsyn.adsrSynthViolin(435.267,nMax/fs)
    addsyn.adsrDesvSynthViolin(435.267,nMax/fs)
    plotSample("violin_A4_15_fortissimo_arco-normal.wav")
    plt.legend(loc='upper right')
    plt.show()
    addsyn.adsrSynthSaxophone(252.2,3)
    addsyn.adsrDesvSynthSaxophone(252.2,3)
    plotSample("saxophone_B3_1_fortissimo_normal.wav")
    plt.legend(loc='upper right')
    plt.show()
    addsyn.adsrSynthTrumpet(441,nMax/fs)
    addsyn.adsrDesvSynthTrumpet(441,nMax/fs)
    plotSample("trumpet_A4_15_forte_normal.wav")
    plt.legend(loc='upper right')
    plt.show()

if __name__== "__main__":
  main()
