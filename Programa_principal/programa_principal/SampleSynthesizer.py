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
import WSOLA as w

MIN_FORTE_INTENSITY = 63
GUITAR_PATH = '.\\Samples\\Guitar'
COR_ANGLAIS_PATH = '.\\Samples\\Cor Anglais'
DRUMS_PATH = '.\\Samples\\Drums'
TRUMPET_PATH = ''

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
    def __init__(self,resolution):
        self.set_create_notes_callback(self.MakeNote)
        super(SampleSynthesizer, self).__init__(resolution)
        self.set_create_notes_callback(self.MakeNote)
        #Genero los diccionarios con la muestra correspondiente a cda semitono
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
            ]) #Para la guitara los valores son: (forte_sample,piano_sample,freq_factor)
        self.corn_dict = dict([
            (midi.E_3, (COR_ANGLAIS_PATH+"\E3_15_fortissimo.wav",COR_ANGLAIS_PATH+"\E3_15_piano.wav",COR_ANGLAIS_PATH+"\E3_025_mezzo_forte.wav",COR_ANGLAIS_PATH+"\E3_025_piano.wav",1)),
            (midi.F_3, (COR_ANGLAIS_PATH+"\E3_15_fortissimo.wav",COR_ANGLAIS_PATH+"\E3_15_piano.wav",COR_ANGLAIS_PATH+"\E3_025_mezzo_forte.wav",COR_ANGLAIS_PATH+"\E3_025_piano.wav",1.059463094)),
            (midi.Fs_3, (COR_ANGLAIS_PATH+"\Gs3_15_forte.wav",COR_ANGLAIS_PATH+"\Gs3_15_piano.wav",COR_ANGLAIS_PATH+"\Gs3_025_forte.wav",COR_ANGLAIS_PATH+"\Gs3_025_piano.wav",0.8908987181)),
            (midi.G_3, (COR_ANGLAIS_PATH+"\Gs3_15_forte.wav",COR_ANGLAIS_PATH+"\Gs3_15_piano.wav",COR_ANGLAIS_PATH+"\Gs3_025_forte.wav",COR_ANGLAIS_PATH+"\Gs3_025_piano.wav",0.9438743127)),
            (midi.Gs_3, (COR_ANGLAIS_PATH+"\Gs3_15_forte.wav",COR_ANGLAIS_PATH+"\Gs3_15_piano.wav",COR_ANGLAIS_PATH+"\Gs3_025_forte.wav",COR_ANGLAIS_PATH+"\Gs3_025_piano.wav",1)),
            (midi.A_3, (COR_ANGLAIS_PATH+"\Gs3_15_forte.wav",COR_ANGLAIS_PATH+"\Gs3_15_piano.wav",COR_ANGLAIS_PATH+"\Gs3_025_forte.wav",COR_ANGLAIS_PATH+"\Gs3_025_piano.wav",1.059463094)),
            (midi.As_3, (COR_ANGLAIS_PATH+"\B3_15_forte.wav",COR_ANGLAIS_PATH+"\B3_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\B3_025_forte.wav",COR_ANGLAIS_PATH+"\B3_025_mezzo-piano.wav",0.9438743127)),
            (midi.B_3, (COR_ANGLAIS_PATH+"\B3_15_forte.wav",COR_ANGLAIS_PATH+"\B3_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\B3_025_forte.wav",COR_ANGLAIS_PATH+"\B3_025_mezzo-piano.wav",1)),
            (midi.C_4, (COR_ANGLAIS_PATH+"\B3_15_forte.wav",COR_ANGLAIS_PATH+"\B3_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\B3_025_forte.wav",COR_ANGLAIS_PATH+"\B3_025_mezzo-piano.wav",1.059463094)),
            (midi.Cs_4, (COR_ANGLAIS_PATH+"\B3_15_forte.wav",COR_ANGLAIS_PATH+"\B3_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\B3_025_forte.wav",COR_ANGLAIS_PATH+"\B3_025_mezzo-piano.wav",1.122462048)),
            (midi.D_4, (COR_ANGLAIS_PATH+"\E4_15_forte.wav",COR_ANGLAIS_PATH+"\E4_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\E4_025_forte.wav",COR_ANGLAIS_PATH+"\E4_025_mezzo-piano.wav",0.8908987181)),
            (midi.Ds_4, (COR_ANGLAIS_PATH+"\E4_15_forte.wav",COR_ANGLAIS_PATH+"\E4_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\E4_025_forte.wav",COR_ANGLAIS_PATH+"\E4_025_mezzo-piano.wav",0.9438743127)),
            (midi.E_4, (COR_ANGLAIS_PATH+"\E4_15_forte.wav",COR_ANGLAIS_PATH+"\E4_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\E4_025_forte.wav",COR_ANGLAIS_PATH+"\E4_025_mezzo-piano.wav",1)),
            (midi.F_4, (COR_ANGLAIS_PATH+"\E4_15_forte.wav",COR_ANGLAIS_PATH+"\E4_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\E4_025_forte.wav",COR_ANGLAIS_PATH+"\E4_025_mezzo-piano.wav",1.059463094)),
            (midi.Fs_4, (COR_ANGLAIS_PATH+"\Gs4_15_forte.wav",COR_ANGLAIS_PATH+"\Gs4_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\Gs4_025_forte.wav",COR_ANGLAIS_PATH+"\Gs4_025_mezzo-piano.wav",0.8908987181)),
            (midi.G_4, (COR_ANGLAIS_PATH+"\Gs4_15_forte.wav",COR_ANGLAIS_PATH+"\Gs4_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\Gs4_025_forte.wav",COR_ANGLAIS_PATH+"\Gs4_025_mezzo-piano.wav",0.9438743127)),
            (midi.Gs_4, (COR_ANGLAIS_PATH+"\Gs4_15_forte.wav",COR_ANGLAIS_PATH+"\Gs4_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\Gs4_025_forte.wav",COR_ANGLAIS_PATH+"\Gs4_025_mezzo-piano.wav",1)),
            (midi.A_4, (COR_ANGLAIS_PATH+"\Gs4_15_forte.wav",COR_ANGLAIS_PATH+"\Gs4_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\Gs4_025_forte.wav",COR_ANGLAIS_PATH+"\Gs4_025_mezzo-piano.wav",1.059463094)),
            (midi.As_4, (COR_ANGLAIS_PATH+"\B4_15_forte.wav",COR_ANGLAIS_PATH+"\B4_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\B4_025_forte.wav",COR_ANGLAIS_PATH+"\B4_025_mezzo-piano.wav",0.9438743127)),
            (midi.B_4, (COR_ANGLAIS_PATH+"\B4_15_forte.wav",COR_ANGLAIS_PATH+"\B4_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\B4_025_forte.wav",COR_ANGLAIS_PATH+"\B4_025_mezzo-piano.wav",1)),
            (midi.C_5, (COR_ANGLAIS_PATH+"\B4_15_forte.wav",COR_ANGLAIS_PATH+"\B4_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\B4_025_forte.wav",COR_ANGLAIS_PATH+"\B4_025_mezzo-piano.wav",1.059463094)),
            (midi.Cs_5, (COR_ANGLAIS_PATH+"\B4_15_forte.wav",COR_ANGLAIS_PATH+"\B4_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\B4_025_forte.wav",COR_ANGLAIS_PATH+"\B4_025_mezzo-piano.wav",1.122462048)),
            (midi.D_5, (COR_ANGLAIS_PATH+"\E5_15_forte.wav",COR_ANGLAIS_PATH+"\E5_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\E5_025_forte.wav",COR_ANGLAIS_PATH+"\E5_025_mezzo-piano.wav",0.8908987181)),
            (midi.Ds_5, (COR_ANGLAIS_PATH+"\E5_15_forte.wav",COR_ANGLAIS_PATH+"\E5_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\E5_025_forte.wav",COR_ANGLAIS_PATH+"\E5_025_mezzo-piano.wav",0.9438743127)),
            (midi.E_5, (COR_ANGLAIS_PATH+"\E5_15_forte.wav",COR_ANGLAIS_PATH+"\E5_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\E5_025_forte.wav",COR_ANGLAIS_PATH+"\E5_025_mezzo-piano.wav",1)),
            (midi.F_5, (COR_ANGLAIS_PATH+"\E5_15_forte.wav",COR_ANGLAIS_PATH+"\E5_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\E5_025_forte.wav",COR_ANGLAIS_PATH+"\E5_025_mezzo-piano.wav",1.059463094)),
            (midi.Fs_5, (COR_ANGLAIS_PATH+"\Gs5_15_forte.wav",COR_ANGLAIS_PATH+"\Gs5_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\Gs5_025_forte.wav",COR_ANGLAIS_PATH+"\Gs5_025_mezzo-piano.wav",0.8908987181)),
            (midi.G_5, (COR_ANGLAIS_PATH+"\Gs5_15_forte.wav",COR_ANGLAIS_PATH+"\Gs5_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\Gs5_025_forte.wav",COR_ANGLAIS_PATH+"\Gs5_025_mezzo-piano.wav",0.9438743127)),
            (midi.Gs_5, (COR_ANGLAIS_PATH+"\Gs5_15_forte.wav",COR_ANGLAIS_PATH+"\Gs5_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\Gs5_025_forte.wav",COR_ANGLAIS_PATH+"\Gs5_025_mezzo-piano.wav",1)),
            (midi.A_5, (COR_ANGLAIS_PATH+"\Gs5_15_forte.wav",COR_ANGLAIS_PATH+"\Gs5_15_mezzo-piano.wav",COR_ANGLAIS_PATH+"\Gs5_025_forte.wav",COR_ANGLAIS_PATH+"\Gs5_025_mezzo-piano.wav",1.059463094)),
            (midi.As_5, (COR_ANGLAIS_PATH+"\B5_1_forte.wav",COR_ANGLAIS_PATH+"\B5_1_mezzo-piano.wav",COR_ANGLAIS_PATH+"\B5_025_forte.wav",COR_ANGLAIS_PATH+"\B5_025_mezzo-piano.wav",0.9438743127)),
            (midi.B_5, (COR_ANGLAIS_PATH+"\B5_1_forte.wav",COR_ANGLAIS_PATH+"\B5_1_mezzo-piano.wav",COR_ANGLAIS_PATH+"\B5_025_forte.wav",COR_ANGLAIS_PATH+"\B5_025_mezzo-piano.wav",1)),
            (midi.C_6, (COR_ANGLAIS_PATH+"\B5_1_forte.wav",COR_ANGLAIS_PATH+"\B5_1_mezzo-piano.wav",COR_ANGLAIS_PATH+"\B5_025_forte.wav",COR_ANGLAIS_PATH+"\B5_025_mezzo-piano.wav",1.059463094))
            ])     #Para el corn anglais los valores son: (forte_1.5,piano_1.5,forte_0.5,piano_0.5,freq_factor)
        #Diccionario donde guardo las notas ya sintetizadas
        self.note_dict = dict()
        self.curr_instrument = ""

    def MakeNote(self,pitch,duration,intensity,instrument='guitar'):
        note = np.zeros(duration)
        if (self.curr_instrument != instrument): #reinicio el diccionario cuando se cambia de instrumento
            self.note_dict.clear()
        self.curr_instrument = instrument
        value_type = str(type(self.note_dict.get((pitch,duration,intensity),1)))
        if(value_type == "<class 'int'>"):
            desired_fs = self.frame_rate
            if( instrument == synth.DRUMS):
                if(duration < 1000):
                    N= math.ceil(duration/2)
                else:
                    N=1000
                f_s, data= wavfile.read( self.GetDrumsData(duration,intensity) )
                t_h = np.linspace(0,data.size,data.size)
                window = MakeWindow(N)
                stretch_factor = (duration)/t_h[-1]
                stretch_func = stretch_factor*t_h
                note= o.OLA(data,window,stretch_func,0.01)
            else:
                if( instrument == synth.GUITAR):
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
                
                elif( instrument == synth.CORN_ANGLAIS):
                    fmin = 165 #Frecuencia minima de un semitono de corn anglais
                    if( pitch < midi.E_3):
                        if( duration > int(0.875*self.frame_rate)): #Uso las muestras de 1.5 seg para duraciones mayores a 0.875 seg
                            forte_sample= COR_ANGLAIS_PATH+"\E3_15_fortissimo.wav"
                            piano_sample= COR_ANGLAIS_PATH+"\E3_15_piano.wav"
                        else:
                            forte_sample= COR_ANGLAIS_PATH+"\E3_025_mezzo_forte.wav"
                            piano_sample= COR_ANGLAIS_PATH+"\E3_025_piano.wav"
                        freq_factor = 1
                    elif( pitch > midi.C_6):
                        if( duration > int(0.625*self.frame_rate)):
                            forte_sample = COR_ANGLAIS_PATH+"\B5_1_forte.wav"
                            piano_sample = COR_ANGLAIS_PATH+"\B5_1_mezzo-piano.wav"
                        else:
                            forte_sample = COR_ANGLAIS_PATH+"\B5_025_forte.wav"
                            COR_ANGLAIS_PATH+"\B5_025_mezzo-piano.wav"
                        freq_factor = 1.059463094
                    else:
                        forte_sample_1_5,piano_sample_1_5,forte_sample_0_25,piano_sample_0_25,freq_factor = self.corn_dict[pitch]
                        if( duration > int(0.875*self.frame_rate) ):
                            forte_sample = forte_sample_1_5
                            piano_sample = piano_sample_1_5
                        else:
                            forte_sample = forte_sample_0_25
                            piano_sample = piano_sample_0_25

                    if intensity >= MIN_FORTE_INTENSITY: #cargo nota con velocidad alta
                        f_s, data= wavfile.read(forte_sample)
                    else: #cargo nota con velocidad baja
                        f_s, data= wavfile.read(piano_sample)
                pitch_corrected_data = ResampleArray(data,f_s,int(f_s/freq_factor),SameTimeLimit=False)
                if((duration/desired_fs)>(1/fmin)):
                    N= 2*int(desired_fs/fmin)
                else:
                    N= int(0.1*duration) #La duracion es menor que el periodo undamental minimo
                t_h = np.linspace(0,pitch_corrected_data.size,pitch_corrected_data.size)
                window = MakeWindow(N)
                stretch_factor = (duration)/t_h[-1]
                stretch_func = stretch_factor*t_h
                note= ph.PhVocoder(pitch_corrected_data,window,stretch_func,int(0.1*N))

            #Normalizo el vector
            note_max_pos = np.max(note)
            note_max_neg = np.min(note)
            if( note_max_pos != 0)or( note_max_neg != 0):
                if( abs(note_max_pos) > abs(note_max_neg)):
                    note = note/abs(note_max_pos)
                else:
                    note = note/abs(note_max_neg)
            self.note_dict.setdefault( (pitch,duration,intensity),note)
            
        else:
            note = self.note_dict.get((pitch,duration,intensity))
        return note

    def SetInstrument(self,inst):
        self.instrument = inst
    def GetDrumsData(self,duration,intensity):
        duration_in_time = duration/self.frame_rate
        sample=""
        if duration_in_time <=0.625:
            if intensity <= MIN_FORTE_INTENSITY:
                sample = DRUMS_PATH + "\\025_mezzo-forte_mallet.wav"
            else:
                sample = DRUMS_PATH + "\\025_forte_mallet.wav"
        elif duration_in_time <= 1.25:
            if intensity <= int(MIN_FORTE_INTENSITY/2):
                sample = DRUMS_PATH + "\\1_pianissimo_struck-singly.wav"
            elif intensity <= MIN_FORTE_INTENSITY:
                sample = DRUMS_PATH + "\\1_mezzo-piano_struck-singly.wav"
            else:
                sample = DRUMS_PATH + "\\1_fortissimo_struck-singly.wav"
        elif duration_in_time <= 4.25:
            if intensity <= MIN_FORTE_INTENSITY:
                sample = DRUMS_PATH + "\\15_pianissimo_rhythm.wav"
            else:
                sample = DRUMS_PATH + "\\15_mezzo-piano_rhythm.wav"
        elif duration_in_time <= 11:
            sample = DRUMS_PATH + ".\\7_mezzo-forte.wav"
        else:
            sample = DRUMS_PATH + ".\\150_mezzo-piano_rhythm"
        return sample