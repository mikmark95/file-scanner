# main.py
import sys
from PyQt6.QtWidgets import QApplication
from gui import FileScannerApp
from update_checker import check_for_update

if __name__ == "__main__":
    check_for_update()  # Controlla la versione prima di avviare la GUI

    app = QApplication(sys.argv)
    window = FileScannerApp()
    window.show()
    sys.exit(app.exec())
