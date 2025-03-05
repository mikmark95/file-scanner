
# File Scanner & Copier

#### Software che serve a ricercare ricorsivamente files tramite una chiave di ricerca e li copia in una cartella di destinazione, rinominandoli in base alla scelta di uno specifico pattern. 
#### Il risultato sarà un insieme di file rinominato come segue: *Prefisso_Pattern_File*

Richiede l'inserimento di alcuni dati:


- **Percorso di input** → Indicazione della cartella da dove iniziare a cercare ricorsivamente, cioè a partire dal livello attuale, scedendo e controllando in tutte le sotto-cartelle.
- **Prefisso** → Prefisso che dovrà essere presente sul nome dei files che verrano copiati.
- **Chiave di ricerca** → Chiave che deve essere presente sul nome dei files che stiamo cercando, può essere un estensione o una sotto-stringa.
- **Seleziona Pattern** → Modello che deve essere ricercato all'interno dei percorsi dei files, che sono stati selezionati mediante la chiave di ricerca, ed inserito nel nome del file copiato.
- **Percorso di output** → La cartella di destinazione, dove andranno inseriti i files copiati e rinominati.


Spiegazione pulsanti interfaccia:
 - ***Avvia***: Questo bottone avvia tutto il processo.
 - ***Salva log***: Questo bottone fa in modo di salvare tutti i messaggi del log in un file .txt, salvato nella posizione decisa dall utente.
 - ***Pulisci*** → Questo bottone pulisce tutti i campi del interfaccia, compreso la zona del log.
## Usage/Examples

La cosa principale da fare in modo preventivo è analizzare il *PATH ASSOLUTO* di uno dei files che vogliamo copiare, ed successivamente andiamo a selezionare il *PATTERN* idoneo.

In base al pattern selezionato si effettua una ricerca nel path del file, letto come stringa, per estrapolare una sottostringa che individua univocamente il il file.

Di seguito la spiegazione dettagliata dei pattern:

 

- #### ANNO-MESE-GIORNO-ORARIO

    Es.→ \\60_output3D\grecia\Mykonos integrazione Backpack\11-01-2025\output data\ResultData**2025-01-11-170051**_0\ 2025-01-11-170051\img_traj.csv

    *Seleziona il la prima occorrenza presente nel percorso che ha il questo formato*
    

- #### ANNO-MESE-GIORNO

    Es.→20_SVILUPPO\60_output3D\grecia\Rethimno Backpack\ __13-12-2024__\R1\R01-2020-12-26_01-19-51.las

    *Seleziona il la prima occorrenza presente nel percorso che ha il questo formato*


- #### NUMERICO

    Es. → \\192.168.199.10\Deposito3\20_SVILUPPO\60_output3D\grecia\Karditsa Z1\Panoramics\1\ __11__\Record001\Record001, Record001, LB6, Ladybug.csv

    *Seleziona il gradino più profondo della directory che è formato solo da cifre*

- #### INDICE PROGRESSIVO
    Rinomina i file in {PREFISSO}_____{PROGRESSIVO}____{NOME FILE}
    
    *Dove prograssivo è un numero che parte da 1 e viene incrementato per ogni file*

- #### INDICE RANDOM
    Rinomina i file in {PREFISSO}_____{RANDOM}____{NOME FILE}
    
    *Dove Random è un numero di 4 cifre generato in modo casuale*
- #### NESSUNO
    Non utilizza pattern particolari, semplicemente copia tutti i file che trova nel percorso di input che rispettano il criterio di ricerca e li copia nella cartella di destinazione




## Authors

- [@mikmark95](https://github.com/mikmark95)


## License

[Personal](https://raw.githubusercontent.com/mikmark95/file-scanner/refs/heads/main/LICENSE)

