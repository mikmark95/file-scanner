import importlib
import requests
import webbrowser
from config import versione


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
            # Apri la pagina di download della versione più recente su GitHub
            download_url = "https://github.com/mikmark95/file-scanner/releases"  # Modifica con il tuo URL di release
            print(f"Visita questa pagina per scaricare l'ultima versione: {download_url}")
            webbrowser.open(download_url)  # Apre il browser con l'URL di download
        else:
            print(f"Il programma è aggiornato alla versione {remote_version}.")
    else:
        print("Errore nel recuperare il file di configurazione da GitHub.")


if __name__ == "__main__":
    check_version()
