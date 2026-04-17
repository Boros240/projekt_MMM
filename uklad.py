import numpy as np
import matplotlib.pyplot as plt
from scipy import signal # Dodajemy moduł do generowania piły i prostokąta

# ==========================================
# 1. PARAMETRY UKŁADU
# ==========================================
R = 5.0      # Rezystancja [Ohm]
L = 0.02     # Indukcyjność [H]
Ke = 0.1     # Stała elektromotoryczna [V/(rad/s)]
Kt = 0.1     # Stała momentu [Nm/A]
J = 0.01     # Moment bezwładności [kg*m^2]
k = 0.5      # Współczynnik sprężystości [Nm/rad]

# ==========================================
# 3. USTAWIENIA SYMULACJI (Czas i Krok)
# ==========================================
t_start = 0.0
t_stop = 100.0 # Wydłużyłem czas do 3 sekund, by lepiej widzieć zachowanie sygnałów
dt = 0.0001


# ==========================================
# 5. SYGNAŁ WEJŚCIOWY (Wymuszenie u(t))
# ==========================================
amplituda = 12.0 # Amplituda napięcia w Voltach
czestotliwosc = 2.0 # Częstotliwość w Hz


# ==========================================
# 6. WŁASNY SOLVER NUMERYCZNY (Metoda Eulera)
# ==========================================
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


def generuj_pile(t_start, t_stop, dt, amplituda, czestotliwosc, offset=None):
    """
    Generuje sygnał piłokształtny z przesunięciem (offsetem).
    
    Argumenty:
    t_start       - czas początkowy
    t_stop        - czas końcowy
    dt            - krok czasu
    amplituda     - "wychylenie" sygnału (wartości bazowe od -A do A)
    czestotliwosc - ilość pełnych cykli na sekundę (Hz)
    offset        - domyślnie równy amplitudzie, podnosi sygnał tak, by wartości były >= 0
    """
    okres = 1.0 / czestotliwosc
    liczba_krokow = int(round((t_stop - t_start) / dt)) + 1
    
    # Jeśli brak offsetu, ustawiamy na amplitudę (minimum sygnału ląduje na 0)
    if offset is None:
        offset = amplituda
        
    t_wartosci = [t_start + i * dt for i in range(liczba_krokow)]
    u_wartosci = []
    
    for t in t_wartosci:
        # Faza sygnału (wartość od 0.0 do blisko 1.0)
        faza = (t % okres) / okres
        
        # Generowanie piły (od -1.0 do 1.0), skalowanie i dodanie offsetu
        y = ((-1.0 + 2.0 * faza) * amplituda) + offset
        u_wartosci.append(y)
        
    return t_wartosci, u_wartosci
# ==========================================
# 7. WIZUALIZACJA WYNIKÓW
# ==========================================
#fig, axs = plt.subplots(3, 1, figsize=(10, 8))

#axs[0].plot(czas, u, color='green')
#axs[0].set_title('Sygnał wejściowy: Napięcie u(t) [V]')
#axs[0].grid(True)

#axs[1].plot(czas, i_prad, color='blue')
#axs[1].set_title('Wyjście 1: Prąd w obwodzie i(t) [A]')
#axs[1].grid(True)

#axs[2].plot(czas, omega, color='red')
#axs[2].set_title('Wyjście 2: Prędkość kątowa wału $\omega$(t) [rad/s]')
#axs[2].set_xlabel('Czas [s]')
#axs[2].grid(True)

#plt.tight_layout()
#plt.show()
