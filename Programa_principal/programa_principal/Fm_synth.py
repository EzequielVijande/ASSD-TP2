import math
import midi
import synth
import wav_gen
import numpy as np


class FmSynthesizer(synth.Synthesizer):
    def __init__(self, resolution):
        self.set_create_notes_callback(self.create_note_array)
        super(FmSynthesizer, self).__init__(resolution)

    # http: // fmslogo.sourceforge.net / manual / midi - instrument.html

    # https://en.wikipedia.org/wiki/MIDI_tuning_standard#Frequency_values
    def create_note_array(self, pitch: int, amount_of_ns: int, velocity, instrument: int):

        if instrument == 112 or instrument == synth.BELL:
            return self.synthesize_bell(pitch, amount_of_ns, velocity)
        elif instrument == 71 or instrument == synth.CLARINET:
            return self.synthesize_clarinet(pitch, amount_of_ns, velocity)
        elif instrument == 56 or instrument == synth.TRUMPET:
            return self.synthesize_trumpet(pitch, amount_of_ns, velocity)
        else:
            return self.synthesize_clarinet(pitch, amount_of_ns, velocity)


    def synthesize_bell(self, pitch: int, amount_of_ns: int, velocity):
        freq = 2 ** ((pitch - 69) / 12) * 440
        num = 6
        fc = freq
        N2 = 1.7
        fm = fc*N2

        tau = -1/math.log(80/680, math.e)*self.frame_rate*10/5
        notes = []

        io = 0.5
        for t in range(amount_of_ns):
            a = math.e**(-t/tau)*velocity/127
            i = -io*math.e**(-t/tau)
            notes.append(a * math.sin(2 * math.pi * fc * t / self.frame_rate + i * math.sin(
                2 * math.pi * fm * t / self.frame_rate)))

        return notes

    def synthesize_clarinet(self, pitch: int, amount_of_ns: int, velocity):
        # c/m = N1/N2
        # fo = c/N1 = m/N2
        # N2 = 1, the spectrum contains all the harmonics
        # when N2 is an even number, the spectrum contains only odd number harmonics.
        # Clarinets often contain odd numbered harmonics.
        # The assumption for the wood instruments are:
        # 1) The frequencies are in the harmonic series and the spectrum contains only odd numbered harmonics
        # 2) The higher harmonics may increase significantly with the attack.
        # JohnChowning
        freq = 2 ** ((pitch - 69) / 12) * 440
        N1 = 1
        fc = freq * N1
        N2 = 4
        fm = freq * N2 + 0.3
        notes = []
        # duration of the attack in seconds:
        attack_ns = int(0.0901 * self.frame_rate)
        # duration of the decay in seconds
        decay_ns = int(0.074 * self.frame_rate)

        # duration of the release in seconds: 0.011
        release_ns = int(0.11 * self.frame_rate)

        if amount_of_ns < (attack_ns + release_ns + decay_ns):
            # duration of the attack / total duration of the note : 0.1346
            attack_ns = int(amount_of_ns*0.1346*2)
            # post_attack_ns = int(amount_of_ns*0.057)
            decay_ns = int(amount_of_ns*0.18)
            # duration of the release / total duration of the note : 0.32
            release_ns = int(amount_of_ns*0.32)

        sustain_ns = amount_of_ns - release_ns - decay_ns - attack_ns
        sustain_level = 0.71
        max_value = 0.98
        attack_constant = attack_ns / math.log(max_value + 1, math.e)
        release_constant = -release_ns / math.log(1/32, math.e)
        decay_constant = -decay_ns / math.log(sustain_level/max_value, math.e)

        io1 = 1
        io2 = 4/3
        io3 = 1
        for t in range(amount_of_ns):

            # attack period
            if t <= attack_ns:
                a = (math.e**(t/attack_constant)-1)
                i = -a*io1
                notes.append(a * velocity/127 * math.sin(2 * math.pi * fc * t / self.frame_rate + i * math.sin(
                    2 * math.pi * fm * t / self.frame_rate)))

            # decay period
            elif t <= (decay_ns + attack_ns):
                curr_time_offset = attack_ns
                a = max_value * math.e**(-(t-curr_time_offset)/decay_constant)
                i = -a*4/3
                notes.append(a * velocity/127 * math.sin(2 * math.pi * fc * t / self.frame_rate + i * math.sin(
                    2 * math.pi * fm * t / self.frame_rate)))

            # sustain period
            elif t <= (decay_ns + sustain_ns + attack_ns):
                a = sustain_level
                i = -a*io2
                notes.append(a * velocity/127 * math.sin(2 * math.pi * fc * t / self.frame_rate + i * math.sin(
                    2 * math.pi * fm * t / self.frame_rate)))

            # release period
            elif t > (decay_ns + sustain_ns + attack_ns):
                curr_time_offset = decay_ns + sustain_ns + attack_ns
                a = sustain_level * math.e**(-(t-curr_time_offset)/release_constant)
                i = -sustain_level*io3
                notes.append(a * velocity/127 * math.sin(2 * math.pi * fc * t / self.frame_rate + i * math.sin(
                    2 * math.pi * fm * t / self.frame_rate)))

        return notes

    def synthesize_trumpet(self, pitch: int, amount_of_ns: int, velocity):
        # c/m = N1/N2
        # fo = c/N1 = m/N2
        # N2 = 1, the spectrum contains all the harmonics
        # JohnChowning
        freq = 2 ** ((pitch - 69) / 12) * 440
        N1 = 1
        fc = freq * N1
        N2 = 1
        fm = freq * N2 + 0.2

        notes = []
        # duration of the attack in seconds:
        attack_ns = int(0.16 * self.frame_rate)
        # duration of the decay in seconds
        decay_ns = int(0.034 * self.frame_rate)
        # post_attack_ns = int(0.022 * self.frame_rate)

        # duration of the release in seconds:
        release_ns = int(0.226 * self.frame_rate)

        if amount_of_ns < (attack_ns + release_ns + decay_ns):
            # duration of the attack / total duration of the note : 0.1346
            attack_ns = int(amount_of_ns*0.3)
            # post_attack_ns = int(amount_of_ns*0.057)
            decay_ns = int(amount_of_ns*0.05)
            # duration of the release / total duration of the note : 0.32
            release_ns = int(amount_of_ns*1/3)

        sustain_ns = amount_of_ns - release_ns - decay_ns - attack_ns
        sustain_level = 0.92
        max_value = 0.999
        attack_constant = attack_ns / math.log(max_value + 1, math.e)
        release_constant = -release_ns / math.log(1/256, math.e)
        decay_constant = -decay_ns / math.log(sustain_level/max_value, math.e)

        io1 = 1
        io2 = 1
        io3 = 1
        io4 = 1
        for t in range(amount_of_ns):

            # attack period
            if t <= attack_ns:
                a = (math.e**(t/attack_constant)-1)
                i = -a*io1
                new_note = a * velocity/127 * math.sin(2 * math.pi * fc * t / self.frame_rate + i * math.sin(
                    2 * math.pi * fm * t / self.frame_rate))
                if new_note < 0:
                    new_note *= 1/3
                notes.append(new_note)

            # decay period
            elif t <= (decay_ns + attack_ns):
                curr_time_offset = attack_ns
                a = max_value * math.e**(-(t-curr_time_offset)/decay_constant)
                i = -a*io2
                new_note = a * velocity/127 * math.sin(2 * math.pi * fc * t / self.frame_rate + i * math.sin(
                    2 * math.pi * fm * t / self.frame_rate))
                if new_note < 0:
                    new_note *= 1/3
                notes.append(new_note)

            # sustain period
            elif t <= (decay_ns + sustain_ns + attack_ns):
                a = sustain_level
                i = -a*io3
                new_note = a * velocity/127 * math.sin(2 * math.pi * fc * t / self.frame_rate + i * math.sin(
                    2 * math.pi * fm * t / self.frame_rate))
                if new_note < 0:
                    new_note *= 1/3
                notes.append(new_note)

            # release period
            elif t > (decay_ns + sustain_ns + attack_ns):
                curr_time_offset = decay_ns + sustain_ns + attack_ns
                a = sustain_level * math.e**(-(t-curr_time_offset)/release_constant)
                i = -sustain_level*io4
                new_note = a * velocity/127 * math.sin(2 * math.pi * fc * t / self.frame_rate + i * math.sin(
                    2 * math.pi * fm * t / self.frame_rate))
                if new_note < 0:
                    new_note *= 1/3
                notes.append(new_note)

        return notes
