import customtkinter as ctk
import tkinter.messagebox as messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importujemy Twoją funkcję z pliku uklad.py
from uklad import calka_eulera

# Konfiguracja wyglądu CustomTkinter
ctk.set_appearance_mode("System")  # Tryb jasny/ciemny zależnie od systemu
ctk.set_default_color_theme("blue")

class SymulacjaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Symulacja Silnika DC")
        self.geometry("1100x700")

        # --- Podział okna na panel boczny (UI) i główny (Wykresy) ---
        self.panel_ui = ctk.CTkFrame(self, width=300)
        self.panel_ui.pack(side="left", fill="y", padx=10, pady=10)

        self.panel_wykresu = ctk.CTkFrame(self)
        self.panel_wykresu.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # --- Tworzenie pól do wprowadzania parametrów ---
        ctk.CTkLabel(self.panel_ui, text="Parametry Symulacji", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 20))

        # Słownik, w którym będziemy trzymać obiekty pól tekstowych
        self.pola_tekstowe = {}

        # Lista parametrów: (nazwa_zmiennej, etykieta_w_gui, wartosc_domyslna)
        parametry_konfig = [
            ("t_start", "Czas start [s]", "0.0"),
            ("t_stop", "Czas stop [s]", "5.0"),
            ("dt", "Krok czasu dt [s]", "0.001"),
            ("amplituda", "Amplituda napięcia [V]", "12.0"),
            ("czestotliwosc", "Częstotliwość [Hz]", "1.0"),
            ("phi", "Przesunięcie fazowe [rad]", "0.0"),
            ("wypelnienie", "Wypełnienie [0-1]", "0.5"),
            ("R", "Rezystancja R [Ohm]", "2.0"),
            ("L", "Indukcyjność L [H]", "0.5"),
            ("Ke", "Stała nap. Ke", "0.1"),
            ("Kt", "Stała mom. Kt", "0.1"),
            ("J", "Bezwładność J", "0.02"),
            ("k", "Wsp. tarcia k", "0.1")
        ]

        # Generowanie etykiet i pól tekstowych w pętli
        for klucz, etykieta, domyslna in parametry_konfig:
            frame_param = ctk.CTkFrame(self.panel_ui, fg_color="transparent")
            frame_param.pack(fill="x", pady=2, padx=10)
            
            lbl = ctk.CTkLabel(frame_param, text=etykieta, width=130, anchor="w")
            lbl.pack(side="left")
            
            entry = ctk.CTkEntry(frame_param, width=80)
            entry.insert(0, domyslna)
            entry.pack(side="right")
            
            self.pola_tekstowe[klucz] = entry
            if klucz == "wypelnienie":
                self.frame_wypelnienie = frame_param
                self.entry_wypelnienie = entry

        # Typ sygnału wejściowego
        frame_typ_sygnalu = ctk.CTkFrame(self.panel_ui, fg_color="transparent")
        frame_typ_sygnalu.pack(fill="x", pady=8, padx=10)

        ctk.CTkLabel(frame_typ_sygnalu, text="Typ sygnału:", width=130, anchor="w").pack(side="left")
        self.typ_sygnalu_var = ctk.StringVar(value="sinusoidalny")
        self.option_typ_sygnalu = ctk.CTkOptionMenu(
            frame_typ_sygnalu,
            values=["sinusoidalny", "prostokątny", "piłozębny"],
            variable=self.typ_sygnalu_var,
            width=120
        )
        self.option_typ_sygnalu.pack(side="right")

        # Pole wypełnienia sygnału prostokątnego jest tworzone w pętli parametrów
        self.typ_sygnalu_var.trace_add("write", self.on_typ_sygnalu_change)

        # Przycisk uruchamiający symulację
        self.btn_generuj = ctk.CTkButton(self.panel_ui, text="Generuj Symulację", command=self.uruchom_symulacje)
        self.btn_generuj.pack(pady=30)

        # --- Przygotowanie Matplotlib ---
        self.fig = Figure(figsize=(8, 6), dpi=100)
        # Tworzymy dwa wykresy jeden pod drugim (2 wiersze, 1 kolumna)
        self.ax1 = self.fig.add_subplot(211) # Napięcie i prąd
        self.ax2 = self.fig.add_subplot(212) # Prędkość kątowa
        self.fig.tight_layout(pad=3.0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.panel_wykresu)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.on_typ_sygnalu_change()

        # Uruchomienie pierwszej symulacji na starcie
        self.uruchom_symulacje()

    def on_typ_sygnalu_change(self, *args):
        if self.typ_sygnalu_var.get() == "prostokątny":
            self.frame_wypelnienie.pack(fill="x", pady=8, padx=10)
        else:
            self.frame_wypelnienie.pack_forget()

    def uruchom_symulacje(self):
        try:
            # 1. Pobranie i konwersja wartości wpisanych przez użytkownika na liczby zmiennoprzecinkowe (float)
            p = {klucz: float(pole.get()) for klucz, pole in self.pola_tekstowe.items()}

            wypelnienie = float(self.pola_tekstowe["wypelnienie"].get())

            # 2. Wywołanie Twojej metody z uklad.py
            czas, u, i_prad, omega = calka_eulera(
                p["t_start"], p["t_stop"], p["dt"], 
                p["amplituda"], p["czestotliwosc"], 
                p["R"], p["L"], p["Ke"], p["Kt"], p["J"], p["k"],
                self.typ_sygnalu_var.get(), wypelnienie, p["phi"]
            )

            # 3. Aktualizacja górnego wykresu (Napięcie wymuszające i Prąd)
            self.ax1.clear()
            self.ax1.set_title("Sygnał wejściowy i Prąd")
            self.ax1.plot(czas, u, label="Napięcie u(t) [V]", color="blue", alpha=0.7)
            self.ax1.plot(czas, i_prad, label="Prąd i(t) [A]", color="orange", linewidth=2)
            self.ax1.set_ylabel("Wartość")
            self.ax1.legend()
            self.ax1.grid(True, linestyle='--', alpha=0.6)

            # 4. Aktualizacja dolnego wykresu (Prędkość kątowa)
            self.ax2.clear()
            self.ax2.set_title("Odpowiedź mechaniczna")
            self.ax2.plot(czas, omega, label="Prędkość kątowa ω(t) [rad/s]", color="green", linewidth=2)
            self.ax2.set_xlabel("Czas [s]")
            self.ax2.set_ylabel("Prędkość ω")
            self.ax2.legend()
            self.ax2.grid(True, linestyle='--', alpha=0.6)

            # 5. Odświeżenie płótna Matplotlib
            self.canvas.draw()

        except ValueError:
            # Komunikat błędu, jeśli użytkownik wpisze np. "abc" zamiast liczby
            messagebox.showerror("Błąd danych", "Upewnij się, że wszystkie parametry są poprawnymi liczbami (używaj kropki, nie przecinka).")
        except Exception as e:
            messagebox.showerror("Błąd symulacji", f"Wystąpił nieoczekiwany błąd:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Błąd symulacji", f"Wystąpił nieoczekiwany błąd:\n{str(e)}")

# Uruchomienie aplikacji
if __name__ == "__main__":
    app = SymulacjaApp()
    app.mainloop()