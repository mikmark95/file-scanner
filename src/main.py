import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from gui import FileScannerApp
from update_checker import check_version
from splash_screen import create_splash

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
    splash = create_splash()
    if splash is None:
        print("❌ Splash screen non caricato, avvio diretto della GUI.")
        check_version()
        main_window = FileScannerApp()
        main_window.show()
        center_widget(main_window)
        sys.exit(app.exec())

    # Mostra e centra lo splash screen
    splash.show()
    center_widget(splash)



    # Funzione per avviare la finestra principale dopo 3 secondi
    def start_main():
        global main_window
        main_window = FileScannerApp()
        main_window.show()
        center_widget(main_window)
        splash.finish(main_window)

    # Avvia la GUI dopo 2000 ms (2 secondi)
    QTimer.singleShot(2000, start_main)
    # Esegui il controllo versione
    check_version()

    sys.exit(app.exec())
