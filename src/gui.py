# Gestione dell'interfaccia grafica con PyQt6
import shutil
# gui.py
import sys
import os
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QFileDialog, \
    QMessageBox, QMenuBar, QMenu, QComboBox, QCheckBox, QHBoxLayout
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
        self.setWindowIcon(QIcon(r"lock.ico"))

        # Applica il foglio di stile (QSS)
        self.setStyleSheet("""
                   QWidget {
                       background-color: #374048;
                       color: white;
                       font-size: 14px;
                   }

                   QPushButton {
                       background-color: #B7BFC8;
                       color: white;
                       border-radius: 5px;
                       padding: 5px;
                   }

                   QPushButton:hover {
                       background-color: #81A1C1;
                   }

                   QLineEdit {
                       background-color: white;
                       font-size: 14px;
                       color: #374048;
                   }

                   QMenuBar {
                       background-color: #6F7F90;
                       font-size: 14px;
                   }
               """)

        layout = QVBoxLayout()

        # Creazione della barra menu
        menubar = QMenuBar(self)
        info_menu = menubar.addMenu("Info")
        about_action = info_menu.addAction("Informazioni")
        about_action.triggered.connect(self.show_about)

        funzione_menu = menubar.addMenu("Funzione")
        function_action = funzione_menu.addAction("Descrizione")
        function_action.triggered.connect(self.show_function)

        layout.setMenuBar(menubar)

        input_layout = QHBoxLayout()
        self.input_path_label = QLabel("Percorso di input:")
        input_layout.addWidget(self.input_path_label)
        self.input_path = QLineEdit()
        self.input_path.setFixedWidth(375)
        input_layout.addWidget(self.input_path)
        self.browse_input_button = QPushButton("Sfoglia")
        self.browse_input_button.clicked.connect(self.browse_input)
        input_layout.addWidget(self.browse_input_button)
        layout.addLayout(input_layout)

        comune_layout = QHBoxLayout()
        self.comune_label = QLabel("Nome comune:")
        comune_layout.addWidget(self.comune_label)
        self.comune_input = QLineEdit()
        self.comune_input.setFixedWidth(496)
        comune_layout.addWidget(self.comune_input)
        layout.addLayout(comune_layout)

        check_layout = QHBoxLayout()
        check_layout.addSpacing(123)
        self.check_comune = QCheckBox("Includere nome Comune")
        self.check_comune.setChecked(True)
        self.check_comune.stateChanged.connect(self.checkbox_changed)
        check_layout.addWidget(self.check_comune)
        layout.addLayout(check_layout)

        key_layout = QHBoxLayout()
        self.key_label = QLabel("Chiave di ricerca:")
        key_layout.addWidget(self.key_label)
        self.key_input = QLineEdit()
        self.key_input.setFixedWidth(496)
        key_layout.addWidget(self.key_input)
        layout.addLayout(key_layout)

        combo_layout = QHBoxLayout()
        self.combo_label = QLabel("Seleziona Pattern:")
        combo_layout.addWidget(self.combo_label)
        self.combo_box = QComboBox(self)
        self.combo_box.setFixedWidth(496)
        self.combo_box.addItems(
            ["Anno-Mese-Giorno-Orario", "Anno-Mese-Giorno", "Numerico", "Indice progressivo", "Indice random",
             "Nessuno"])
        self.combo_box.setStyleSheet("QComboBox { text-align: center; }")
        combo_layout.addWidget(self.combo_box)
        layout.addLayout(combo_layout)

        output_layout = QHBoxLayout()
        self.output_path_label = QLabel("Percorso di output:")
        output_layout.addWidget(self.output_path_label)
        self.output_path = QLineEdit()
        self.output_path.setFixedWidth(385)
        output_layout.addWidget(self.output_path)
        self.browse_output_button = QPushButton("Sfoglia")
        self.browse_output_button.clicked.connect(self.browse_output)
        output_layout.addWidget(self.browse_output_button)
        layout.addLayout(output_layout)

        self.start_button = QPushButton("Avvia")
        self.start_button.clicked.connect(self.start_scan)
        layout.addWidget(self.start_button)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        # Pulsante per salvare il log
        button_layout = QHBoxLayout()
        self.save_log_button = QPushButton("Salva Log")
        self.save_log_button.clicked.connect(self.save_log)
        button_layout.addWidget(self.save_log_button)

        # Pulsante per pulire i campi e il log
        self.clear_button = QPushButton("Pulisci")
        self.clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browse_input(self):
        path = QFileDialog.getExistingDirectory(self, "Seleziona Cartella di Input")
        if path:
            self.input_path.setText(path)

    def browse_output(self):
        path = QFileDialog.getExistingDirectory(self, "Seleziona Cartella di Output")
        if path:
            self.output_path.setText(path)

    def log(self, message):
        self.log_text.append(message)
        QApplication.processEvents()

    def show_about(self):
        QMessageBox.information(self, "Informazioni", f"File Scanner & Copier\nVersione: {versione}\nAutore: {autore}")

    def show_function(self):
        QMessageBox.information(self, "Funzione",
                                ""
                                "Programma che serve per ricercare ricorsivamente all'interno di un percorso di input, tutti i file che contengono le chiavi di ricerca nel nome."
                                "\nSe checkbox attivata restituisce i file rinominati nel seguente modo:"
                                "\n\t---> (nome_comune)_(Pattern)_file."
                                "\n Altrimenti:"
                                "\n\t---> (Pattern)_file")

    def checkbox_changed(self, state):
        if state == 2:  # Qt.Checked è rappresentato dal valore 2
            return 2
        else:
            return 1

    def save_log(self):
        # Apre la finestra di dialogo per scegliere il percorso del file
        file_path, _ = QFileDialog.getSaveFileName(self, "Salva Log", "", "File di Testo (*.txt);;Tutti i file (*)")

        if file_path:
            try:
                # Salva il log nel file selezionato
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.log_text.toPlainText())
                QMessageBox.information(self, "Successo", "Log salvato con successo!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Si è verificato un errore durante il salvataggio:\n{str(e)}")

    def clear_fields(self):
        # Pulisce i campi di input
        self.input_path.clear()
        self.comune_input.clear()
        self.key_input.clear()
        self.output_path.clear()
        self.combo_box.setCurrentIndex(0)  # Imposta la combo box al primo elemento (default)
        self.check_comune.setChecked(True)  # Ripristina il checkbox a "selezionato"

        # Svuota il log
        self.log_text.clear()

    def start_scan(self):
        path = self.input_path.text().strip()
        comune = self.comune_input.text().strip()
        key = self.key_input.text().strip()
        path_out = self.output_path.text().strip()
        patt = self.combo_box.currentText().strip()
        check = self.check_comune.isChecked()

        if check:
            if not all([path, comune, key, path_out]):
                self.log("Errore: tutti i campi devono essere compilati.")
                return

        if not os.path.exists(path):
            self.log("Errore: il percorso di input non esiste.")
            return
        if not key:
            self.log("Errore: chiave di ricerca non inserita.")
            return
        if not os.path.exists(path_out):
            self.log("Errore: il percorso di output non esiste.")
            return

        diz_out = {}
        self.log("Avvio scansione...")
        self.log(f"Includere nome Comune: {check}")
        self.log(f"Pattern usato: {patt}")

        self.scan_dir(path, comune, key, diz_out, patt, check)

        self.log("\nTUTTI GLI ELEMENTI SONO STATI CONTROLLATI")
        self.log(f"Sono stati trovati {len(diz_out)} file\n")
        self.log("Inizio con la copia dei file\n")

        for chiave, elem in diz_out.items():
            dest = os.path.join(path_out, chiave)
            shutil.copy2(elem, dest)
            self.log(f"Copia in corso: {elem} --> {dest}")
            self.log('')

        self.log("Processo TERMINATO!!!")