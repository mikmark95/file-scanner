import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from gui import FileScannerApp
from update_checker import check_version
from splash_screen import SplashScreen  # Importa la nuova classe SplashScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Funzione per centrare un widget sullo schermo
    def center_widget(widget):
        screen = app.primaryScreen()
        screen_geometry = screen.availableGeometry()
        widget_geometry = widget.frameGeometry()
        widget_geometry.moveCenter(screen_geometry.center())
        widget.move(widget_geometry.topLeft())

    # Crea lo splash screen
    splash = SplashScreen()
    splash.show()
    center_widget(splash)

    # Funzione per avviare la finestra principale dopo 3 secondi
    def start_main():
        global main_window
        splash.close()  # Chiude manualmente lo splash screen
        check_version()  # Eseguiamo il controllo della versione prima di aprire la GUI
        main_window = FileScannerApp()
        main_window.show()
        center_widget(main_window)

    # Avvia la GUI dopo 3 secondi
    QTimer.singleShot(3000, start_main)

    sys.exit(app.exec())
