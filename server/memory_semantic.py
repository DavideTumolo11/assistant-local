# ==========================================================
# memory_semantic.py
# ----------------------------------------------------------
# Gestione della memoria semantica (concetti chiave)
# Utilizza Chroma (nuova API) per creare un vector store locale
# ==========================================================

import os
import uuid
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings  # nuova importazione aggiornata


class SemanticMemory:
    """
    Classe per salvare e recuperare concetti chiave dalla memoria semantica
    """

    def __init__(self, persist_directory="semantic_db"):
        # Percorso locale dove verranno salvati i dati della memoria
        self.persist_directory = persist_directory

        # Crea la cartella se non esiste
        os.makedirs(self.persist_directory, exist_ok=True)

        # Modello di embeddings locale (trasforma testo in vettori numerici)
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # ✅ Nuovo metodo compatibile con le versioni moderne di Chroma
        self.client = chromadb.PersistentClient(path=self.persist_directory)

        # Crea o recupera la collezione principale
        self.collection = self.client.get_or_create_collection(
            name="semantic_memory"
        )

    def add(self, text, metadata=None):
        """
        Aggiunge un concetto alla memoria semantica
        """
        metadata = metadata or {"source": "manual"}  # Metadati minimi richiesti da Chroma
        doc_id = str(uuid.uuid4())  # ID unico per ogni elemento

        # Calcoliamo l’embedding del testo
        embedding = self.embeddings.embed_query(text)

        # Aggiungiamo il concetto alla collezione
        self.collection.add(
            ids=[doc_id],
            documents=[text],
            metadatas=[metadata],
            embeddings=[embedding]
        )

        print(f"✅ Concetto aggiunto alla memoria: {text}")

    def query(self, text, k=3):
        """
        Recupera i concetti più rilevanti rispetto al testo di query
        """
        results = self.collection.query(
            query_embeddings=[self.embeddings.embed_query(text)],
            n_results=k
        )

        docs = results["documents"][0]
        print("\n🔍 Risultato della query:")
        print(docs)
        return docs

    def list_all(self):
        """
        Mostra tutti i concetti salvati nella memoria
        """
        results = self.collection.get()
        all_docs = results["documents"]

        print("\n🧠 Contenuti salvati nella memoria semantica:")
        for i, doc in enumerate(all_docs, 1):
            print(f"{i}. {doc}")
        return all_docs


# ==========================
# Esempio di test locale
# ==========================
if __name__ == "__main__":
    memory = SemanticMemory()
    memory.add("Il sole è una stella")
    memory.add("La luna orbita attorno alla Terra")
    memory.query("Che cosa illumina il giorno?")
    memory.list_all()
