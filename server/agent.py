# server/agent.py
import os
import asyncio
from langchain.chat_models import ChatOpenAI
from memory_semantic import SemanticMemory  # la tua classe di memoria personalizzata

# Imposta la tua chiave API di OpenAI come variabile d'ambiente
os.environ["OPENAI_API_KEY"] = "INSERISCI_LA_TUA_API_KEY"

# Funzione principale asincrona per far partire l'agente
async def main():
    # Inizializza il modello ChatGPT
    llm = ChatOpenAI(
        model_name="gpt-4",  # puoi cambiare in gpt-3.5-turbo se vuoi
        temperature=0.7
    )

    # Inizializza la memoria semantica
    memory = SemanticMemory()

    print("Agente avviato! Scrivi 'exit' per uscire.")
    while True:
        # Input dell'utente
        user_input = input("Tu: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Recupera il contesto dalla memoria
        context = memory.get_context()

        # Prepara il messaggio da inviare al modello
        prompt = f"{context}\nUtente: {user_input}\nAgente:"
        response = await llm.apredict(input=prompt)

        # Mostra la risposta
        print(f"Agente: {response}")

        # Aggiorna la memoria con l'interazione recente
        memory.add_to_memory(user_input, response)

# Avvio dell'agente
if __name__ == "__main__":
    asyncio.run(main())
