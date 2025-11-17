"""
Reset completo della memoria JARVIS
====================================

Pulisce completamente il database ChromaDB quando è corrotto.
Usa questo script se vedi errori come:
- "Error creating hnsw segment reader"
- "Nothing found on disk"
- JARVIS risponde in modo errato con dati memorizzati

ATTENZIONE: Cancella TUTTA la memoria salvata!
"""

import shutil
import os
from pathlib import Path

def reset_jarvis_memory():
    """Elimina completamente il database ChromaDB"""

    memory_path = Path("./memory/chroma_db")

    print("=" * 60)
    print("🧠 RESET MEMORIA JARVIS")
    print("=" * 60)
    print()
    print("⚠️  ATTENZIONE: Questa operazione cancellerà:")
    print("   - Tutte le conversazioni salvate")
    print("   - Tutti i fatti utente (nome, età, preferenze)")
    print("   - Tutta la knowledge acquisita")
    print()

    # Controllo esistenza
    if not memory_path.exists():
        print(f"✅ Database non esiste: {memory_path}")
        print("   Nessuna azione necessaria - verrà creato al prossimo avvio")
        return

    # Conferma
    response = input("Vuoi procedere? (scrivi 'SI' per confermare): ")

    if response.strip().upper() != "SI":
        print("❌ Operazione annullata")
        return

    # Elimina directory
    try:
        print(f"\n🗑️  Eliminazione database: {memory_path}")
        shutil.rmtree(memory_path)
        print("✅ Database eliminato con successo!")
        print()
        print("📝 Prossimi passi:")
        print("   1. Riavvia il server WebSocket (python server/websocket_server.py)")
        print("   2. Il database verrà ricreato automaticamente")
        print("   3. Dovrai inserire nuovamente le informazioni (nome, età, ecc.)")
        print()

    except Exception as e:
        print(f"❌ Errore durante eliminazione: {e}")
        print("\nProva manualmente:")
        print(f"   1. Ferma il server JARVIS")
        print(f"   2. Elimina la cartella: {memory_path.absolute()}")
        print(f"   3. Riavvia il server")


if __name__ == "__main__":
    reset_jarvis_memory()
