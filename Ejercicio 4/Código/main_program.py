from .synth import Synthesizer
import midi
import wave
import struct
# from .wav_gen import WaveManagement

pattern = None
assert isinstance(pattern, midi.Pattern)
trks = [pattern[i] for i in range(len(pattern))]
synths = []
insts = []

synths_trks_insts = [(synths[i], trks[i], insts[i]) for i in range(len(trks))]

wavs = []
for s, t, i in synths_trks_insts:
    assert isinstance(s, Synthesizer)
    wavs.append(s.synthesize(t, i))

avg = 0
final_wav = wave.open('Final.wav', 'wb')

for j in range(wave.open(wavs[0], 'rb').getnframes()):
    for i in range(len(wavs)):
        wav_file = wave.open(wavs[i], 'rb')
        # this could be dependable on the number of bytes for the codification of my .wav files
        # (haven t checked yet)
        # if so, the following line should be replaced with
        # avg += wav_file.readframes(WaveManagement.number_of_bytes_codification)
        avg += wav_file.readframes(1)
        # the joining process could be done for more than 2 bytes at a time but we should use a auxiliary list to do so!
        if i == len(wavs)-1:
            final_wav.writeframes(b''.join(struct.pack('h', int(avg/len(wavs)))))
