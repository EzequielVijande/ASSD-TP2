import random
import numpy as np
from IPython.display import Audio
import matplotlib.pyplot as plt


def create_noise(fs, pitch):  # vector con 1 ó -1
    wavetable_size = fs // pitch
    #random.uniform(-1, 1) for _ in range(wavetable_size)
    wavetable = np.array([2 * random.randint(0, 1) - 1])
    for i in range(wavetable_size):
        wavetable = np.append(wavetable, 2 * random.randint(0, 1) - 1)
    plt.plot(wavetable)
    plt.show()
    return wavetable.astype(np.float)


def KarplusStrongString(fs, n_samples, pitch):
    wavetable = create_noise(fs, pitch)
    samples = []
    current_sample = 0
    previous_value = np.float(0)
    while len(samples) < n_samples:
        wavetable[current_sample] = 0.996 * 0.5 * (wavetable[current_sample] + previous_value)  # promedio
        samples.append(wavetable[current_sample])
        previous_value = samples[-1]  # ultimo elemento de la lista
        current_sample += 1
        current_sample = current_sample % wavetable.size
    return np.array(samples)


def KarplusStrongDrum(fs, n_samples, pitch):
    b = 0.3  # b=0.3 suena cool
    wavetable = np.ones(fs // pitch)
    samples = []
    current_sample = 0
    previous_value = np.float(0)
    while len(samples) < n_samples:
        rand = np.random.binomial(1, b)  # sale 1 ó 0
        sign = 2 * rand - 1  # si sale 1 queda 1; si sale 0, queda -1
        wavetable[current_sample] = sign * 0.5 * (wavetable[current_sample] + previous_value)  # promedio
        samples.append(wavetable[current_sample])
        previous_value = samples[-1]  # ultimo elemento de la lista
        current_sample += 1
        current_sample = current_sample % wavetable.size
    return np.array(samples)


fs = 20000

for pitch in [20, 55, 110, 220, 440, 880, 1288]:
    sample = KarplusStrongString(fs, 2 * fs, pitch)
    # sample = KarplusStrongDrum(fs, 2 * fs, pitch)
    Audio(sample, rate=fs)

# pitch = 40
# sample1 = KarplusStrongString(fs, 2 * fs, pitch)
# sample1 = KarplusStrongDrum(fs, 1 * fs, pitch)
# plt.subplot(211)
# plt.plot(sample1)
# plt.subplot(212)
# plt.plot(sample1)
# plt.xlim(0, 1000)
# plt.show()
# Audio(sample1, rate=fs)
