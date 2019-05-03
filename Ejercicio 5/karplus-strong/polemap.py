import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import random
import control


N = 20
RL= -0.996


def create_noise(n):        #número random entre [-0.5;0.5]
    return [random.random() - 0.5 for _ in range(n)]


#funcion transferencia

num = np.array([1])
for i in range(0, N+1, 1):
    num = np.append(num, 0)
#den = np.array([1,  (0 for i in range(1, int(N), 1)),  -RL/2, -RL/2])
den = np.array([1])
for i in range(0, N-1, 1):
    den = np.append(den, 0)
for _ in range(2):
    den = np.append(den, -RL/2)

tfz = control.TransferFunction(num, den)

#diagrama de polos  y ceros
[z, p]=control.pzmap(tfz)
plt.grid()
plt.show()

#para ver si es inestable ??
# poles = np.array(abs(tfz.pole()))
#if np.any(poles > 1):
#    print("putavida, inestable")















