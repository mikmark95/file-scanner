# main.py
import sys
from PyQt6.QtWidgets import QApplication
from gui import FileScannerApp
from update_checker import check_version

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = FileScannerApp()
    window.show()
    check_version()  # Controlla la versione prima di avviare la GUI
    sys.exit(app.exec())
