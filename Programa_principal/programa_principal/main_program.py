from synth import Synthesizer
from Fm_synth import FmSynthesizer
import midi
import time
import struct, math
import wav_gen
from additiveSynthesis import additiveSynthesis
import SampleSynthesizer as sammy
import karplus
import synth
import GraphSpectrogram as gs
import os

MIDIS_PATH = ".\\ArchivosMIDI\\"

def avg(prev_data, new_data, avg_count):
    if len(prev_data) == 0:
        prev_data = [0]*len(new_data)
    elif avg_count == 0:
        prev_data = [0]*len(new_data)
    elif len(prev_data) != len(new_data):
        print('Cuidado! Distintas dimensiones!')
        print('len(prev_data)=' + str(len(prev_data)))
        print('len(new_data)=' + str(len(new_data)))
        if len(newer_data) > len(prev_data):
            prev_data += [0]*(len(newer_data) - len(prev_data))
        else:
            new_data += [0]*(len(prev_data) - len(newer_data))

    for i in range(len(new_data)):
        prev_data[i] = (prev_data[i]*avg_count+new_data[i])/(avg_count + 1)

    return prev_data


def not_meta_track(track):
    t = track
    for ev in t:
        if ev.name == 'Note On':
            return True
    return False
def isfloat(value):
      try:
        float(value)
        return True
      except ValueError:
        return False

def IsValidNumber(arg):
    if( isfloat(arg)): #valido el argumento
        arg_f=float(arg)
        if(arg_f<=0):
            return ( "El numero ingresado debe ser positivo\n")
        elif (arg_f==float("inf"))or(arg_f>=10e9):
            return ("El numero ingresado debe tener un valor finito\n")

    else:
        return ("Error de sintaxis")

    return "Ok" #El numero parece ser valido

def GetSelectedMidi():
    valid = False
    print("Bienvenido, este es un programa sintetizador de Audio en fomrato wav a partir de archivos MIDI.\n")
    print("El programa comienza con la eleccion del archivo midi que se desea sintetizar.\n")
    print("Luego de elegir el midi se presentaran las tracks que se encuentran dentro del mismo y\n")
    print("debe elegirse el metodo de sintesis deseado y que instrumento se desea utilizar para cada track.\n")
    print("\n A continuacion se presentan los archivos MIDI disponibles para sintetizar:\n")
    i=0
    midi_dict = dict()
    for file in os.listdir(MIDIS_PATH):
        i +=1 
        if file.endswith(".mid"):
            print(str(i)+')'+file)
            midi_dict[i] = file
    while not valid:
        num_str = input("Por favor seleccione el MIDI deseado ingresando el numero previo al nombre\n")
        result_str = IsValidNumber(num_str)
        if(result_str =='Ok'):
            num = int(num_str)
            if (num in midi_dict):
                valid =True
                return midi_dict[num]
        else:
            valid = False
            print(result_str)

def GetInstrument(synth_string):
    valid=False
    print("\Ahora por favor seleccione el instrumento deseado para el track actual:\n")
    if(synth_string == 'Aditiva'):
        add_inst_dict =dict([
            (1,synth.GUITAR),
            (2,synth.TRUMPET),
            (3,synth.VIOLIN),
            (4,synth.SAXO)
            ])
        while(not valid):
            inst_num_str = input("1)Guitarra\t 2)Trompeta\t 3)Violin\t 4)Saxo\n")
            result_str = IsValidNumber(inst_num_str)
            if(result_str =='Ok'):
                inst_num = int(inst_num_str)
                if (inst_num in add_inst_dict):
                    return add_inst_dict[inst_num]
            else:
                print(result_str)

    elif(synth_string == 'FM'):
        fm_inst_dict =dict([
            (1,synth.BELL),
            (2,synth.TRUMPET),
            (3,synth.CLARINET)
            ])
        while(not valid):
            inst_num_str = input("1)Campana\t 2)Trompeta\t 3)Clarinete\n")
            result_str = IsValidNumber(inst_num_str)
            if(result_str =='Ok'):
                inst_num = int(inst_num_str)
                if (inst_num in fm_inst_dict):
                    return fm_inst_dict[inst_num]
            else:
                print(result_str)
    elif(synth_string == 'Karplus'):
        karplus_inst_dict =dict([
            (1,synth.GUITAR),
            (2,synth.DRUMS),
            (3,synth.ELECTRIC_GUITAR)
            ])
        while(not valid):
            inst_num_str = input("1)Guitarra acustica\t 2)Tambores\t 3)Guitarra electrica\n")
            result_str = IsValidNumber(inst_num_str)
            if(result_str =='Ok'):
                inst_num = int(inst_num_str)
                if (inst_num in karplus_inst_dict):
                    return karplus_inst_dict[inst_num]
            else:
                print(result_str)
    elif(synth_string == 'Muestras'):
        sample_inst_dict =dict([
            (1,synth.GUITAR),
            (2,synth.TRUMPET),
            (3,synth.VIOLIN),
            (4,synth.CORN_ANGLAIS),
            (5,synth.DRUMS)
            ])
        while(not valid):
            inst_num_str = input("1)Guitarra\t 2)Trompeta\t 3)Violin\t 4)Corn anglais\t 5)Bombo\n")
            result_str = IsValidNumber(inst_num_str)
            if(result_str =='Ok'):
                inst_num = int(inst_num_str)
                if (inst_num in sample_inst_dict):
                    return sample_inst_dict[inst_num]
            else:
                print(result_str)
