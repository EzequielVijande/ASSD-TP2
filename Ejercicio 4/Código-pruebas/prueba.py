from synth import Synthesizer
from Fm_synth import FmSynthesizer
import midi
import time
import struct, math
import wav_gen

waver = wav_gen.WaveManagement()

synth = FmSynthesizer(192)
func = synth.create_note_array

pitches = [(110, 220), (220, 440), (110, 220), (110, 220), (250, 350), (250, 350)]
taus = [2, 2, 12, 0.3, 2, 1]
times = [6, 6, 3, 3, 5, 5]          # seconds
fs = 11025
amount_of_ns = [int(t*fs) for t in times]
taus = [int(tau*fs) for tau in taus]
velocity = 127
inst = 112

for i in range(len(pitches)):
    # (pitch, amount_of_ns: int, velocity, instrument :int, tau)
    notes = func(pitch=pitches[i], amount_of_ns=amount_of_ns[i], velocity=velocity, instrument=inst, tau=taus[i])
    waver.generate_wav(True, notes, n_channels=1, sample_width=2, frame_rate=fs, file_name='TrackBell'+str(i)+'.wav')



