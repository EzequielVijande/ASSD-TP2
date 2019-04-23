import math
import midi
import synth


class FmSynthesizer(synth.Synthesizer):
    def __init__(self, resolution):
        self.set_create_notes_callback(self.create_note_array)
        super(FmSynthesizer, self).__init__(resolution)

    # https://en.wikipedia.org/wiki/MIDI_tuning_standard#Frequency_values
    def create_note_array(self, pitch, amount_of_ns: int, velocity, instrument :int):
        notes = []
        freq = 2 ** ((pitch - 69) / 12) * 440
        phim = -math.pi / 2
        phic = phim
        fc = freq * 3
        fm = freq * 4
        I = []
        for i in range(amount_of_ns):
            I.append(4)
            notes.append(math.cos(2 * math.pi * fc * i / self.frame_rate + I[i] * math.cos(
                2 * math.pi * fm * i / self.frame_rate + phim) + phic))
        return notes


# pruebas
# pattern = midi.read_midifile(".\ArchivosMIDI\Super Mario 64 - Bob-Omb Battlefield.mid")
# synther = FmSynthesizer(pattern.resolution)
# synther.set_create_notes_callback(synther.create_note_array)
# for j in range(1, len(pattern)):
#    synther.synthesize(pattern[j], j, 'Track'+str(j)+'.wav')