def GetSynthClass(synth_string,resolution):
    if(synth_string == 'Aditiva'):
        return additiveSynthesis(resolution)
    elif(synth_string == 'FM'):
        return FmSynthesizer(resolution)
    elif(synth_string == 'Karplus'):
        return karplus.KarplusSynthesizer(pattern.resolution)
    elif(synth_string == 'Muestras'):
        return sammy.SampleSynthesizer(resolution)



def GetSynthAndInsts(tracks,resolution):
    synth_options_dict = dict([
        (1,'Aditiva'),
        (2,'FM'),
        (3,'Karplus'),
        (4,'Muestras')
        ])
    synths = []
    insts = []
    print("\n A continuacion se presentara cada track relevante del MIDI:\n")
    i=1
    for t in tracks:
        valid=False
        info=''
        if( not_meta_track(t)):
            for ev in t:
                if ev.name == 'Track Name':
                    info += ev.text
            print("Track number "+str(i))
            print("\nText info of Track: "+info)
            while(not valid):
                print("\nPor favor seleccione el metodo de sintesis que desea para este track(ingresar el numero previo al nombre):\n")
                synth_sel_str = input("1)Aditiva\t 2)FM\t 3)Basada en modelos fisicos\t 4)Basada en muestras\n")
                result_str = IsValidNumber(synth_sel_str)
                if(result_str =='Ok'):
                    synth_sel = int(synth_sel_str)
                    if (synth_sel in synth_options_dict):
                        valid =True
                        synths.append(GetSynthClass(synth_options_dict[synth_sel],resolution))
                        insts.append(GetInstrument(synth_options_dict[synth_sel]))
        else:
            synths.append(sammy.SampleSynthesizer(resolution))
            insts.append(synth.CORN_ANGLAIS)
    return synths,insts

waver = wav_gen.WaveManagement()
selected_midi = GetSelectedMidi()
pattern = midi.read_midifile(MIDIS_PATH+selected_midi)
trks = [pattern[i] for i in range(len(pattern))]
synths,insts = GetSynthAndInsts(trks,pattern.resolution)



synths_trks_insts = [(synths[i], trks[i], insts[i]) for i in range(len(trks))]

start = time.time()

finished = False
data = []
j = 0

# for format 1 .mid files
#if synths[0].get_tempo_map(trks[0]) is not None:
if not not_meta_track(trks[0]) and synths[0].get_tempo_map(trks[0]) is not None:
    # new_tempo_map should be None if the first meta track does not contain tempo information
    new_tempo_map = synths[0].get_tempo_map(trks[0])
    for k in range(1, len(synths_trks_insts)):
        s, t, i = synths_trks_insts[k]
        s.set_tempo_map(new_tempo_map)
    #synths_trks_insts = synths_trks_insts[1:]

iterable_list = list(range(len(synths_trks_insts)))

# The tracks that only contain MetaEvents will not be taken into account when filling the .wav !
iterable_list[:] = [x for x in iterable_list if not_meta_track(trks[x])]
finished = [True]*len(synths_trks_insts) #Lista donde se va marcando los tracks que se terminaron
for i in iterable_list:
    finished[i] = False #Actualizo cuales son los tracks que faltan terminar.

while not all(finished):
    for k in iterable_list:
        s, t, i = synths_trks_insts[k]
        newer_data, finished[k] = s.synthesize(t, i, j == 0, 70000)
        if(finished[k]): #Si el track k-esimo termino lo saca de la lista
            iterable_list.remove(k)
        # print('j='+str(j)+'. Tempo map' + str(k) + str(s.tempo_map))
        data = avg(prev_data=data, new_data=newer_data, avg_count=k)
    waver.generate_wav(all(finished), data, n_channels=1, sample_width=2, frame_rate=44100, file_name='Track'+str(j)+'.wav')
    j += 1

end = time.time()

print('Tardo ' + str(int(end-start)) + ' segundos en sintetizar todo!')
del synths_trks_insts
gs.GraphSpectrogram(file_name='.\\Track0'+'.wav')
