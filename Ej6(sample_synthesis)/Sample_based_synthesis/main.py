import wave
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import OLA as o
import PhaseVocoder as ph
import SpectrumSeparator as spectre
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
tau=3*t
t_h, harm, t_p, perc = spectre.GetPercussiveAndHarmonicSpectrum(data,10,10,2210,beta=2)
harm = harm.astype('int16')
perc = perc.astype('int16')

ax1=plt.subplot(2, 1, 1)
plt.plot(t_h,harm)

ax2=plt.subplot(2, 1, 2)
plt.plot(t_p,perc)
plt.show()

wavfile.write("Armonico.wav", f_s, harm)
wavfile.write("Percusion.wav", f_s, perc)

#y= ph.PhVocoder(data,window,tau,int(N/2))
#y= o.OLA(data,window,tau,0.1)
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

