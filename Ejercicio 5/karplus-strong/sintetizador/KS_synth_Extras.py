import numpy as np


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

def overdriveKS(self, pitch, duration: int, intensity):
    wavetable = self.create_noise(self.frame_rate, pitch)
    wavetable = self.normalize(wavetable)
    notes = []
    current_note = 0
    previous_note, x = np.float(0), np.float(0)
    while len(notes) < duration:
        rand = np.random.binomial(1, 1 - 1 / (
                    1 + intensity / 127))  # sale 1 con prob=1-1/s;; sale 0 con prob 1/s (xo 1 al s para que sea > 1)
        if rand == 0:
            wavetable[current_note] = 0.5 * (wavetable[current_note] + previous_note)  # promedio
        # x = self.soft_clip(wavetable[current_note])
        notes.append(wavetable[current_note])  # el promedio (con prob 1/s) o queda igual (con prob 1-1/s)
        previous_note = notes[-1]  # ultimo elemento de la lista
        current_note += 1
        current_note = current_note % wavetable.size
    return notes

def backupoverdrive(self, pitch, duration: int, intensity):
    wavetable = self.create_noise(self.frame_rate, pitch)
    wavetable = self.normalize(wavetable)
    x = wavetable.copy()
    notes, h1, h2, h1h2 = [], [], [], []
    normed = []
    current_note = 0
    # freq = 2 ** ((pitch - 69) / 12) * 440
    # a = 1/np.abs((1 + 2 * math.cos(2 * math.pi * freq)))
    self.set_dc_blocking_filter(pitch)
    previous_note, prev_x, prevprev_x = np.float(0), np.float(0), np.float(0)
    while len(notes) < duration:
        for i in range(wavetable.size):
            h1.append(self.lp1 * x[current_note] + self.lp0 * prev_x + self.lp1 * prevprev_x)
            h2.append(self.a0 * x[current_note] + self.a1 * prev_x + self.b1 * previous_note)
            previous_note = wavetable[current_note]  # ultimo elemento de la lista
            prevprev_x = prev_x
            # wavetable[current_note] = distortion
            if current_note > 0:
                prev_x = x[current_note - 1]
            current_note += 1
            current_note = current_note % wavetable.size
        notes.append(np.convolve(h1, h2))
    # h1h2 = list(np.convolve(h1, h2))
    # notes.append(h1h2)
    return notes


# percusion sin decay stretching
def drum_wo_decay(self, pitch, duration: int, intensity):
        b = 0.5  # drumlike sound
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


def overdrive2(self, x, pitch):
    N = self.frame_rate//pitch
    self.set_dc_blocking_filter(pitch)      #seteo variables del filtro que filtra la continua
    y = np.array([0.0] * x.size)
    w = np.array([0.0] * x.size)
    prev_x, prev_y, prev_w, prevN_y = 0.0, 0.0, 0.0, 0.0
    q = 0.01

    for n in range(x.size):
        if n >= N:
            w[n] = self.a0 * x[n] + self.a1 * x[n-1] + self.b1 * w[n-1]
            y[n] = w[n] - q*w[n-1] + q*y[n-1] + (1-q)*y[n-N]
        else:
            if n > 0:
                prev_y = y[n-1]
                prev_w = w[n-1]
                prev_x = x[n-1]
                if n >= N:
                    prevN_y = y[n - N]
                else:
                    prevN_y = 0
                w[n] = self.a0 * x[n] + self.a1 * prev_x + self.b1 * prev_w
                y[n] = w[n] - q * prev_w + q * prev_y + (1 - q) * prevN_y
            else:
                w[n] = self.a0 * x[n]
                y[n] = w[n]

        #y[n] = self.soft_clip(y[n])  # distorsiono
    return y