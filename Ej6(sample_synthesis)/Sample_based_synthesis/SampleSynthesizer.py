import PhaseVocoder as ph
import OLA as o
import wave
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import math
import midi
import SpectrumSeparator as spectr

MIN_FORTE_INTENSITY = 63

def ResampleArray(array,f_s_original,f_s_output):
    input_points = array.size
    output_points = math.ceil( (f_s_output/f_s_original)*input_points )
    output = np.zeros( output_points)
    freq_factor= f_s_original/f_s_output
    output[0] = array[0]
    for i in range(1,output.size):
        if( math.floor(freq_factor*i)+1 < input_points):
            output[i] = 0.5*(array[math.floor(freq_factor*i)] + array[math.floor(freq_factor*i)+1])
        else:
            output[i] = array[math.floor(freq_factor*i)]

    return output

def MakeWindow(length,type='Hann'):
    if(type== 'Hann'):
        return np.hanning(length)
    else:
        return np.zeros(1)

#Funcion que recibe el pitch, la duracion en segundos y la
#intensidad
def MakeNote(pitch,duration,intensity,desired_fs,instrument='guitar'):
    note = np.zeros(int(duration*desired_fs))
    if( instrument == 'guitar'):
        fmin=82 #Frecuencia minima de un semitono de guitarra.
        if pitch == midi.C_3:
            if intensity >= MIN_FORTE_INTENSITY: #cargo nota con velocidad alta
                f_s, data= wavfile.read(".\Samples\Guitar\C3_forte_trimmed.wav")
            else: #cargo nota con velocidad baja
                f_s, data= wavfile.read(".\Samples\Guitar\C3_piano_trimmed.wav")
            resampled_data = ResampleArray(data,f_s,desired_fs)
            N= 2*int(desired_fs/fmin)
            t_h, harm, t_p, perc = spectr.GetPercussiveAndHarmonicSpectrum(resampled_data,frame_size = N,beta=2)
            window = MakeWindow(N)
            stretch_factor = (duration*desired_fs)/t_h[-1]
            stretch_func = stretch_factor*t_h
            y_h= ph.PhVocoder(harm,window,stretch_func,int(0.1*N))
            y_p= o.OLA(perc,window,stretch_func,0.1)
            note = y_h + y_p
        if pitch == midi.C_5:
            f_s, data= wavfile.read(".\Samples\Guitar\C5.wav")

    return note


