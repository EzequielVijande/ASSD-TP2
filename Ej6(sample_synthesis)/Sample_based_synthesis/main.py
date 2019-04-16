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

f_s, data= wavfile.read(".\Audio\Stam1h-120.wav")
if(len(data.shape) > 1):
    data = data[:,0]
N=2210
window = MakeWindow(N)
print("fs = ",f_s)
t=np.linspace(0,len(data),num=len(data))
tau=2*t
y= o.OLA(data,window,tau)
y = y.astype('int16')
t= t/f_s
ax1=plt.subplot(2, 1, 1)
plt.plot(t,data)

ax2=plt.subplot(2, 1, 2)
t_out= np.linspace(0,len(data),num=len(y))/f_s
plt.plot(t_out,y)
plt.show()
wavfile.write("Holis.wav", f_s, y)
wavfile.write("original.wav", f_s, data)

