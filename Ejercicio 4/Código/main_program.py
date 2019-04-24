from synth import Synthesizer
import trkcontrol
from Fm_synth import FmSynthesizer
import midi
import time
import wave, struct, math
import wav_gen


def avg(data, new_data):
    pass

pattern = midi.read_midifile(".\Super Mario 64 - Bob-Omb Battlefield.mid")
processor = trkcontrol.TrackProcessor()
trks = [processor.process_track(pattern[i]) for i in range(1, len(pattern))]
synthe = FmSynthesizer(pattern.resolution)
synthe.set_create_notes_callback(synthe.create_note_array)

synths = [synthe for i in range(1, len(pattern))]
insts = [2 for i in range(1, len(pattern))]

#     def synthesize(self, track: midi.Track, instrument: int, name: str):
synths_trks_insts = [(synths[i], trks[i], insts[i]) for i in range(len(trks))]
start = time.time()

# manager used to generate the .wav file
wav_manager = wav_gen.WaveManagement()

j = 0
finished = False
while not finished:
    data = []
    i = 0
    for s, t, i in synths_trks_insts:
        new_data, finished = s.synthesize(t, i, 100000, i == 0)
        avg(data, new_data)
        i += 1
    wav_manager.generate_wav(finished, data, 1, sample_width=2, frame_rate=44100, file_name='FINAL.wav')

end = time.time()

print('Tardo ' + str(int(end-start)) + ' segundos en sintetizar todo!')
