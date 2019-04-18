import wave
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import OLA as o
import PhaseVocoder as ph
def MakeWindow(length,type='Hann'):
    if(type== 'Hann'):
        return np.hanning(length)
    else:
        return np.zeros(1)

f_s, data= wavfile.read(".\Audio\pop.wav")
if(len(data.shape) > 1):
    data = data[:,0]
N=2210
window = MakeWindow(N)
print("fs = ",f_s)
t=np.linspace(0,len(data),num=len(data))
tau=1.5*t
y= ph.PhVocoder(data,window,tau,int(N/2))
#y = y.astype('int16')
#t= t/f_s
#ax1=plt.subplot(2, 1, 1)
#plt.plot(t,data)

#ax2=plt.subplot(2, 1, 2)
#t_out= np.linspace(0,len(y),num=len(y))/f_s
#plt.plot(t_out,y)
#plt.show()
#wavfile.write("Holis.wav", f_s, y)
#wavfile.write("original.wav", f_s, data)

