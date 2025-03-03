# Funzioni per la gestione dei pattern regex

# patterns.py
import re
import random

contatore = 0


def azione(pattern, entry_path):
    global contatore
    match pattern:
        case "Anno-Mese-Giorno-Orario":
            regex = r"\d*-\d*-\d*-\d*"
        case "Anno-Mese-Giorno":
            regex = r"\d*-\d*-\d*"
        case "Numerico":
            regex = r"\\(\d{1,2}?)\\"
        case "Indice progressivo":
            contatore += 1
            return str(contatore)
        case "Indice random":
            return str(random.randint(1, 1000)).zfill(4)
        case "Nessuno":
            return 'vuoto'
        case _:
            return ''

    return re.findall(regex, entry_path)[0] if re.findall(regex, entry_path) else ''
