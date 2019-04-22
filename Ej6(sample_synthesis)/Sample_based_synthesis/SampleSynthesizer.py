import PhaseVocoder as ph
import OLA as o
import wave
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import math
import midi
import SpectrumSeparator as spectr
import synth

MIN_FORTE_INTENSITY = 63
GUITAR_PATH = '.\Samples\Guitar'

def ResampleArray(array,f_s_original,f_s_output,SameTimeLimit=True):
    input_points = array.size
    if(SameTimeLimit):
        output_points = math.ceil( (f_s_output/f_s_original)*input_points )
    else:
        output_points = math.floor( input_points/(f_s_original/f_s_output))

    output = np.zeros( output_points)
    output[0] = array[0]
    freq_factor= f_s_original/f_s_output
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

#Funcion que recibe el pitch, la duracion en muestras y la
#intensidad
class SampleSynthesizer(synth.Synthesizer):
    def __init__(self):
        self.set_create_notes_callback(self.MakeNote)
        super(SampleSynthesizer, self).__init__()
        self.set_create_notes_callback(self.MakeNote)
        #Genero los diccionarios con la muestra correspondiente a cda semitono
        #Para la guitara los valores son: (forte_sample,piano_sample,freq_factor)
        self.guitar_dict = dict([
            (midi.E_2,(GUITAR_PATH+"\E2_forte_trimmed.wav",GUITAR_PATH+"\E2_piano_trimmed.wav",1)),
            (midi.F_2,(GUITAR_PATH+"\E2_forte_trimmed.wav",GUITAR_PATH+"\E2_piano_trimmed.wav",0.9438743127)),
            (midi.Fs_2,(GUITAR_PATH+"\E2_forte_trimmed.wav",GUITAR_PATH+"\E2_piano_trimmed.wav",0.8908987181)),
            (midi.G_2,(GUITAR_PATH+"\Gs2_forte_trimmed.wav",GUITAR_PATH+"\Gs2_piano_trimmed.wav",1.059463094)),
            (midi.Gs_2,(GUITAR_PATH+"\Gs2_forte_trimmed.wav",GUITAR_PATH+"\Gs2_piano_trimmed.wav",1)),
            (midi.A_2,(GUITAR_PATH+"\Gs2_forte_trimmed.wav",GUITAR_PATH+"\Gs2_piano_trimmed.wav",0.9438743127)),
            (midi.As_2,(GUITAR_PATH+"\Gs2_forte_trimmed.wav",GUITAR_PATH+"\Gs2_piano_trimmed.wav",0.8908987181)),
            (midi.B_2,(GUITAR_PATH+"\C3_forte_trimmed.wav",GUITAR_PATH+"\C3_piano_trimmed.wav",1.059463094)),
            (midi.C_3,(GUITAR_PATH+"\C3_forte_trimmed.wav",GUITAR_PATH+"\C3_piano_trimmed.wav",1)),
            (midi.Cs_3,(GUITAR_PATH+"\C3_forte_trimmed.wav",GUITAR_PATH+"\C3_piano_trimmed.wav",0.9438743127)),
            (midi.D_3,(GUITAR_PATH+"\C3_forte_trimmed.wav",GUITAR_PATH+"\C3_piano_trimmed.wav",0.8908987181)),
            (midi.Ds_3,(GUITAR_PATH+"\E3_forte_trimmed.wav",GUITAR_PATH+"\E3_piano_trimmed.wav",1.059463094)),
            (midi.E_3,(GUITAR_PATH+"\E3_forte_trimmed.wav",GUITAR_PATH+"\E3_piano_trimmed.wav",1)),
            (midi.F_3,(GUITAR_PATH+"\E3_forte_trimmed.wav",GUITAR_PATH+"\E3_piano_trimmed.wav",0.9438743127)),
            (midi.Fs_3,(GUITAR_PATH+"\E3_forte_trimmed.wav",GUITAR_PATH+"\E3_piano_trimmed.wav",0.8908987181)),
            (midi.G_3,(GUITAR_PATH+"\Gs3_forte_trimmed.wav",GUITAR_PATH+"\Gs3_piano_trimmed.wav",1.059463094)),
            (midi.Gs_3,(GUITAR_PATH+"\Gs3_forte_trimmed.wav",GUITAR_PATH+"\Gs3_piano_trimmed.wav",1)),
            (midi.A_3,(GUITAR_PATH+"\Gs3_forte_trimmed.wav",GUITAR_PATH+"\Gs3_piano_trimmed.wav",0.9438743127)),
            (midi.As_3,(GUITAR_PATH+"\Gs3_forte_trimmed.wav",GUITAR_PATH+"\Gs3_piano_trimmed.wav",0.8908987181)),
            (midi.B_3,(GUITAR_PATH+"\C4_forte_trimmed.wav",GUITAR_PATH+"\C4_forte_trimmed.wav",1.059463094)),
            (midi.C_4,(GUITAR_PATH+"\C4_forte_trimmed.wav",GUITAR_PATH+"\C4_forte_trimmed.wav",1)),
            (midi.Cs_4,(GUITAR_PATH+"\C4_forte_trimmed.wav",GUITAR_PATH+"\C4_forte_trimmed.wav",0.9438743127)),
            (midi.D_4,(GUITAR_PATH+"\E4_forte_trimmed.wav",GUITAR_PATH+"\E4_piano_trimmed.wav",1.122462048)),
            (midi.Ds_4,(GUITAR_PATH+"\E4_forte_trimmed.wav",GUITAR_PATH+"\E4_piano_trimmed.wav",1.059463094)),
            (midi.E_4,(GUITAR_PATH+"\E4_forte_trimmed.wav",GUITAR_PATH+"\E4_piano_trimmed.wav",1)),
            (midi.F_4,(GUITAR_PATH+"\E4_forte_trimmed.wav",GUITAR_PATH+"\E4_piano_trimmed.wav",0.9438743127)),
            (midi.Fs_4,(GUITAR_PATH+"\E4_forte_trimmed.wav",GUITAR_PATH+"\E4_piano_trimmed.wav",0.8908987181)),
            (midi.G_4,(GUITAR_PATH+"\Gs4_forte_trimmed.wav",GUITAR_PATH+"\Gs4_piano_trimmed.wav",1.059463094)),
            (midi.Gs_4,(GUITAR_PATH+"\Gs4_forte_trimmed.wav",GUITAR_PATH+"\Gs4_piano_trimmed.wav",1)),
            (midi.A_4,(GUITAR_PATH+"\Gs4_forte_trimmed.wav",GUITAR_PATH+"\Gs4_piano_trimmed.wav",0.9438743127)),
            (midi.As_4,(GUITAR_PATH+"\Gs4_forte_trimmed.wav",GUITAR_PATH+"\Gs4_piano_trimmed.wav",0.8908987181)),
            (midi.B_4,(GUITAR_PATH+"\C5_trimmed.wav",GUITAR_PATH+"\C5_trimmed.wav",1.059463094)),
            (midi.C_5,(GUITAR_PATH+"\C5_trimmed.wav",GUITAR_PATH+"\C5_trimmed.wav",1)),
            (midi.Cs_5,(GUITAR_PATH+"\C5_trimmed.wav",GUITAR_PATH+"\C5_trimmed.wav",0.9438743127)),
            (midi.D_5,(GUITAR_PATH+"\E5_forte_trimmed.wav",GUITAR_PATH+"\E5_piano_trimmed.wav",1.122462048)),
            (midi.Ds_5,(GUITAR_PATH+"\E5_forte_trimmed.wav",GUITAR_PATH+"\E5_piano_trimmed.wav",1.059463094)),
            (midi.E_5,(GUITAR_PATH+"\E5_forte_trimmed.wav",GUITAR_PATH+"\E5_piano_trimmed.wav",1)),
            (midi.F_5,(GUITAR_PATH+"\E5_forte_trimmed.wav",GUITAR_PATH+"\E5_piano_trimmed.wav",0.9438743127)),
            (midi.Fs_5,(GUITAR_PATH+"\E5_forte_trimmed.wav",GUITAR_PATH+"\E5_piano_trimmed.wav",0.8908987181)),
            (midi.G_5,(GUITAR_PATH+"\Gs5_forte_trimmed.wav",GUITAR_PATH+"\Gs5_forte_trimmed.wav",1.059463094)),
            (midi.Gs_5,(GUITAR_PATH+"\Gs5_forte_trimmed.wav",GUITAR_PATH+"\Gs5_forte_trimmed.wav",1)),
            (midi.A_5,(GUITAR_PATH+"\Gs5_forte_trimmed.wav",GUITAR_PATH+"\Gs5_forte_trimmed.wav",0.9438743127)),
            (midi.As_5,(GUITAR_PATH+"\Gs5_forte_trimmed.wav",GUITAR_PATH+"\Gs5_forte_trimmed.wav",0.8908987181)),
            (midi.B_5,(GUITAR_PATH+"\C6_forte_trimmed.wav",GUITAR_PATH+"\C6_forte_trimmed.wav",1.059463094)),
            (midi.C_6,(GUITAR_PATH+"\C6_forte_trimmed.wav",GUITAR_PATH+"\C6_forte_trimmed.wav",1))
            ])

    def MakeNote(self,pitch,duration,intensity,instrument='guitar'):
        desired_fs = self.frame_rate
        note = np.zeros(duration)
        if( instrument == 'guitar'):
            fmin = 82 #Frecuencia minima de un semitono de guitarra
            if( pitch < midi.E_2):
                forte_sample= GUITAR_PATH+"\E2_forte_trimmed.wav"
                piano_sample= GUITAR_PATH+"\E2_piano_trimmed.wav"
                freq_factor = 1
            elif( pitch > midi.C_6):
                forte_sample = GUITAR_PATH+"\C6_forte_trimmed.wav"
                piano_sample = GUITAR_PATH+"\C6_piano_trimmed.wav"
                freq_factor = 1
            else:
                forte_sample,piano_sample,freq_factor = self.guitar_dict[pitch]

            if intensity >= MIN_FORTE_INTENSITY: #cargo nota con velocidad alta
                f_s, data= wavfile.read(forte_sample)
            else: #cargo nota con velocidad baja
                f_s, data= wavfile.read(piano_sample)
            pitch_corrected_data = ResampleArray(data,f_s,int(f_s/freq_factor),SameTimeLimit=False)
            resampled_data = ResampleArray(pitch_corrected_data,int(f_s/freq_factor),desired_fs)
            if((duration/desired_fs)>(1/fmin)):
                N= 2*int(desired_fs/fmin)
            else:
                N= int(0.1*duration) #La duracion es menor que el periodo undamental minimo
            #t_h, harm, t_p, perc = spectr.GetPercussiveAndHarmonicSpectrum(resampled_data,frame_size = N,beta=2)
            t_h = (1.0/desired_fs)*np.linspace(0,duration)
            window = MakeWindow(N)
            stretch_factor = (duration)/t_h[-1]
            stretch_func = stretch_factor*t_h
            #y_h= ph.PhVocoder(harm,window,stretch_func,int(0.1*N))
            #y_p= o.OLA(perc,window,stretch_func,0.1)
            note= o.OLA(resampled_data,window,stretch_func,0.1)
            #note = y_h + y_p
            #Normalizo el vector
            note_max_pos = np.max(note)
            note_max_neg = np.min(note)
            if( note_max_pos != 0)and( note_max_neg != 0):
                if( abs(note_max_pos) > abs(note_max_neg)):
                    note = note/abs(note_max_pos)
                else:
                    note = note/abs(note_max_neg)

        return note
    def SetInstrument(self,inst):
        self.instrument = inst

