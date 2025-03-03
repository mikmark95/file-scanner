# Gestione dell'interfaccia grafica con PyQt6

# gui.py
import sys
import os
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QFileDialog, QMessageBox, QMenuBar, QMenu, QComboBox, QCheckBox
from file_utils import scan_dir, copy_files
from config import autore, versione, icona

class FileScannerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("File Scanner & Copier")
        self.setGeometry(150, 150, 640, 450)
        self.setFixedSize(640, 450)
        self.setWindowIcon(QIcon(icona))

        layout = QVBoxLayout()
        self.input_path = QLineEdit()
        self.output_path = QLineEdit()
        self.comune_input = QLineEdit()
        self.key_input = QLineEdit()
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(["Anno-Mese-Giorno-Orario", "Anno-Mese-Giorno", "Numerico", "Indice progressivo", "Indice random", "Nessuno"])
        self.check_comune = QCheckBox("Includere nome Comune")
        self.check_comune.setChecked(True)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        self.start_button = QPushButton("Avvia")
        self.start_button.clicked.connect(self.start_scan)
        layout.addWidget(self.start_button)
        layout.addWidget(self.log_text)
        self.setLayout(layout)

    def log(self, message):
        self.log_text.append(message)
        QApplication.processEvents()

    def start_scan(self):
        path = self.input_path.text().strip()
        comune = self.comune_input.text().strip()
        key = self.key_input.text().strip()
        path_out = self.output_path.text().strip()
        patt = self.combo_box.currentText().strip()
        check = self.check_comune.isChecked()

        if not all([path, comune, key, path_out]):
            self.log("Errore: tutti i campi devono essere compilati.")
            return

        if not os.path.exists(path) or not os.path.exists(path_out):
            self.log("Errore: percorso non valido.")
            return

        diz_out = {}
        self.log("Avvio scansione...")
        scan_dir(path, comune, key, diz_out, patt, check, self.log)
        self.log(f"Trovati {len(diz_out)} file. Avvio copia...")
        copy_files(diz_out, path_out, self.log)
        self.log("Processo completato!")

