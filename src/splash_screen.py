from PyQt6.QtWidgets import QSplashScreen, QLabel
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt

def create_splash():
    """Crea e restituisce lo Splash Screen con una GIF animata."""
    splash = QSplashScreen()
    splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)

    # Carica la GIF animata
    label = QLabel(splash)
    movie = QMovie("assets/logo_animato.gif")  # Assicurati che il percorso sia corretto
    label.setMovie(movie)
    movie.start()

    # Adatta la finestra alla dimensione della GIF
    splash.resize(movie.frameRect().size())
    label.setGeometry(0, 0, splash.width(), splash.height())

    return splash
