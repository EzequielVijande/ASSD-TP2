import wave
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import math
from SampleSynthesizer import ResampleArray

desired_fs = 44100
f_s, data= wavfile.read('.\\Samples\\Trumpet\\trumpet_C4_1_fortissimo_normal.wav')
if(len(data.shape) > 1):
    data = data[:,0]
if(f_s != desired_fs):
    data = ResampleArray(data,f_s,desired_fs)

t=np.linspace(0,len(data),num=len(data))
t= t/desired_fs

ax1=plt.subplot(2, 1, 1)
plt.plot(t,data)
plt.ylabel("Original")

ax2=plt.subplot(2, 1, 2)

start_index = int(0.179027*desired_fs)
sec_index = int((2.12517)*desired_fs)
output = np.zeros(sec_index-start_index)
output = data[start_index:sec_index]
t_out=np.linspace(0,len(output),num=len(output))/desired_fs

plt.plot(t_out,output)
plt.ylabel("Modificada")
plt.show()

#wavfile.write("Gs5_forte_trimmed.wav", desired_fs, output)
