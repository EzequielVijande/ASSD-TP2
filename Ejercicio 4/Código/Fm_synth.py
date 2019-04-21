import math
import midi
import synth


class FmSynthesizer(synth.Synthesizer):
    def __init__(self):
        self.set_create_notes_callback(self.create_note_array)
        super(FmSynthesizer, self).__init__()

# https://en.wikipedia.org/wiki/MIDI_tuning_standard#Frequency_values
    def create_note_array(self, pitch, amount_of_ns: int):
        notes = []
        freq = 2**((pitch-69)/12)*440
        phim = -math.pi / 2
        phic = phim
        fc = freq*3
        fm = freq*4
        I = []
        for i in range(amount_of_ns):
            # notes.append(math.sin(2*math.pi*freq*i/self.frame_rate))
            I.append(4)
            notes.append(math.cos(2*math.pi*fc*i/self.frame_rate + I[i]*math.cos(2*math.pi*fm*i/self.frame_rate+phim)+phic))
        return notes


# pruebas
synther = FmSynthesizer()
synther.set_create_notes_callback(synther.create_note_array)
pattern = midi.read_midifile(".\ArchivosMIDI\Super Mario 64 - Bob-Omb Battlefield.mid")
synther.set_resolution(pattern.resolution)
# for trk in pattern:
#   synth.synthesize(trk)
synther.synthesize(pattern[1])
