 
#Dziedzina czasu
#U(t)= R*i(t) + L*i'(t) + K_e *Teta'
#U(S)= R*i + s*L*i + K_e * Teta * s 
#
#  J*teta''= K_T*i - k*teta
#  J*teta*s^2 = K_T*i -k*teta

import numpy as np
from scipy import signal




t=np.linspace(0,10,1000)

# sygnał wejsciowy
amplituda = 5
czestotliwosc = 1 #Hz
szerokosc = 0.5
u_harmoniczny = amplituda * np.sin(2*np.pi*czestotliwosc*t)
u_trojkatny = amplituda*signal.sawtooth(2*np.pi*czestotliwosc*t, szerokosc )

R=1
L=1
K_e=1
J=2

