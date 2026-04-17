import numpy as np
import matplotlib.pyplot as plt
from scipy import signal # Dodajemy moduł do generowania piły i prostokąta

def calka_eulera(t_start,t_stop,dt,amplituda,czestotliwosc,R,L,Ke,Kt,J,k):

    N = int((t_stop - t_start) / dt)

    czas = np.linspace(t_start, t_stop, N)

    i_prad = np.zeros(N)
    omega = np.zeros(N)
    theta = np.zeros(N)
    u = np.zeros(N)

    u = amplituda * signal.sawtooth(2 * np.pi * czestotliwosc * czas)


    for n in range(N - 1):
        di_dt = (1/L) * (u[n] - R * i_prad[n] - Ke * omega[n])
        domega_dt = (1/J) * (Kt * i_prad[n] - k * theta[n])
        dtheta_dt = omega[n]
    
        i_prad[n+1] = i_prad[n] + di_dt * dt
        omega[n+1] = omega[n] + domega_dt * dt
        theta[n+1] = theta[n] + dtheta_dt * dt
    return czas,u,i_prad,omega

