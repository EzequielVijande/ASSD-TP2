from synth import Synthesizer
from Fm_synth import FmSynthesizer
import midi
import time
import struct, math
import wav_gen
import SampleSynthesizer as sammy
import synth

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


def not_meta_track(synth_trk_inst):
    s, t, i = synth_trk_inst
    for ev in t:
        if ev.name == 'Note On':
            return True
    return False
    # return len(s.synthesize(t, i, True, 1000)[0]) != 0


waver = wav_gen.WaveManagement()
pattern = midi.read_midifile(".\ArchivosMIDI\Super Mario 64 - Bob-Omb Battlefield.mid")
# pattern = midi.read_midifile(".\Super Mario 64 - Bob-Omb Battlefield.mid")
trks = [pattern[i] for i in range(len(pattern))]

synths = [sammy.SampleSynthesizer(pattern.resolution) for i in range(len(pattern))]
for s in synths:
    s.set_create_notes_callback(s.create_notes_callback)

insts = [synth.CORN_ANGLAIS]*len(trks)

synths_trks_insts = [(synths[i], trks[i], insts[i]) for i in range(len(trks))]

start = time.time()

finished = False
data = []
j = 0

# for format 1 .mid files
if synths[0].get_tempo_map(trks[0]) is not None:
    # new_tempo_map should be None if the first meta track does not contain tempo information
    new_tempo_map = synths[0].get_tempo_map(trks[0])
    print(new_tempo_map)
    for k in range(1, len(synths_trks_insts)):
        s, t, i = synths_trks_insts[k]
        s.set_tempo_map(new_tempo_map)
    synths_trks_insts = synths_trks_insts[1:]

iterable_list = list(range(len(synths_trks_insts)))

# The tracks that only contain MetaEvents will not be taken into account when filling the .wav !
iterable_list[:] = [x for x in iterable_list if not_meta_track(synths_trks_insts[x])]


while not finished:
    for k in iterable_list:
        s, t, i = synths_trks_insts[k]
        newer_data, finished = s.synthesize(t, i, j == 0, 70000)
        # print('j='+str(j)+'. Tempo map' + str(k) + str(s.tempo_map))
        data = avg(prev_data=data, new_data=newer_data, avg_count=k)
    waver.generate_wav(finished, data, n_channels=1, sample_width=2, frame_rate=44100, file_name='Track'+str(j)+'.wav')
    j += 1

end = time.time()

print('Tardo ' + str(int(end-start)) + ' segundos en sintetizar todo!')

