import requests
import webbrowser
from config import versione  # Importa la versione attuale del programma

GITHUB_API_URL = "https://api.github.com/repos/tuo-username/my_project/releases/latest"
DOWNLOAD_URL = "https://github.com/tuo-username/my_project/releases"

def get_latest_version():
    """ Recupera l'ultima versione rilasciata su GitHub. """
    try:
        response = requests.get(GITHUB_API_URL, timeout=5)
        if response.status_code == 200:
            latest_release = response.json()
            return latest_release["tag_name"].lstrip("v")  # Rimuove il prefisso "v" se presente
    except requests.RequestException:
        print("Errore nel controllare la versione.")
    return None

def check_for_update():
    """ Controlla se è disponibile una nuova versione e, in caso, apre la pagina di download. """
    latest_version = get_latest_version()
    if latest_version and latest_version != versione:
        print(f"Nuova versione disponibile: {latest_version} (attuale: {versione})")
        print("Vai alla pagina di download per aggiornare.")
        webbrowser.open(DOWNLOAD_URL)
    else:
        print("Il programma è aggiornato.")

if __name__ == "__main__":
    check_for_update()
