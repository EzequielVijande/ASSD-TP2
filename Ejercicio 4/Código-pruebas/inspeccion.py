from pydub import AudioSegment
import numpy as np
from matplotlib import pyplot as pl
from os import listdir
from os.path import isfile, join
from scipy import signal

mypath = '.\\samples\\audio'
mypath = '.\\samples'

def get_file_names():
    return [f for f in listdir(mypath) if isfile(join(mypath, f))]


def read_mp3_files(file_names):
    AudioSegment.converter = "C:\\FFmpeg\\bin\\ffmpeg.exe"
    AudioSegment.ffmpeg = "C:\\FFmpeg\\bin\\\\ffmpeg.exe"
    AudioSegment.ffprobe = "C:\\FFmpeg\\bin\\\\ffprobe.exe"
    name_counter = 0
    for name in file_names:

        sound = AudioSegment.from_mp3(mypath + '\\'+name)

        raw_data = sound.raw_data
        sample_rate = sound.frame_rate
        sample_size = sound.sample_width
        # channels = sound.channels

        data = np.frombuffer(raw_data, dtype=np.int16)
        manage_plot(data, name)
        print('Listo archivo\t' + str(name_counter) + ' / ' + str(len(file_names)))
        name_counter += 1


def manage_plot(plot_info, file_name):
    print(file_name)
    pl.plot(np.arange(len(plot_info))/44100, plot_info)
    pl.xlabel('Tiempo - n')
    pl.ylabel('Amplitud - A')
    pl.grid()
    # pl.savefig(file_name + '.png')
    # pl.clf()
    pl.show()

    # Para el espectograma
    # f, t, Sxx = signal.spectrogram(plot_info, 44100)
    # pl.pcolormesh(t, f, Sxx)
    # pl.title(file_name)
    # pl.ylabel('Frequency [Hz]')
    # pl.xlabel('Time [sec]')
    # pl.show()

read_mp3_files(get_file_names())

