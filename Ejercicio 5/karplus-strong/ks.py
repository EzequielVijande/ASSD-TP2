import random
import numpy as np
from IPython.display import Audio
import matplotlib.pyplot as plt


def create_noise(fs):       #vector con 1 ó -1
    wavetable_size = fs // 110
    wavetable = np.array([2 * random.randint(0, 1) - 1])
    for i in range(wavetable_size):
         wavetable = np.append(wavetable, 2 * random.randint(0, 1) - 1)
    plt.plot(wavetable)
    plt.show()
    return wavetable.astype(np.float)


def karplus_strong(wavetable, n_samples):
    samples = []
    current_sample = 0
    previous_value = np.float(0)
    while len(samples) < n_samples:
        wavetable[current_sample] = 0.996* 0.5 * (wavetable[current_sample] + previous_value)       #promedio
        samples.append(wavetable[current_sample])
        previous_value = samples[-1]        #ultimo elemento de la lista
        current_sample += 1
        current_sample = current_sample % wavetable.size
    return np.array(samples)


fs=22050
wavetable = create_noise(fs)
sample1 = karplus_strong(wavetable, 2 * fs)
plt.subplot(211)
plt.plot(sample1)
plt.show()
plt.subplot(212)
plt.plot(sample1)
plt.xlim(0, 1000)
plt.show()
Audio(sample1, rate=fs)
