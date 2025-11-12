# ==========================================================
# llm_client.py
# ----------------------------------------------------------
# Questo file gestisce la comunicazione con Ollama.
# Permette di inviare un messaggio al modello Mistral locale
# e ricevere la risposta testuale.
# ==========================================================

import subprocess   # serve per eseguire comandi di sistema
import shlex        # serve per dividere stringhe in argomenti sicuri

class OllamaClient:
    """
    Classe che gestisce la connessione con Ollama.
    Puoi cambiare il modello (es. 'mistral', 'llama2', ecc.)
    passando il nome nel costruttore.
    """
    def __init__(self, model='mistral'):
        self.model = model  # Nome del modello caricato in Ollama

    def prompt(self, text):
        """
        Invia un testo (prompt) al modello e ritorna la risposta.
        """
        # Comando per eseguire ollama tramite terminale
        cmd = f'ollama run {self.model} "{text}"'
        args = shlex.split(cmd)

        # Eseguiamo il comando e catturiamo l'output
        res = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='ignore')


        # Se qualcosa va storto, stampiamo l'errore
        if res.returncode != 0:
            raise RuntimeError(f"Errore Ollama: {res.stderr}")

        # Ritorniamo la risposta generata dal modello
        return res.stdout.strip()


# ----------------------------------------------------------
# Test rapido (puoi lanciare questo file direttamente da VS Code)
# ----------------------------------------------------------
if __name__ == "__main__":
    client = OllamaClient(model="mistral")   # istanziamo la classe
    risposta = client.prompt("Ciao! Scrivi una frase breve di prova.")
    print("\nRisposta del modello:")
    print(risposta)
