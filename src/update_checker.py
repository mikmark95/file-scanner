import sys
import requests
import webbrowser
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from config import versione  # Assicurati che 'versione' sia definita in config.py

def check_version():
    # Versione attuale del programma (locale)
    current_version = versione

    # URL del repository GitHub che contiene il file config.py
    repo_url = "https://raw.githubusercontent.com/mikmark95/file-scanner/main/src/config.py"

    # Fai una richiesta HTTP per ottenere il file config.py dal repository GitHub
    response = requests.get(repo_url)

    if response.status_code == 200:
        # Leggi la versione dal file configurazione su GitHub
        remote_config = response.text
        start_index = remote_config.find('versione = "') + len('versione = "')
        end_index = remote_config.find('"', start_index)
        remote_version = remote_config[start_index:end_index]

        # Confronta la versione corrente con quella remota
        if current_version != remote_version:
            print(f"Attenzione! Una nuova versione ({remote_version}) è disponibile.")
            # Creiamo la finestra di dialogo per chiedere se vogliono aggiornare
            ask_update(remote_version)
        else:
            print(f"Il programma è aggiornato alla versione {remote_version}.")
    else:
        print("Errore nel recuperare il file di configurazione da GitHub.")

def ask_update(remote_version):
    # Funzione per mostrare una finestra di dialogo con la richiesta di aggiornamento

    # Crea una finestra di applicazione (necessaria per l'interfaccia grafica)
    app = QApplication(sys.argv)

    # Crea una finestra principale (questa finestra non verrà visualizzata)
    window = QWidget()

    # Crea una finestra di dialogo (MessageBox) per chiedere all'utente se vuole aggiornare
    reply = QMessageBox.question(
        window,  # La finestra principale (non visibile)
        "Nuova versione disponibile",  # Titolo della finestra
        f"Una nuova versione ({remote_version}) è disponibile. Vuoi aggiornare?",  # Messaggio
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # Opzioni di risposta
        QMessageBox.StandardButton.No  # Imposta "No" come predefinito
    )

    # Se l'utente clicca "Sì"
    if reply == QMessageBox.StandardButton.Yes:
        download_url = "https://github.com/mikmark95/file-scanner/releases"  # Modifica con il tuo URL di release
        print(f"Visita questa pagina per scaricare l'ultima versione: {download_url}")
        webbrowser.open(download_url)  # Apre il browser con l'URL di download
    else:
        print("L'aggiornamento è stato annullato.")

    sys.exit(app.exec())  # Avvia l'applicazione PyQt6 e chiudi quando l'utente risponde

if __name__ == "__main__":
    check_version()
