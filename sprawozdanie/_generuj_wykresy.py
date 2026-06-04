"""Skrypt jednorazowy: generuje wykresy do sprawozdania na podstawie uklad.py.

Uruchomienie z katalogu repozytorium:
    python sprawozdanie/_generuj_wykresy.py
"""

import os
import sys
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from uklad import calka_eulera

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wykresy")
os.makedirs(OUT, exist_ok=True)

PARAMS = dict(
    t_start=0.0, t_stop=5.0, dt=0.001,
    amplituda=12.0, czestotliwosc=1.0, phi=0.0,
    R=2.0, L=0.5, Ke=0.1, Kt=0.1, J=0.02, k=0.1,
)


def rysuj(typ, nazwa, wypelnienie=0.5, czestotliwosc=None):
    p = dict(PARAMS)
    if czestotliwosc is not None:
        p["czestotliwosc"] = czestotliwosc
    czas, u, i_prad, omega = calka_eulera(
        **p, typ_sygnalu=typ, wypelnienie=wypelnienie,
    )

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 5.5), dpi=110)

    ax1.set_title(f"Sygnał wejściowy i prąd – {typ}")
    ax1.plot(czas, u, label="u(t) [V]", color="#1f77b4", alpha=0.7)
    ax1.plot(czas, i_prad, label="i(t) [A]", color="#ff7f0e", linewidth=1.8)
    ax1.set_ylabel("Wartość")
    ax1.legend(loc="upper right")
    ax1.grid(True, linestyle="--", alpha=0.5)

    ax2.set_title("Odpowiedź mechaniczna")
    ax2.plot(czas, omega, label="ω(t) [rad/s]", color="#2ca02c", linewidth=1.8)
    ax2.set_xlabel("Czas [s]")
    ax2.set_ylabel("ω")
    ax2.legend(loc="upper right")
    ax2.grid(True, linestyle="--", alpha=0.5)

    fig.tight_layout(pad=2.0)
    sciezka = os.path.join(OUT, nazwa)
    fig.savefig(sciezka)
    plt.close(fig)
    print(f"  zapisano: {sciezka}")


def main():
    print("Generuję wykresy do sprawozdania:")
    rysuj("sinusoidalny", "odpowiedz_sinus.png")
    rysuj("piłozębny", "odpowiedz_pila.png")
    rysuj("prostokątny", "odpowiedz_prostokat.png", wypelnienie=0.5)
    rysuj("prostokątny", "odpowiedz_prostokat_d025.png", wypelnienie=0.25)


if __name__ == "__main__":
    main()
