import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from gui import FileScannerApp
from file_utils import center_widget
from update_checker import check_version
from splash_screen import SplashScreen  # Importa la nuova classe SplashScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Funzione per centrare un widget sullo schermo

    # Crea lo splash screen
    splash = SplashScreen()
    splash.show()
    center_widget(app,splash)

    # Funzione per avviare la finestra principale dopo 3 secondi
    def start_main():
        global main_window
        splash.close()  # Chiude manualmente lo splash screen
        check_version()  # Eseguiamo il controllo della versione prima di aprire la GUI
        main_window = FileScannerApp()

        # Centra la finestra principale prima di mostrarla
        center_widget(app,main_window)

        # Mostra la finestra principale
        main_window.show()

    # Avvia la GUI dopo 3 secondi
    QTimer.singleShot(3000, start_main)

    sys.exit(app.exec())
