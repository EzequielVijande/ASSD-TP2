from synth import Synthesizer
from Fm_synth import FmSynthesizer
import midi
import wave
import struct
import time

# para la manera mas eficiente!
# import numpy as np
# from scipy.io.wavfile import read
# from pydub import AudioSegment
# from pydub.playback import play
# import wave, struct, math

pattern = midi.read_midifile(".\ArchivosMIDI\Super Mario 64 - Bob-Omb Battlefield.mid")
trks = [pattern[i] for i in range(1, len(pattern))]
synthe = FmSynthesizer(pattern.resolution)
synthe.set_create_notes_callback(synthe.create_note_array)

synths = [synthe for i in range(1, len(pattern))]
insts = [2 for i in range(1, len(pattern))]

#     def synthesize(self, track: midi.Track, instrument: int, name: str):
synths_trks_insts = [(synths[i], trks[i], insts[i]) for i in range(len(trks))]
start = time.time()
wavs = []
j = 1
for s, t, i in synths_trks_insts:
    wavs.append(s.synthesize(t, i, 'Name' + str(j) + '.wav'))
    j += 1
end = time.time()

print('Tardo ' + str(int(end-start)) + ' segundos en sintetizar todo!')

#for j in range(1, 6):
#    wavs.append('Name' + str(j) + '.wav')

avg = 0
final_wav = wave.open('Final.wav', 'wb')
final_wav.setnchannels(2)
final_wav.setframerate(44100)
final_wav.setsampwidth(2)
start = time.time()

data = []
wav_files = []
for i in range(len(wavs)):
    wav_files.append(wave.open(wavs[i], 'rb'))
for j in range(wave.open(wavs[0], 'rb').getnframes()):
    for i in range(len(wavs)):
        avg += int(*struct.unpack('h', wav_files[i].readframes(1)))
        if i == len(wavs)-1:
            data.append(struct.pack('h', int(avg/len(wavs))))
            avg = 0
            print(len(data))
            if len(data) > 70000:
                final_wav.writeframes(b''.join(data))
                data = []
                print('Escribi')


end = time.time()
print('Tardo ' + str(int(end-start)) + ' segundos en sintetizar todo!')
