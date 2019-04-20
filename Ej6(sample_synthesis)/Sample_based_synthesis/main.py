import wave
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import SampleSynthesizer as sam
import midi


f_s= int(50e3)
duration= 2
velocity = 80
note = sam.MakeNote(midi.C_3,duration,velocity,f_s)
note = note.astype('int16')
ax1=plt.subplot(1, 1, 1)
t = np.linspace(0,duration,note.size)
plt.plot(t,note)
plt.show()
wavfile.write("nota.wav", f_s, note)

