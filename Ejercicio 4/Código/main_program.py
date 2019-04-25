from synth import Synthesizer
from Fm_synth import FmSynthesizer
import midi
import time
import struct, math
import wav_gen


def avg(prev_data, new_data, avg_count):
    if avg_count == 0:
        prev_data = [0]*len(new_data)
    elif len(prev_data) != len(new_data):
        print('Cuidado! Distintas dimensiones!')
        print('len(prev_data)=' + str(len(prev_data)))
        print('len(new_data)=' + str(len(new_data)))

    for i in range(len(new_data)):
        prev_data[i] = (prev_data[i]*avg_count+new_data[i])/(avg_count + 1)

    return prev_data


waver = wav_gen.WaveManagement()
pattern = midi.read_midifile(".\pirates.mid")
trks = [pattern[i] for i in range(1, len(pattern))]

synths = [FmSynthesizer(pattern.resolution) for i in range(1, len(pattern))]
for s in synths:
    s.set_create_notes_callback(s.create_note_array)

insts = [2 for i in range(1, len(pattern))]

synths_trks_insts = [(synths[i], trks[i], insts[i]) for i in range(len(trks))]

start = time.time()

finished = False
data = []
j = 0
while not finished:

    for k in range(len(synths_trks_insts)):
        s, t, i = synths_trks_insts[k]
        # print(t)
        newer_data, finished = s.synthesize(t, i, j == 0)
        data = avg(prev_data=data, new_data=newer_data, avg_count=k)
    waver.generate_wav(finished, data, n_channels=1, sample_width=2, frame_rate=44100, file_name='Track'+str(j)+'.wav')
    print(j)
    j += 1

end = time.time()

print('Tardo ' + str(int(end-start)) + ' segundos en sintetizar todo!')
