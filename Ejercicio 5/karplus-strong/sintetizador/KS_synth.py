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

    # https://en.wikipedia.org/wiki/MIDI_tuning_standard#Frequency_values
    def create_note_array(self, pitch, amount_of_ns: int, velocity, instrument: int):
        # if instrument==drum:
        notes = self.drum(pitch, amount_of_ns, velocity)
        #plt.plot(notes)
        #plt.show()
        return notes
        #     return notes
        #notes = self.drum(pitch, amount_of_ns, velocity)
        #return notes


    #cuerdas sin decay stretching
    def stringWODecay(self, pitch, amount_of_ns: int, velocity):
        b = -1
        wavetable = self.create_noise(self.frame_rate, pitch)
        notes = []
        current_note = 0
        previous_note = np.float(0)
        while len(notes) < amount_of_ns:
            wavetable[current_note] = b * 0.5 * (wavetable[current_note] + previous_note)  # promedio
            notes.append(wavetable[current_note])
            previous_value = notes[-1]  # ultimo elemento de la lista
            current_note += 1
            current_note = current_note % wavetable.size
        return np.array(notes)



    def string(self, pitch, amount_of_ns: int, velocity):
        wavetable = self.create_noise(self.frame_rate, pitch)
        notes = []
        current_note = 0
        previous_note = np.float(0)
        while len(notes) < amount_of_ns:
            rand = np.random.binomial(1, 1 - 1 / (1+velocity/127))  # sale 1 con prob=1-1/s;; sale 0 con prob 1/s (sumo 1 al s para que sea > 1)
            if rand == 0:
                wavetable[current_note] = 0.996 * 0.5 * (wavetable[current_note] + previous_note)  # promedio
            notes.append(wavetable[current_note])  # el promedio (con prob 1/s) o queda igual (con prob 1-1/s)
            previous_note = notes[-1]  # ultimo elemento de la lista
            current_note += 1
            current_note = current_note % wavetable.size
        return np.array(notes)

    #percusion sin decay stretching
    def drumWODecay(self, pitch, amount_of_ns: int, velocity):
        b = 0.5  #drumlike sound
        wavetable = np.ones(self.frame_rate // pitch)
        notes = []
        current_note = 0
        previous_note = np.float(0)
        while len(notes) < amount_of_ns:
            rand = np.random.binomial(1, b)  # sale 1 ó 0
            sign = 2 * rand - 1  # si sale 1 queda 1; si sale 0, queda -1
            wavetable[current_note] = sign * 0.9 * 0.5 * (wavetable[current_note] + previous_note)  # promedio
            notes.append(wavetable[current_note])
            previous_note = notes[-1]  # ultimo elemento de la lista
            current_note += 1
            current_note = current_note % wavetable.size
        return np.array(notes)


    def drum(self, pitch, amount_of_ns: int, velocity):
        b = 0.5  #drumlike sound
        wavetable = np.ones(self.frame_rate // pitch)
        notes = []
        current_note = 0
        previous_note = np.float(0)
        while len(notes) < amount_of_ns:
            rand = np.random.binomial(1, 1 - 1 / (1+velocity/127))  # sale 1 con prob=1-1/s;; sale 0 con prob 1/s (sumo 1 al s para que sea > 1)
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
        #np.random.uniform(-1.0, 1.0, wavetable.size)
        wavetable = np.array([2 * random.randint(0, 1) - 1])
        for i in range(wavetable_size):
            wavetable = np.append(wavetable, 2 * random.randint(0, 1) - 1)
        #plt.plot(wavetable)
        #plt.show()
        return wavetable.astype(np.float)




