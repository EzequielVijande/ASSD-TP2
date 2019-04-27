import math
import midi
import synth


class FmSynthesizer(synth.Synthesizer):
    def __init__(self, resolution):
        self.set_create_notes_callback(self.create_note_array)
        super(FmSynthesizer, self).__init__(resolution)

    # http: // fmslogo.sourceforge.net / manual / midi - instrument.html

    # https://en.wikipedia.org/wiki/MIDI_tuning_standard#Frequency_values
    def create_note_array(self, pitch, amount_of_ns: int, velocity, instrument :int):
        freq = 2 ** ((pitch - 69) / 12) * 440

        if instrument == 112 or instrument == 'Tinkle Bell':
            return self.synthesize_bell(freq, amount_of_ns, velocity, instrument)
        elif instrument == 71 or instrument == 'Clarinet':
            return self.synthesize_clarinet(freq, amount_of_ns, velocity,instrument)
        else:
            notes = []
            freq = 2 ** ((pitch - 69) / 12) * 440
            phim = -math.pi / 2
            phic = phim
            fc = freq * 3
            fm = freq * 4
            I = []
            for i in range(amount_of_ns):
                I.append(4)
                notes.append((velocity/127)*math.cos(2 * math.pi * fc * i / self.frame_rate + I[i] * math.cos(
                    2 * math.pi * fm * i / self.frame_rate + phim) + phic))
            return notes

    def synthesize_bell(self, freq: float, amount_of_ns: int, velocity, instrument: int):
        amount_of_ns *=2
        notes = []
        #fc = freq * 3
        #fm = freq * 4
        fc = 110
        fm = 220
        phim = -math.pi / 2
        phic = phim
        tau = 100000
        Io = 10
        for t in range(amount_of_ns):
            A = math.e**(-t/tau)
            I = Io*math.e**(-t/tau)

            notes.append(A* math.cos(2 * math.pi * fc * t / self.frame_rate + I * math.cos(
                2 * math.pi * fm * t / self.frame_rate + phim) + phic))

        return notes

    def synthesize_clarinet(self, freq: float, amount_of_ns: int, velocity, instrument: int):
        pass

