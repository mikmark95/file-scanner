# Funzioni per la scansione e la copia dei file

# file_utils.py
import os
import shutil
from patterns import azione

def scan_dir(path_input, comune, key, diz_out, pattern, checkbox, log_callback):
    for entry in os.scandir(path_input):
        if entry.is_dir(follow_symlinks=False):
            scan_dir(entry.path, comune, key, diz_out, pattern, checkbox, log_callback)
        elif entry.is_file(follow_symlinks=False):
            if key in entry.name:
                data = azione(pattern, entry.path)
                chiave = f"{comune}_{data}_{entry.name}" if checkbox else f"{data}_{entry.name}"
                diz_out[chiave] = entry.path
                log_callback(f"Elemento aggiunto al dizionario --> {chiave}")

def copy_files(diz_out, output_path, log_callback):
    for chiave, elem in diz_out.items():
        dest = os.path.join(output_path, chiave)
        shutil.copy2(elem, dest)
        log_callback(f"Copia in corso: {elem} --> {dest}")

def center_widget(app, widget):
    screen = app.primaryScreen()
    screen_geometry = screen.availableGeometry()
    widget_geometry = widget.frameGeometry()
    widget_geometry.moveCenter(screen_geometry.center())
    widget.move(widget_geometry.topLeft())