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
# 2. INTERFEJS UŻYTKOWNIKA 
# ==========================================
print("--- SYMULATOR SILNIKA ELEKTRYCZNEGO ---")
nowe_R = input(f"Podaj nową wartość rezystancji R (obecnie {R} Ohm) lub wciśnij Enter, aby zostawić domyślną: ")
if nowe_R.strip(): 
    R = float(nowe_R)

print("\nWybierz rodzaj sygnału wejściowego u(t):")
print("1. Sinusoidalny")
print("2. Prostokątny skończony (wypełnienie 50%)")
print("3. Piłozębny")
wybor_sygnalu = input("Twój wybór (1/2/3): ")

print(f"\nRozpoczynam symulację z R = {R} Ohm...\n")

# ==========================================
# 3. USTAWIENIA SYMULACJI (Czas i Krok)
# ==========================================
t_start = 0.0
t_stop = 100.0 # Wydłużyłem czas do 3 sekund, by lepiej widzieć zachowanie sygnałów
dt = 0.0001
N = int((t_stop - t_start) / dt)

czas = np.linspace(t_start, t_stop, N)

# ==========================================
# 4. INICJALIZACJA ZMIENNYCH STANU
# ==========================================
i_prad = np.zeros(N)
omega = np.zeros(N)
theta = np.zeros(N)

# ==========================================
# 5. SYGNAŁ WEJŚCIOWY (Wymuszenie u(t))
# ==========================================
amplituda = 12.0 # Amplituda napięcia w Voltach
czestotliwosc = 2.0 # Częstotliwość w Hz

u = np.zeros(N)

if wybor_sygnalu == '1':
    # Sygnał sinusoidalny
    u = amplituda * np.sin(2 * np.pi * czestotliwosc * czas)

elif wybor_sygnalu == '2':
    # Sygnał prostokątny o wypełnieniu 50% (duty=0.5 to domyślne dla signal.square)
    # Zwraca wartości od -1 do 1, chcemy od 0 do amplitudy:
    u_ciagly = amplituda * (signal.square(2 * np.pi * czestotliwosc * czas, duty=0.5) > 0)
    
    # Robimy go SKOŃCZONYM (np. wyłączamy go po 1.5 sekundy)
    u = np.where(czas <= 1.5, u_ciagly, 0.0)

elif wybor_sygnalu == '3':
    # Sygnał piłozębny
    u = amplituda * signal.sawtooth(2 * np.pi * czestotliwosc * czas)

else:
    print("Niepoprawny wybór. Wczytuję domyślny skok jednostkowy.")
    u[czas >= 0.1] = amplituda

# ==========================================
# 6. WŁASNY SOLVER NUMERYCZNY (Metoda Eulera)
# ==========================================
for n in range(N - 1):
    di_dt = (1/L) * (u[n] - R * i_prad[n] - Ke * omega[n])
    domega_dt = (1/J) * (Kt * i_prad[n] - k * theta[n])
    dtheta_dt = omega[n]
    
    i_prad[n+1] = i_prad[n] + di_dt * dt
    omega[n+1] = omega[n] + domega_dt * dt
    theta[n+1] = theta[n] + dtheta_dt * dt

# ==========================================
# 7. WIZUALIZACJA WYNIKÓW
# ==========================================
fig, axs = plt.subplots(3, 1, figsize=(10, 8))

axs[0].plot(czas, u, color='green')
axs[0].set_title('Sygnał wejściowy: Napięcie u(t) [V]')
axs[0].grid(True)

axs[1].plot(czas, i_prad, color='blue')
axs[1].set_title('Wyjście 1: Prąd w obwodzie i(t) [A]')
axs[1].grid(True)

axs[2].plot(czas, omega, color='red')
axs[2].set_title('Wyjście 2: Prędkość kątowa wału $\omega$(t) [rad/s]')
axs[2].set_xlabel('Czas [s]')
axs[2].grid(True)

plt.tight_layout()
plt.show()