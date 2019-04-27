import math
import midi
import synth


class FmSynthesizer(synth.Synthesizer):
    def __init__(self, resolution):
        self.set_create_notes_callback(self.create_note_array)
        super(FmSynthesizer, self).__init__(resolution)

    # https://en.wikipedia.org/wiki/MIDI_tuning_standard#Frequency_values
    def create_note_array(self, pitch, amount_of_ns: int, velocity, instrument: int):

        freq = 2 ** ((pitch - 69) / 12) * 440
        notes = []

        phim = -math.pi / 2
        phic = phim
        fc = freq * 3
        fm = freq * 4
        I = []
        for i in range(amount_of_ns):
            I.append(4)
            notes.append((velocity/127)*math.cos(2 * math.pi * fc * i / self.frame_rate + I[i] * math.cos(2 * math.pi * fm * i / self.frame_rate + phim) + phic))
        return notes



