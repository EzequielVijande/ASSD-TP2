import matplotlib.pyplot as plt
import spectralAnalysis as sa
import additiveSynthesis as addsyn
from pathlib import Path

def realEnvelopeSynthesis(fileNameOrigin,fileNameDestination,npg):
    data_folder = Path("all-samples/")
    file_to_open = data_folder / fileNameOrigin
    fs, signalTime, signalData, fftF, fftData, stftF, stftT, stftData, nMax = sa.wavSpectralAnalysis(file_to_open)
    fHarmonic , amplitude = sa.findHarmonic(fftData,fftF, nMax)
    envelopes = sa.findEnvelopes(fHarmonic,signalData,fs,nMax,npg)
    synthFunc = addsyn.additiveSynthesis(fHarmonic,envelopes, fs)
    addsyn.createWav(synthFunc, fileNameDestination, fs)
    fs, synthSignalTime, synthSignalData, synthFftF, synthFftData, *extras = sa.wavSpectralAnalysis(fileNameDestination)
    for i in range(0,len(fHarmonic)):
        print("Harmonic %s: %s  Amplitude: %s" % (i,fHarmonic[i],amplitude[i]))
    plt.figure("Synth Signal")
    plt.plot(synthSignalTime,synthFunc)
    plt.ylabel("Amplitude")
    plt.xlabel("Time [sec]")
    plt.figure("Original Signal")
    plt.xlabel("Time [sec]")
    plt.ylabel("Amplitude")
    plt.plot(signalTime,signalData,color='b',label='signal')
    plt.legend(loc='upper right')
    plt.figure("Original Signal FFT")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude")
    plt.yscale('log')
    plt.plot(fftF,abs(fftData[:]),'r')
    plt.figure("Synth Signal FFT")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude")
    plt.yscale('log')
    plt.plot(synthFftF,abs(synthFftData[:]),'r')
    plt.show()


def main():
    #realEnvelopeSynthesis("trumpet_A4_15_forte_normal.wav","reTrumpet128.wav",128)
    #realEnvelopeSynthesis("violin_A4_15_fortissimo_arco-normal.wav","reViolin512.wav",512)
    #realEnvelopeSynthesis("saxophone_B3_1_fortissimo_normal.wav","reSaxo256.wav",256)
    realEnvelopeSynthesis("8403__speedy__clean-g-str-pluck.wav","reGuitar256.wav",256)


if __name__== "__main__":
  main()


