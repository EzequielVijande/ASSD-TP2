import wave
from scipy.io import wavfile
import math
import numpy as np
import struct


# https://soledadpenades.com/posts/2009/fastest-way-to-generate-wav-files-in-python-using-the-wave-module/
def generate_wav(data: list, n_channels: int = 1, sample_width=2, frame_rate=44100, file_name='NEW_WAV.wav'):
    new_wav_file = wave.open(file_name, 'wb')
    new_wav_file.setparams((n_channels, sample_width, frame_rate, len(data), 'NONE', 'not compressed'))
    translated_data = []

    for d in data:
        translated_data.append(struct.pack('h', int(d)))

    new_wav_file.writeframes(b''.join(translated_data))


amp = 20000.0

my_data = []
f_rate = 44100
for i in range(f_rate*5):
    my_data.append(math.cos(2*math.pi*400*i/f_rate)*amp/2)

generate_wav(my_data, n_channels=1, sample_width=2, frame_rate=f_rate, file_name='KEASE.wav')

