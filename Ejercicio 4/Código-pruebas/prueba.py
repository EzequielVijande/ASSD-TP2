from synth import Synthesizer
from Fm_synth import FmSynthesizer
import midi
import time
import struct, math
import wav_gen
from matplotlib import pyplot as pl
from scipy import signal as sig
import numpy as np
import pandas as pd
import scipy

from scipy import signal

waver = wav_gen.WaveManagement()

synth = FmSynthesizer(192)
func = synth.create_note_array

# amount_of_ns = 17500      # clarinete
amount_of_ns = 200000      # campana
# amount_of_ns = 27000        # trompeta
velocity = 127
# inst = 71     # clarinete
inst = 112    # campana
# inst = 56      # trompeta
# pitch = 57    # trompeta y clarinete
pitch = 69      # campana
notes = func(pitch=pitch, amount_of_ns=amount_of_ns, velocity=velocity, instrument=inst)
# pl.plot(list(range(len(notes))), [n*4500 for n in notes])       # clarinete
pl.plot(list(range(len(notes))), [n*680 for n in notes])      # campana
# pl.plot(list(range(len(notes))), [n*6200 for n in notes])     # trompeta
pl.show()
waver.generate_wav(finished=True, data=notes, n_channels=1, sample_width=2, frame_rate=44100, file_name='NEW_WAV.wav')

# Para el espectograma!!!

# notes = np.asarray(notes)
# f, t, Sxx = signal.spectrogram(notes, 44100)
# pl.pcolormesh(t, f, Sxx)
# pl.title('A3, Nota sintetizada')
# pl.ylabel('Frequency [Hz]')
# pl.xlabel('Time [sec]')
# pl.show()

