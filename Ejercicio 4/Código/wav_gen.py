import wave
import math
import struct

# https://soledadpenades.com/posts/2009/fastest-way-to-generate-wav-files-in-python-using-the-wave-module/
def generate_wav(data: list, n_channels: int = 1, sample_width=2, frame_rate=44100, file_name='NEW_WAV.wav'):
    """generate_wav generates a new .wav file based on the input data.
The amplitude of each data sample should be a float belonging to the interval [-1,1],
where 1 will be the maximum representable number on the wav file."""

    new_wav_file = wave.open(file_name, 'wb')
    new_wav_file.setparams((n_channels, sample_width, frame_rate, len(data), 'NONE', 'not compressed'))
    translated_data = []

    # https://docs.python.org/2/library/struct.html#struct-format-strings
    # h : 2 bytes -> 2^15-1 =32767, maximum amplitude
    # i : 4 bytes
    for d in data:
        translated_data.append(struct.pack('h', int(d*(2**15-1))))

    new_wav_file.writeframes(b''.join(translated_data))


my_data = []
f_rate = 44100          # standard frame rate for audio
for i in range(f_rate*5):
    my_data.append(math.cos(2*math.pi*400*i/f_rate))

generate_wav(my_data, n_channels=1, sample_width=2, frame_rate=f_rate, file_name='KEASE.wav')

