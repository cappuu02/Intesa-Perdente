import tkinter as tk
from tkinter import ttk
from turtle import back
from ttkthemes import ThemedTk
import random
from PIL import Image, ImageTk


def carica_vocabolario():
    try:
        with open('vocabolario.txt', 'r', encoding='utf-8') as file:
            vocabolario = [parola.strip() for parola in file.readlines()]
        return vocabolario
    except FileNotFoundError:
        print("Il file del vocabolario non è stato trovato.")
        return []


class CatenaReazione:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title("Intesa Perdente")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        self.root.configure(bg="black")
        self.tempo_fermo = 0

        # Carica l'immagine di sfondo
        background_image = Image.open("/home/luca/Documenti/Intesa/background.jpg")
        background_image = background_image.resize((500, 300), Image.LANCZOS)  # Utilizza LANCZOS
        self.background_photo = ImageTk.PhotoImage(background_image)

        # Crea un Canvas come base per la finestra principale
        self.canvas = tk.Canvas(self.root, width=500, height=300)
        self.canvas.pack(fill="both", expand=True)

        # Imposta l'immagine di sfondo
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)

        self.parola_label = ttk.Label(self.canvas, text="", font=("Impact", 18), background="#fff600",
                                      foreground="black")
        self.parola_label.pack(pady=20)
        self.parola_label.place(x=252, y=137, anchor='center', height=35)

        # Sposta le etichette "Tempo" e "Punteggio"
        self.timer_label = ttk.Label(self.canvas, text="120", font=("Impact", 15), background="white",
                                     foreground="black")
        self.timer_label.place(x=96, y=125)

        self.punteggio_label = ttk.Label(self.canvas, text="0", font=("Impact", 15), background="white",
                                         foreground="black")
        self.punteggio_label.place(x=382, y=125)

        # Configura i bottoni con stile diverso

        self.stop_button = tk.Button(self.canvas, text="Ferma", command=self.ferma_gioco, relief="flat", bd=0,
                                     font=("Impact", 15), background="white", foreground="black")
        self.stop_button.place(x=6, y=237, width=110, height=35)

        self.riprendi_button = tk.Button(self.canvas, text="Riprendi", command=self.riprendi_gioco, relief="flat", bd=0,
                                         font=("Impact", 15), foreground="black")
        self.riprendi_button.place(x=132, y=237, width=110, height=35)

        self.next_word_button = tk.Button(self.canvas, text="→", command=self.aggiorna_parola, relief="flat", bd=0,
                                          font=("Impact", 15), foreground="black")
        self.next_word_button.place(x=384, y=237, width=110, height=35)

        self.piu_punto_button = tk.Button(self.canvas, text="+1", command=self.aumenta_punteggio, relief="flat", bd=0,
                                          font=("Impact", 15), foreground="white", background="#29d51c")
        self.piu_punto_button.place(x=50, y=250, width=100, height=40)

        self.meno_punto_button = tk.Button(self.canvas, text="-1", command=self.diminuisci_punteggio, relief="flat",
                                           bd=0, font=("Impact", 15), foreground="white", background="#ea1919")
        self.meno_punto_button.place(x=350, y=250, width=100, height=40)

        self.meno_punto_button.place(x=171, y=203, anchor='center', width=40,
                                     height=40)  # Posiziona il pulsante -1 a sinistra
        self.piu_punto_button.place(x=329, y=203, anchor='center', width=40,
                                    height=40)  # Posiziona il pulsante +1 a destra

        self.start_button = tk.Button(self.canvas, text="Inizia", command=self.inizia_gioco, relief="flat", bd=0,
                                      font=("Impact", 15), foreground="black")
        self.start_button.place(x=258, y=237, width=110, height=35)

        self.timer_countdown = 120
        self.punteggio = 0
        self.in_gioco = False
        self.inizia_premuto = False

        self.vocabolario = carica_vocabolario()
        self.vocabolario_usato = []

        self.stop_button.config(state=tk.DISABLED)
        self.riprendi_button.config(state=tk.DISABLED)
        self.next_word_button.config(state=tk.DISABLED)
        self.piu_punto_button.config(state=tk.DISABLED)
        self.meno_punto_button.config(state=tk.DISABLED)

    def aggiorna_parola(self):
        if self.vocabolario:
            if not self.vocabolario_usato:
                self.vocabolario_usato = self.vocabolario.copy()

            parola_random = random.choice(self.vocabolario_usato)
            self.vocabolario_usato.remove(parola_random)

            self.parola_label.config(text=parola_random)
        else:
            self.parola_label.config(text="Vocabolario vuoto")

    def resize_image(image_path, width, height):
        original_image = Image.open(image_path)
        resized_image = original_image.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_image)

    def inizia_gioco(self):
        self.in_gioco = True
        self.inizia_premuto = True
        self.timer_countdown = 120  # Imposta il tempo a 120 secondi
        self.aggiorna_parola()
        self.aggiorna_timer()

        self.start_button.place_forget()

        self.stop_button.config(state=tk.NORMAL)
        self.riprendi_button.config(state=tk.DISABLED)
        self.next_word_button.config(state=tk.NORMAL)
        self.piu_punto_button.config(state=tk.NORMAL)
        self.meno_punto_button.config(state=tk.NORMAL)

    def ferma_gioco(self):
        self.in_gioco = False
        self.timer_label.config(text=f"{self.timer_countdown}")
        self.tempo_fermo = self.timer_countdown  # Memorizza il tempo rimanente quando si ferma il gioco

        self.stop_button.config(state=tk.DISABLED)
        self.riprendi_button.config(state=tk.NORMAL)
        self.next_word_button.config(state=tk.NORMAL)
        self.piu_punto_button.config(state=tk.NORMAL)
        self.meno_punto_button.config(state=tk.NORMAL)

    def riprendi_gioco(self):
        if self.tempo_fermo > 0:  # Se c'è del tempo rimanente, riprendi il gioco
            self.in_gioco = True
            self.timer_countdown = self.tempo_fermo
            self.tempo_fermo = 0  # Resetta il tempo fermo
            self.aggiorna_timer()

            self.riprendi_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.next_word_button.config(state=tk.NORMAL)
            self.piu_punto_button.config(state=tk.NORMAL)
            self.meno_punto_button.config(state=tk.NORMAL)

            self.start_button.place_forget()

    def aggiorna_timer(self):
        if self.in_gioco and self.timer_countdown > 0:
            self.timer_label.config(text=f"{self.timer_countdown}")
            self.timer_countdown -= 1
            self.root.after(1000, self.aggiorna_timer)
        elif self.in_gioco:
            self.timer_label.config(text="X")
            self.in_gioco = False

            self.stop_button.config(state=tk.DISABLED)
            self.riprendi_button.config(state=tk.DISABLED)
            self.next_word_button.config(state=tk.DISABLED)
            self.piu_punto_button.config(state=tk.DISABLED)
            self.meno_punto_button.config(state=tk.DISABLED)

            self.start_button.place(x=258, y=237, width=110, height=35)
            self.start_button.config(state=tk.NORMAL)

    def gestisci_punteggio(self, incremento):
        self.punteggio += incremento
        if self.punteggio < 0:
            self.punteggio = 0
        self.punteggio_label.config(text=f"{self.punteggio}")

    def aumenta_punteggio(self):
        if self.in_gioco or not self.in_gioco:
            self.gestisci_punteggio(1)

    def diminuisci_punteggio(self):
        if self.in_gioco or not self.in_gioco:
            self.gestisci_punteggio(-1)

    def run(self):
        self.root.mainloop()


# Creazione dell'istanza del gioco
catena_reazione = CatenaReazione()
catena_reazione.run()
