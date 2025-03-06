# Gestione dell'interfaccia grafica con PyQt6

import shutil
import os
import sys
import webbrowser
import requests
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QFileDialog, \
    QMessageBox, QMenuBar, QMenu, QComboBox, QCheckBox, QHBoxLayout, QSystemTrayIcon
from config import autore, versione, icona
from file_utils import scan_dir
from update_checker import check_version

class FileScannerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("File Scanner & Copier")
        self.setGeometry(150, 150, 640, 450)
        self.setFixedSize(640, 450)


        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Cartella dello script
        ico_path = os.path.join(base_path, "assets", "github.ico")
        self.setWindowIcon(QIcon(ico_path))

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
                   QMenu::item {
                       background-color: #6F7F90;  
                       color: white;  
                       padding: 5px;  
                   }

               """)

        layout = QVBoxLayout()

        # Creazione della barra menu
        menubar = QMenuBar(self)
        info_menu = menubar.addMenu("Info")
        guida_action = info_menu.addAction("Guida")
        guida_action.triggered.connect(self.guida_function)
        about_action = info_menu.addAction("Versione")
        about_action.triggered.connect(self.show_about)

        supporto_menu = menubar.addMenu("Supporto")
        supporto_action = supporto_menu.addAction("Invia Mail")
        supporto_action.triggered.connect(self.send_email)

        update_menu = menubar.addMenu("Aggiornamento")
        update_action = update_menu.addAction("Verifica aggiornamento")
        update_action.triggered.connect(self.check_update)

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

        prefisso_layout = QHBoxLayout()
        self.prefisso_label = QLabel("Prefisso:")
        prefisso_layout.addWidget(self.prefisso_label)
        self.prefisso_input = QLineEdit()
        self.prefisso_input.setFixedWidth(496)
        prefisso_layout.addWidget(self.prefisso_input)
        layout.addLayout(prefisso_layout)

        check_layout = QHBoxLayout()
        check_layout.addSpacing(123)
        self.check_prefisso = QCheckBox("Includere prefisso")
        self.check_prefisso.setChecked(True)
        self.check_prefisso.stateChanged.connect(self.checkbox_changed)
        check_layout.addWidget(self.check_prefisso)
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
            ["Anno-Mese-Giorno-Orario", "Anno-Mese-Giorno", "Numerico", "Indice progressivo", "Indice random", "Personalizzato",
             "Nessuno"])
        self.combo_box.setStyleSheet("QComboBox { text-align: center; }")
        self.combo_box.setCurrentIndex(self.combo_box.count() - 1)
        combo_layout.addWidget(self.combo_box)
        layout.addLayout(combo_layout)

        personalized_layout = QHBoxLayout()
        self.personalized_label = QLabel("Inserire pattern:")
        personalized_layout.addWidget(self.personalized_label)
        self.personalized_input = QLineEdit()
        self.personalized_input.setFixedWidth(494)
        personalized_layout.addWidget(self.personalized_input)
        self.personalized_label.setVisible(False)
        self.personalized_input.setVisible(False)
        layout.addLayout(personalized_layout)

        # Segnale per cambiare visibilità della QLineEdit
        self.combo_box.currentTextChanged.connect(self.toggle_line_edit)


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

    def check_update(self):
        """Chiama il controllo aggiornamenti con il contesto della finestra principale."""
        check_version(self)

    def send_email(self):
        """Apre il client email predefinito con un template precompilato."""
        destinatario = "michele-marchetti@hotmail.it"
        oggetto = "Report Bug - FILE SCANNER"
        corpo = "Ciao,\n\nHo riscontrato il seguente bug:\n\n[Spiegazione Sommaria Bug]\n\n[Cosa stavi cercando mentre si è presentato il bug]\n\n[ESEMPIO PARAMETRI INSERITI]\n\nSaluti!"

        # Formattazione della stringa mailto (sostituire gli spazi con %20 e le nuove righe con %0A)
        mailto_link = f"mailto:{destinatario}?subject={oggetto}&body={corpo}".replace(" ", "%20").replace("\n", "%0A")

        # Aprire il client di posta
        webbrowser.open(mailto_link)


    def toggle_line_edit(self, text):
        """Mostra la QLineEdit solo se viene selezionata una certa opzione."""
        if text == "Personalizzato":  # Cambia "Altro" con l'opzione desiderata
            self.personalized_label.setVisible(True)
            self.personalized_input.setVisible(True)
        else:
            self.personalized_label.setVisible(False)
            self.personalized_input.setVisible(False)

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

    def guida_function(self):
        webbrowser.open_new(r"https://github.com/mikmark95/file-scanner/blob/main/README.md")


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
        self.prefisso_input.clear()
        self.key_input.clear()
        self.output_path.clear()
        self.combo_box.setCurrentIndex(self.combo_box.count() - 1)  # Imposta la combo box al primo elemento (default)
        self.check_prefisso.setChecked(True)  # Ripristina il checkbox a "selezionato"
        self.personalized_input.clear()



        # Svuota il log
        self.log_text.clear()

    def start_scan(self):
        path = self.input_path.text().strip()
        prefisso = self.prefisso_input.text().strip()
        key = self.key_input.text().strip()
        path_out = self.output_path.text().strip()
        patt = self.combo_box.currentText().strip()
        check = self.check_prefisso.isChecked()
        if self.personalized_input.isVisible():
            patt = self.personalized_input.text().strip()

        if check:
            if not all([path, prefisso, key, path_out]):
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
        self.log(f"Includere prefisso: {check}")
        self.log(f"Pattern usato: {patt}")
        self.log(f"Scansione file in corso...")
        scan_dir(path, prefisso, key, diz_out, patt, check, self.log_text)

        self.log("\nTUTTI GLI ELEMENTI SONO STATI CONTROLLATI")
        self.log(f"Sono stati trovati {len(diz_out)} file\n")
        self.log("Inizio con la copia dei file\n")

        for chiave, elem in diz_out.items():
            dest = os.path.join(path_out, chiave)
            try:
                self.log(f"Copia in corso: {elem} --> {dest}")
                self.log('')
                shutil.copy2(elem, dest)
            except Exception as e:
                self.log(f"Errore: {e}")
                self.log(f'Probailmente Patter Personalizzato ERRATO')

        self.log("Processo TERMINATO!!!")
        self.log('-----------------------------------------------------------------------------------------------')
        self.log('')