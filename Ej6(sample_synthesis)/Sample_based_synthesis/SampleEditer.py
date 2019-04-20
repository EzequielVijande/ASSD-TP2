import wave
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import math


f_s, data= wavfile.read(".\Samples\Guitar\guitar_Gs5_very-long_forte_normal.wav")
if(len(data.shape) > 1):
    data = data[:,0]

t=np.linspace(0,len(data),num=len(data))
tau=0.8*t
t= t/f_s

ax1=plt.subplot(2, 1, 1)
plt.plot(t,data)
plt.ylabel("Original")

ax2=plt.subplot(2, 1, 2)

sec_index = int(2.2*f_s)
output = np.zeros(sec_index)
output = data[:sec_index]
t_out=np.linspace(0,len(output),num=len(output))/f_s

plt.plot(t_out,output)
plt.ylabel("Modificada")
plt.show()

wavfile.write("Gs5_forte_trimmed.wav", f_s, output)
