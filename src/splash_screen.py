import sys
import os
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QTimer

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        # 🔹 Rendi la finestra senza bordi e sempre in primo piano
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        # 🔹 Trova il percorso della GIF, compatibile con PyInstaller
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  # Quando eseguito da PyInstaller
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Quando eseguito normalmente

        gif_path = os.path.join(base_path, "assets", "splash.gif")

        # 🔹 Verifica che il file esista
        if not os.path.exists(gif_path):
            print(f"❌ Errore: GIF non trovata! Percorso: {gif_path}")
            return

        # 🔹 Creazione di una QLabel per mostrare la GIF animata
        self.label = QLabel(self)
        self.movie = QMovie(gif_path)  # Creiamo un oggetto QMovie per la GIF

        # ✅ Verifica che la GIF sia valida
        if not self.movie.isValid():
            print("❌ Errore: GIF non valida!")
            return

        # ✅ Imposta la GIF su QLabel e avviala
        self.label.setMovie(self.movie)
        self.movie.setCacheMode(QMovie.CacheMode.CacheAll)  # Usa cache per evitare lag
        self.movie.setSpeed(100)  # Imposta la velocità normale
        self.movie.start()  # Avvia la GIF

        # 🔹 Imposta il layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # ✅ Imposta la dimensione della finestra alla dimensione della GIF
        self.resize(self.movie.frameRect().size())

    def close_splash(self):
        """Chiude lo splash screen."""
        self.movie.stop()  # Ferma la GIF prima di chiudere
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()

    # ✅ Usa QTimer per chiudere lo splash dopo 3 secondi SENZA bloccare l'interfaccia
    QTimer.singleShot(3000, splash.close_splash)

    sys.exit(app.exec())


