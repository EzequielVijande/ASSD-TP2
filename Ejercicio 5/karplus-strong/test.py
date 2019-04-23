from random import random
from array import array
import wave
import matplotlib.pyplot as plt
import numpy as np
import math

SampleRate = 44100
DAMPING = 0.996

notes = [391, 440, 489, 521, 586, 660, 734, 782]
duration = [16, 4, 16, 4, 64, 16, 4, 8]

nchannels, swdth, frame_rate, nframes = 1, 2, 44100, 44100

max_val = 32767


def Generate(f, nsamples):
    N = SampleRate // f

    buf = [random() - 0.5 for i in range(N)]
    samples = []

    bufSize = len(buf)

    for i in range(nsamples):
        samples.append(buf[0])
        avg = DAMPING * 0.5 * (buf[0] + buf[1])
        buf.append(avg)
        buf.pop(0)



#    plt.plot(buf)
#    plt.show()

    tempbuf = [int(x * max_val) for x in samples]

    data = array('h', tempbuf).tobytes()
    file.writeframes(data)


file = wave.open('sim.wav', 'wb')
file.setparams((nchannels, swdth, frame_rate, nframes, 'NONE', 'nonecompressed'))
for i in range(len(notes)):
    Generate(notes[i], 44100 // duration[i])
file.close()