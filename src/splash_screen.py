import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QUrl


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        # 🔹 Rendi la finestra senza bordi e sempre in primo piano
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(640,450)

        # 🔹 Trova il percorso del video, compatibile con PyInstaller
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  # Quando eseguito da PyInstaller
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Quando eseguito normalmente

        video_path = os.path.join(base_path, "assets", "splash.mp4")

        # 🔹 Verifica che il file esista
        if not os.path.exists(video_path):
            print(f"❌ Errore: Video non trovato! Percorso: {video_path}")
            return

        # 🔹 Creazione del player video
        self.video_widget = QVideoWidget(self)
        self.video_widget.setStyleSheet("background: transparent;")

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)
        self.player.setSource(QUrl.fromLocalFile(video_path))

        # ✅ Avvia il video
        self.player.play()

        # 🔹 Imposta il layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.video_widget)
        self.setLayout(layout)

        # ✅ Imposta la dimensione della finestra
        self.resize(640, 450)  # Puoi modificare in base al video

        # ✅ Chiudi lo splash screen alla fine del video
        self.player.mediaStatusChanged.connect(self.on_video_finished)

    def on_video_finished(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.close_splash()

    def close_splash(self):
        """Chiude lo splash screen."""
        self.player.stop()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec())
