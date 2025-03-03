# Avvio dell'applicazione

# main.py
import sys
from PyQt6.QtWidgets import QApplication
from gui import FileScannerApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileScannerApp()
    window.show()
    sys.exit(app.exec())
