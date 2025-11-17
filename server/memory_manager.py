"""
JARVIS Memory Manager - Sistema di Memoria Persistente con ChromaDB
===================================================================

Gestisce la memoria a lungo termine di JARVIS usando:
- ChromaDB per vector storage
- sentence-transformers per embeddings semantici
- Metadata per filtraggio e categorizzazione

JARVIS ricorda:
- Conversazioni passate
- Fatti sull'utente (nome, età, preferenze)
- Conoscenza acquisita
- Contesto storico
"""

import chromadb
from chromadb.config import Settings
from datetime import datetime
import os
import json
from typing import List, Dict, Optional


class MemoryManager:
    """Gestisce la memoria persistente di JARVIS"""

    def __init__(self, persist_directory: str = "./memory/chroma_db"):
        """
        Inizializza il sistema di memoria

        Args:
            persist_directory: Path dove salvare il database ChromaDB
        """
        self.persist_directory = persist_directory

        # Crea directory se non esiste
        os.makedirs(persist_directory, exist_ok=True)

        print(f"🧠 Inizializzazione memoria JARVIS...")
        print(f"📁 Database: {persist_directory}")

        # Setup ChromaDB con persistenza locale
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Collection per conversazioni
        self.conversations_collection = self.client.get_or_create_collection(
            name="conversations",
            metadata={"description": "Cronologia conversazioni con utente"}
        )

        # Collection per fatti sull'utente
        self.user_facts_collection = self.client.get_or_create_collection(
            name="user_facts",
            metadata={"description": "Informazioni permanenti sull'utente"}
        )

        # Collection per knowledge acquisita
        self.knowledge_collection = self.client.get_or_create_collection(
            name="knowledge",
            metadata={"description": "Conoscenza studiata da JARVIS"}
        )

        print(f"✅ Memoria JARVIS inizializzata")
        print(f"📊 Conversazioni salvate: {self.conversations_collection.count()}")
        print(f"👤 Fatti utente salvati: {self.user_facts_collection.count()}")
        print(f"📚 Knowledge salvata: {self.knowledge_collection.count()}")

    def save_conversation(
        self,
        user_message: str,
        jarvis_response: str,
        metadata: Optional[Dict] = None
    ):
        """
        Salva una conversazione nella memoria

        Args:
            user_message: Messaggio dell'utente
            jarvis_response: Risposta di JARVIS
            metadata: Metadata aggiuntivi (timestamp, ecc.)
        """
        timestamp = datetime.now().isoformat()
        conversation_id = f"conv_{timestamp}_{hash(user_message)}"

        # Prepara metadata
        conv_metadata = {
            "timestamp": timestamp,
            "type": "conversation",
            "user_message": user_message[:200],  # Troncato per metadata
            "response": jarvis_response[:200]
        }

        if metadata:
            conv_metadata.update(metadata)

        # Crea documento testuale per embedding
        document = f"User: {user_message}\nJARVIS: {jarvis_response}"

        # Salva in ChromaDB
        self.conversations_collection.add(
            documents=[document],
            metadatas=[conv_metadata],
            ids=[conversation_id]
        )

        print(f"💾 Conversazione salvata: ID={conversation_id}")

    def save_user_fact(
        self,
        fact_key: str,
        fact_value: str,
        category: str = "general"
    ):
        """
        Salva un fatto permanente sull'utente

        Args:
            fact_key: Chiave del fatto (es. "nome", "età", "hobby")
            fact_value: Valore del fatto
            category: Categoria (personal, preferences, etc.)
        """
        timestamp = datetime.now().isoformat()
        fact_id = f"fact_{fact_key}_{timestamp}"

        metadata = {
            "key": fact_key,
            "category": category,
            "timestamp": timestamp,
            "type": "user_fact"
        }

        # Documento per embedding semantico
        document = f"{fact_key}: {fact_value}"

        # Salva
        self.user_facts_collection.add(
            documents=[document],
            metadatas=[metadata],
            ids=[fact_id]
        )

        print(f"👤 Fatto utente salvato: {fact_key} = {fact_value}")

    def save_knowledge(
        self,
        topic: str,
        content: str,
        source: str = "conversation"
    ):
        """
        Salva conoscenza acquisita da JARVIS

        Args:
            topic: Argomento (es. "fisica quantistica")
            content: Contenuto della conoscenza
            source: Fonte (conversation, wikipedia, study, etc.)
        """
        timestamp = datetime.now().isoformat()
        knowledge_id = f"know_{topic}_{timestamp}"

        metadata = {
            "topic": topic,
            "source": source,
            "timestamp": timestamp,
            "type": "knowledge"
        }

        document = f"Topic: {topic}\n{content}"

        self.knowledge_collection.add(
            documents=[document],
            metadatas=[metadata],
            ids=[knowledge_id]
        )

        print(f"📚 Knowledge salvata: {topic} (source: {source})")

    def get_relevant_memories(
        self,
        query: str,
        n_results: int = 5,
        include_conversations: bool = True,
        include_user_facts: bool = True,
        include_knowledge: bool = True
    ) -> Dict[str, List[Dict]]:
        """
        Recupera memorie rilevanti per una query usando semantic search

        Args:
            query: Query dell'utente
            n_results: Numero massimo risultati per collection
            include_conversations: Include cronologia conversazioni
            include_user_facts: Include fatti utente
            include_knowledge: Include knowledge base

        Returns:
            Dict con memorie categorizzate: {conversations, user_facts, knowledge}
        """
        results = {
            "conversations": [],
            "user_facts": [],
            "knowledge": []
        }

        # Search conversazioni
        if include_conversations and self.conversations_collection.count() > 0:
            try:
                conv_results = self.conversations_collection.query(
                    query_texts=[query],
                    n_results=min(n_results, self.conversations_collection.count())
                )

                if conv_results['documents'] and conv_results['documents'][0]:
                    for i, doc in enumerate(conv_results['documents'][0]):
                        results["conversations"].append({
                            "document": doc,
                            "metadata": conv_results['metadatas'][0][i] if conv_results['metadatas'] else {},
                            "distance": conv_results['distances'][0][i] if 'distances' in conv_results else None
                        })
            except Exception as e:
                print(f"⚠️ Error searching conversations: {e}")

        # Search fatti utente
        if include_user_facts and self.user_facts_collection.count() > 0:
            try:
                facts_results = self.user_facts_collection.query(
                    query_texts=[query],
                    n_results=min(n_results, self.user_facts_collection.count())
                )

                if facts_results['documents'] and facts_results['documents'][0]:
                    for i, doc in enumerate(facts_results['documents'][0]):
                        results["user_facts"].append({
                            "document": doc,
                            "metadata": facts_results['metadatas'][0][i] if facts_results['metadatas'] else {},
                            "distance": facts_results['distances'][0][i] if 'distances' in facts_results else None
                        })
            except Exception as e:
                print(f"⚠️ Error searching user facts: {e}")

        # Search knowledge
        if include_knowledge and self.knowledge_collection.count() > 0:
            try:
                know_results = self.knowledge_collection.query(
                    query_texts=[query],
                    n_results=min(n_results, self.knowledge_collection.count())
                )

                if know_results['documents'] and know_results['documents'][0]:
                    for i, doc in enumerate(know_results['documents'][0]):
                        results["knowledge"].append({
                            "document": doc,
                            "metadata": know_results['metadatas'][0][i] if know_results['metadatas'] else {},
                            "distance": know_results['distances'][0][i] if 'distances' in know_results else None
                        })
            except Exception as e:
                print(f"⚠️ Error searching knowledge: {e}")

        return results

    def get_user_fact(self, fact_key: str) -> Optional[str]:
        """
        Recupera un fatto specifico sull'utente

        Args:
            fact_key: Chiave del fatto (es. "nome", "età")

        Returns:
            Valore del fatto o None se non trovato
        """
        try:
            results = self.user_facts_collection.query(
                query_texts=[fact_key],
                n_results=1,
                where={"key": fact_key}
            )

            if results['documents'] and results['documents'][0]:
                # Estrai valore dal documento "key: value"
                doc = results['documents'][0][0]
                if ':' in doc:
                    return doc.split(':', 1)[1].strip()

            return None
        except Exception as e:
            print(f"⚠️ Error getting user fact: {e}")
            return None

    def format_memories_for_prompt(self, memories: Dict[str, List[Dict]]) -> str:
        """
        Formatta le memorie recuperate in testo per il system prompt

        Args:
            memories: Dict da get_relevant_memories()

        Returns:
            Testo formattato per il prompt
        """
        prompt_parts = []

        # Fatti utente (priorità massima)
        if memories["user_facts"]:
            facts_text = "\n".join([
                f"- {mem['document']}"
                for mem in memories["user_facts"][:3]  # Top 3
            ])
            prompt_parts.append(f"INFORMAZIONI UTENTE:\n{facts_text}")

        # Conversazioni rilevanti
        if memories["conversations"]:
            conv_text = "\n".join([
                f"- {mem['document'][:200]}..."
                for mem in memories["conversations"][:2]  # Top 2
            ])
            prompt_parts.append(f"CONVERSAZIONI RILEVANTI:\n{conv_text}")

        # Knowledge
        if memories["knowledge"]:
            know_text = "\n".join([
                f"- {mem['document'][:200]}..."
                for mem in memories["knowledge"][:2]  # Top 2
            ])
            prompt_parts.append(f"KNOWLEDGE BASE:\n{know_text}")

        return "\n\n".join(prompt_parts) if prompt_parts else ""

    def get_stats(self) -> Dict:
        """Ritorna statistiche sulla memoria"""
        return {
            "conversations": self.conversations_collection.count(),
            "user_facts": self.user_facts_collection.count(),
            "knowledge": self.knowledge_collection.count(),
            "total_memories": (
                self.conversations_collection.count() +
                self.user_facts_collection.count() +
                self.knowledge_collection.count()
            )
        }

    def reset_memory(self):
        """ATTENZIONE: Cancella tutta la memoria (solo per debug)"""
        print("⚠️ RESET MEMORIA IN CORSO...")
        self.client.reset()
        print("✅ Memoria resettata completamente")


# Test rapido
if __name__ == "__main__":
    print("🧪 Test MemoryManager...")

    # Init
    mm = MemoryManager()

    # Test salvataggio conversazione
    mm.save_conversation(
        user_message="Ciao, mi chiamo Davide",
        jarvis_response="Piacere di conoscerti, Davide. Tutti i sistemi operativi."
    )

    # Test salvataggio fatto
    mm.save_user_fact("nome", "Davide", "personal")
    mm.save_user_fact("età", "39 anni", "personal")

    # Test retrieval
    memories = mm.get_relevant_memories("come mi chiamo?")
    print("\n🔍 Memorie recuperate:")
    print(json.dumps(memories, indent=2, ensure_ascii=False))

    # Test format
    formatted = mm.format_memories_for_prompt(memories)
    print("\n📝 Formato per prompt:")
    print(formatted)

    # Stats
    print("\n📊 Statistiche:")
    print(mm.get_stats())
