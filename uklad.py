import matplotlib.pyplot as plt
import math

def calka_eulera(t_start, t_stop, dt, amplituda, czestotliwosc, R, L, Ke, Kt, J, k, typ_sygnalu="sinusoidalny", wypelnienie=0.5, phi=0.0):

    N = int((t_stop - t_start) / dt)
    
    # Zastępujemy np.linspace listą składaną (list comprehension)
    czas = [t_start + i * dt for i in range(N)]

    # Zastępujemy np.zeros prealokowanymi listami wypełnionymi zerami
    i_prad = [0.0] * N
    omega = [0.0] * N
    theta = [0.0] * N
    u = [0.0] * N

    typ = typ_sygnalu.lower().strip()

    # Ponieważ nie mamy numpy, generujemy sygnał element po elemencie w pętli
    for i in range(N):
        t = czas[i]
        
        if typ == "sinusoidalny":
            u[i] = amplituda * math.sin(2 * math.pi * czestotliwosc * t + phi)
            
        elif typ in ["piłozębny", "piłozebny"]:
            faza = (czestotliwosc * t + phi / (2 * math.pi)) % 1.0
            u[i] = amplituda * (2.0 * faza - 1.0)
            
        elif typ in ["prostokątny", "prostokatny"]:
            duty = max(0.0, min(1.0, wypelnienie))
            faza = (czestotliwosc * t + phi / (2 * math.pi)) % 1.0
            # Zamiast np.where używamy standardowego warunku if/else
            u[i] = amplituda * (1.0 if faza < duty else -1.0)
            
        else:
            raise ValueError(f"Nieobsługiwany typ sygnału: {typ_sygnalu}")

    # Główna pętla całkująca pozostaje bez zmian, działa na zwykłych listach
    for n in range(N - 1):
        di_dt = (1/L) * (u[n] - R * i_prad[n] - Ke * omega[n])
        domega_dt = (1/J) * (Kt * i_prad[n] - k * theta[n])
        dtheta_dt = omega[n]
 
        i_prad[n+1] = i_prad[n] + di_dt * dt
        omega[n+1] = omega[n] + domega_dt * dt
        theta[n+1] = theta[n] + dtheta_dt * dt
        
    return czas, u, i_prad, omega
