import random
import numpy as np
import math
import matplotlib.pyplot as plt
import midi
import synth




class KSSynthesizer(synth.Synthesizer):
    def __init__(self, resolution):
        self.set_create_notes_callback(self.create_note_array)
        super(KSSynthesizer, self).__init__(resolution)
        self.curr_instrument = ""
        # overdrive variables
        self.lp1 = .5    # para el low pass
        self.lp0 = .1    # para el low pass


        self.a0 = np.float(0)   # dc blocking filter
        self.a1 = np.float(0)   # dc blocking filter
        self.b1 = np.float(0)   # dc blocking filter



    def set_dc_blocking_filter(self, pitch):
        freq = 2 ** ((pitch - 69) / 12) * 440
        wco = 2.0*math.pi*freq/10.0
        self.a0 = 1.0/(1.0 + wco/2.0)
        self.a1 = -1.0 * self.a0
        self.b1 = self.a0*(1 - wco/2.0)

    # https://en.wikipedia.org/wiki/MIDI_tuning_standard#Frequency_values
    def create_note_array(self, pitch, duration: int, intensity, instrument = int):
        # if instrument==drum:
        return self.overdrive(pitch, duration, intensity)

    # cuerdas sin decay stretching
    def string_wo_decay(self, pitch, duration: int, intensity):
        b = -1
        # noinspection SpellCheckingInspection
        wavetable = self.create_noise(self.frame_rate, pitch)
        notes = []
        current_note = 0
        previous_note = np.float(0)
        while len(notes) < duration:
            wavetable[current_note] = b * 0.5 * (wavetable[current_note] + previous_note)  # promedio
            notes.append(wavetable[current_note])
            previous_note = notes[-1]  # ultimo elemento de la lista
            current_note += 1
            current_note = current_note % wavetable.size
        return np.array(notes)

    def string(self, pitch, duration: int, intensity):
        wavetable = self.create_noise(self.frame_rate, pitch)
        wavetable = self.normalize(wavetable)
        notes = []
        current_note = 0
        previous_note = np.float(0)
        while len(notes) < duration:
            rand = np.random.binomial(1, 1 - 1 / (1 + intensity / 127))  # sale 1 con prob=1-1/s;; sale 0 con prob 1/s (xo 1 al s para que sea > 1)
            if rand == 0:
                wavetable[current_note] = 0.996 * 0.5 * (wavetable[current_note] + previous_note)  # promedio
            notes.append(wavetable[current_note])  # el promedio (con prob 1/s) o queda igual (con prob 1-1/s)
            previous_note = notes[-1]  # ultimo elemento de la lista
            current_note += 1
            current_note = current_note % wavetable.size
        return np.array(notes)

    def overdrive(self, pitch, duration: int, intensity):
        wavetable = self.create_noise(self.frame_rate, pitch)
        wavetable = self.normalize(wavetable)
        #print(sum(wavetable))
        notes = []
        current_note = 0
        previous_note, x = np.float(0), np.float(0)
        while len(notes) < duration:
            rand = np.random.binomial(1, 1 - 1 / (1 + intensity / 127))  # sale 1 con prob=1-1/s;; sale 0 con prob 1/s (xo 1 al s para que sea > 1)
            if rand == 0:
                wavetable[current_note] = 0.996 * 0.5 * (wavetable[current_note] + previous_note)  # promedio
            x = self.soft_clip(wavetable[current_note])
            notes.append(0.3*wavetable[current_note]+x)  # el promedio (con prob 1/s) o queda igual (con prob 1-1/s)
            previous_note = notes[-1]  # ultimo elemento de la lista
            current_note += 1
            current_note = current_note % wavetable.size
        return notes

    def soft_clip(self, x):       # soft clipping
            if x >= 1:
                return 2/3
            elif x <= -1:
                return -2/3
            else:
                return x - x**3/3

    # percusion sin decay stretching
    def drum_wo_decay(self, pitch, duration: int, intensity):
        b = 0.5  #drumlike sound
        wavetable = np.ones(self.frame_rate // pitch)
        notes = []
        current_note = 0
        previous_note = np.float(0)
        while len(notes) < duration:
            rand = np.random.binomial(1, b)  # sale 1 ó 0
            sign = 2 * rand - 1  # si sale 1 queda 1; si sale 0, queda -1
            wavetable[current_note] = sign * 0.9 * 0.5 * (wavetable[current_note] + previous_note)  # promedio
            notes.append(wavetable[current_note])
            previous_note = notes[-1]  # ultimo elemento de la lista
            current_note += 1
            current_note = current_note % wavetable.size
        return np.array(notes)

    # TODO : hacer que suene mas linda la percusion con decay
    def drum(self, pitch, duration: int, intensity):
        b = 0.5  # drumlike sound
        wavetable = np.ones(self.frame_rate // pitch)
        wavetable = self.normalize(wavetable)
        notes = []
        current_note = 0
        previous_note = np.float(0)
        while len(notes) < duration:
            rand = np.random.binomial(1, 1 - 1 / (1 + intensity / 127))
            sign = -1 + 2 * np.random.binomial(1, b)   # si sale 1 queda 1; si sale 0, queda -1
            if rand == 0:
                wavetable[current_note] = sign * 0.9 * 0.5 * (wavetable[current_note] + previous_note)  # promedio
                notes.append(wavetable[current_note])
            else:
                notes.append(sign * wavetable[current_note])
            previous_note = notes[-1]  # ultimo elemento de la lista
            current_note += 1
            current_note = current_note % wavetable.size
        return np.array(notes)

    def create_noise(self, fs, pitch):  # vector con 1 ó -1
        freq = 2 ** ((pitch - 69) / 12) * 440
        wavetable_size = fs // int(freq)
        wavetable = np.random.uniform(-1.0, 1.0, wavetable_size)
        #wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1)
        return wavetable
        #return wavetable.astype(np.float)

    def normalize(self, vec):
        norm = np.linalg.norm(vec)
        #print(sum(vec/norm))
        if norm == 0:
            return vec
        return vec / norm


