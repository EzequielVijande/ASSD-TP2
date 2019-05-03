import random
import numpy as np
import math
import matplotlib.pyplot as plt
import midi
import synth
from scipy import signal
import karplus_extras


class KarplusSynthesizer(synth.Synthesizer):
    def __init__(self, resolution):
        super(KarplusSynthesizer, self).__init__(resolution)
        self.set_create_notes_callback(self.make_note)
        # overdrive variables
        self.lp1 = 0.996    # para el low pass
        self.lp0 = .1    # para el low pass

        self.a0 = np.float(0)   # dc blocking filter
        self.a1 = np.float(0)   # dc blocking filter
        self.b1 = np.float(0)   # dc blocking filter

    def set_create_notes_callback(self, callback):
        self.create_notes_callback = callback

    def set_dc_blocking_filter(self, pitch):        #defino variables del filtro de continua segun la frecuencia
        freq = 2 ** ((pitch - 69) / 12) * 440
        wco = 2.0*math.pi*freq/10.0
        self.a0 = 1.0/(1.0 + wco/2.0)
        self.a1 = -1.0 * self.a0
        self.b1 = self.a0*(1 - wco/2.0)


    def make_note(self, pitch, duration: int, intensity, instrument):
        if instrument == synth.GUITAR:      #guitarra acustica
            return self.acoustic_guitar(pitch, duration, intensity)
        elif instrument == synth.DRUMS:     #percusion
            return self.drums(pitch, duration, intensity)
        elif instrument == synth.ELECTRIC_GUITAR:   #guitarra electrica
            return self.electric_guitar(pitch, duration, intensity)
        else:
            return self.acoustic_guitar(pitch, duration, intensity)


    def acoustic_guitar(self, pitch, duration: int, intensity):
        wavetable = self.create_noise(self.frame_rate, pitch)       #ruido
        wavetable = self.normalize(wavetable)                       #normalizo
        notes = []
        current_note = 0
        previous_note = np.float(0)
        while len(notes) < duration:
            rand = np.random.binomial(1, 1 - 1 / (1 + intensity / 127))  # sale 1 con prob=1-1/s;; sale 0 con prob 1/s (xo 1 al s para que sea > 1)
            if rand == 0:
                wavetable[current_note] = 0.996 * 0.5 * (wavetable[current_note] + previous_note)  # promedio
            notes.append(wavetable[current_note])  # el promedio (con prob 1/s) o queda igual (con prob 1-1/s)
            previous_note = notes[-1]  # ultimo elemento de la lista
            current_note += 1           #incremento indice
            current_note = current_note % wavetable.size
        return np.array(self.normalize_notes(notes))

    def electric_guitar(self, pitch, duration: int, intensity):
        distorsion = 1.0
        notes = []
        # notes_post_distortion = []
        burst = self.create_noise(self.frame_rate, pitch)       #ruido
        burst = self.normalize(burst)
        burst = self.dynamics(burst, intensity)                 #filtro para la intensidad de la nota
        while len(notes) < duration:
            xsoft = self.lowpass(burst, pitch)      #pasabajos y normalizo
            x = self.lowpass(xsoft, pitch)          #otro pasabajos para que no se escuche tan metalico, sin púa

            w = self.dc_blocking_filter(x, pitch)   #filtro que bloquea la continua
            y = self.overdrive(w, distorsion)       #distorsion
            z = self.lowpass(np.add(1.4*w, y),pitch)    #pasabajos hace que suene mejor
            #burst = self.feedback_delay(y, pitch)
            notes.extend(z)
        notes = self.normalize_notes(notes)
        return notes

    # percusion con decay
    def drums(self, pitch, duration: int, intensity):
        b = 0.5  # drumlike sound
        wavetable = np.ones(self.frame_rate // pitch)
        notes = []
        current_note = 0
        previous_note = np.float(0)
        while len(notes) < duration:
            rand = np.random.binomial(1, 1 - 1 / (1 + intensity / 127))
            sign = -1 + 2 * np.random.binomial(1, b)   # si sale 1 queda 1; si sale 0, queda -1
            if rand == 0:
                wavetable[current_note] = sign * 0.85 * 0.5 * (wavetable[current_note] + previous_note)  # promedio
                notes.append(wavetable[current_note])
            else:
                notes.append(sign * wavetable[current_note])
            previous_note = notes[-1]  # ultimo elemento de la lista
            current_note += 1
            current_note = current_note % wavetable.size

            #normalizo no con self.normalize, ni self.normalize_notes porque el vector tiene valores entre [0,1], NO [-1, 1]
        suma = sum(notes)
        if notes:
            notes = self.normalize_notes(notes)
        return np.array(notes)

    def dc_blocking_filter(self, x, pitch):
        self.set_dc_blocking_filter(pitch)  # seteo variables del filtro que filtra la continua
        y = np.array([0.0] * x.size)
        prev_x, prev_y= 0.0, 0.0
        for n in range(x.size):
         if n > 0:
             prev_x = x[n-1]
         else:
             prev_x = 0.0
         if n > 0:
            prev_y = y[n-1]
         else:
             prev_y = 0
         y[n] = self.a0*x[n] + self.a1*prev_x + self.b1*prev_y       #filtro
        return y

    def overdrive(self, y, distorsion):
        for n in range(y.size):
            y[n] = distorsion*self.soft_clip(y[n])         #distorsiono
        return self.normalize(y)

    def feedback_delay(self, x, pitch):
        N = self.frame_rate//pitch
        y = np.array([0.0] * x.size)
        prev_x, prev_y, prevN_y = 0.0, 0.0, 0.0
        q = 0.9

        for n in range(x.size):
            if n >= N:
                y[n] = x[n] - q*x[n-1] + q*y[n-1] + (1-q)*y[n-N]
            else:
                if n > 0:
                    prev_y = y[n-1]
                    prev_x = x[n-1]
                    if n >= N:
                        prevN_y = y[n - N]
                    else:
                        prevN_y = 0
                    y[n] = x[n] - q * prev_x + q * prev_y + (1 - q) * prevN_y
                else:
                    y[n] = x[n]
        return y

    def lowpass(self, x: np.ndarray, pitch):
        c = 1 / abs(1 + 2 * math.cos(2 * math.pi * pitch / self.frame_rate))
        y = np.array([0.0]*x.size)
        prev_x, prevprev_x = np.float(0), np.float(0)
        for i in range(x.size):
            if i > 0:
                prev_x = x[i - 1]
            if i > 1:
                prevprev_x = x[i - 2]
            y[i] = c * x[i] + c * prev_x + c * prevprev_x
        return self.normalize(y)

    # para normalizar lista de notas
    def normalize_notes(self, notes):
        normed = []
        if len(notes) > 1:
            minimum = np.min(notes)
            maximum = np.max(notes)
            for val in notes:
                x = 2*(val-minimum)/(maximum-minimum) - 1
                if np.isnan(x):
                    normed.append(0)
                else:
                    normed.append(x)
            return normed
        else:
            return notes

    def soft_clip(self, x):       # soft clipping
        if x >= 1:
            return 2/3
        elif x <= -1:
            return -2/3
        else:
            return x - x**3/3



    def create_noise(self, fs, pitch):  # vector con 1 ó -1
        freq = 2 ** ((pitch - 69) / 12) * 440
        wavetable_size = fs // int(freq)
        wavetable = np.random.uniform(-1.0, 1.0, wavetable_size)
        return wavetable

    # para normalizar vector conocido
    def normalize(self, raw):       # normalizo entre -1, 1
        min = np.amin(raw)
        max = np.amax(raw)
        for i, val in np.ndenumerate(raw):
            raw[i] = 2*(val - min) / (max - min)-1
        return raw

    def dynamics(self, x, intensity):        #R e (0, 1); cerca de 1 suena más bajo
        R = 1 + intensity/127
        y = np.array([0.0] * x.size)
        prev_x = np.float(0)
        for i in range(x.size):
            if i > 0:
                prev_x = x[i - 1]
            y[i] = (1-R) * x[i] + R * prev_x
        return self.normalize(y)
