import sys
from PyQt6.QtWidgets import QApplication, QSplashScreen, QLabel
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt
import os

def create_splash():
    """Crea uno splash screen con una GIF animata in PyQt6."""
    # Crea una finestra splash senza immagine iniziale
    splash = QSplashScreen()
    splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
    print(os.getcwd())
    # Trova il percorso assoluto della GIF
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Cartella dello script
    gif_path = os.path.join(base_path,"assets", "loading.gif")

    # Verifica che il file esista
    if not os.path.exists(gif_path):
        print(f"❌ Errore: GIF non trovata! Percorso: {gif_path}")
        return None

    # Crea un QLabel e assegna la GIF con QMovie
    label = QLabel(splash)
    movie = QMovie(gif_path)

    # Verifica se la GIF è valida
    if not movie.isValid():
        print(f"❌ Errore: GIF non valida o non supportata!")
        return None

    label.setMovie(movie)
    movie.start()

    # Imposta la dimensione della finestra per adattarsi alla GIF
    splash.resize(movie.frameRect().size())

    # Mostra lo splash screen
    splash.show()

    return splash


