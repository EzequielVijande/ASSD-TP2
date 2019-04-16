import wave
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import OLA as o
def MakeWindow(length,type='Hann'):
    if(type== 'Hann'):
        return np.hanning(length)
    else:
        return np.zeros(1)

f_s, data= wavfile.read(".\Audio\Drums.wav")
N=2210
window = MakeWindow(N)
print("fs = ",f_s)
t=np.linspace(0,len(data),num=len(data))
tau=2*t
y= o.OLA(data,window,tau)
y = y.astype('int16')
print(y.size)
t= t/f_s
tau = tau/f_s
ax1=plt.subplot(2, 1, 1)
plt.plot(t,data)
ax2=plt.subplot(2, 1, 2)
plt.plot(tau,y)
plt.show()
wavfile.write("Holis.wav", f_s, y)

