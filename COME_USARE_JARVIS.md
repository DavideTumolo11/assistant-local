# 🚀 GUIDA COMPLETA - JARVIS AI ASSISTANT

## 📋 REQUISITI

Prima di avviare JARVIS, assicurati di avere installato:

### 1. **Python 3.8+**
- Scarica da: https://www.python.org/downloads/
- ⚠️ **IMPORTANTE**: Durante l'installazione, spunta "Add Python to PATH"!

### 2. **Node.js (con npm)**
- Scarica da: https://nodejs.org/
- Versione consigliata: LTS (Long Term Support)

---

## 🎯 METODI DI AVVIO

Hai **3 modi** per avviare JARVIS:

### **Metodo 1: Con finestra visibile (CONSIGLIATO PER DEBUG)** 🪟
Doppio click su: `start_jarvis.bat`

**Cosa fa:**
- Mostra finestre CMD dove vedi cosa succede
- Perfetto per vedere eventuali errori
- Utile quando sviluppi o testi

**Output che vedrai:**
```
========================================================
         JARVIS AI ASSISTANT - AVVIO SISTEMA
========================================================

[1/5] Verifica Python...
[OK] Python trovato

[2/5] Verifica ambiente virtuale...
[OK] Ambiente virtuale trovato

[3/5] Attivazione ambiente virtuale...
[OK] Ambiente virtuale attivo

[4/5] Verifica dipendenze Python...
[OK] Dipendenze base trovate

[5/5] Verifica Node.js...
[OK] Node.js trovato

========================================================
              AVVIO COMPONENTI JARVIS
========================================================

[BACKEND] Avvio server WebSocket Python (porta 8765)...
[FRONTEND] Avvio interfaccia Electron...
```

---

### **Metodo 2: Modalità STEALTH (invisibile)** 🥷
Doppio click su: `start_jarvis_stealth.vbs`

**Cosa fa:**
- Avvia JARVIS completamente in background
- Nessuna finestra CMD visibile
- Aspetto più professionale

**Come fermarlo:**
- Doppio click su `stop_jarvis.bat`
- OPPURE apri Task Manager (Ctrl+Shift+Esc) e chiudi `python.exe` ed `electron.exe`

---

### **Metodo 3: Manuale (per sviluppatori)** 👨‍💻

**Terminale 1 - Backend:**
```bash
cd assistant-local
python -m venv .venv
.venv\Scripts\activate
pip install websockets
python server\websocket_server.py
```

**Terminale 2 - Frontend:**
```bash
cd assistant-local
npm install
npm start
```

---

## ⚙️ PRIMA CONFIGURAZIONE

### **1. Installa dipendenze Python** (solo la prima volta)

Apri CMD nella cartella del progetto:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

⚠️ **Nota**: Alcune dipendenze sono pesanti (llama-index, chromadb, ecc.). Se vuoi solo testare JARVIS velocemente, installa solo:
```bash
pip install websockets
```

### **2. Installa dipendenze Node.js** (solo la prima volta)

```bash
npm install
```

---

## 🎮 COME USARE JARVIS

### **Interfaccia Principale**
Quando avvii JARVIS vedrai:
- 🎨 Anelli animati stile Iron Man
- 📊 Pannelli laterali con status sistema
- 💬 Pulsante CHAT in basso a destra

### **Chat Testuale**
1. Clicca sul pulsante **💬 CHAT**
2. Si apre il pannello chat
3. Scrivi il tuo messaggio
4. Premi **Invio** o clicca **➤**

**Esempi di comandi:**
- "Ciao JARVIS!"
- "Come stai?"
- "Che ore sono?"
- "Da quanto sei online?"
- "Chi sei?"

### **Riconoscimento Vocale** (in sviluppo)
- Clicca sul pulsante **🎙️ VOICE**
- Parla al microfono
- JARVIS risponderà con voce sintetizzata

---

## 🐛 RISOLUZIONE PROBLEMI

### ❌ **"Python non trovato"**
**Soluzione:**
1. Installa Python da https://www.python.org/downloads/
2. Durante installazione, spunta "Add Python to PATH"
3. Riavvia il computer
4. Riprova

### ❌ **"Node.js/npm non trovato"**
**Soluzione:**
1. Installa Node.js da https://nodejs.org/
2. Riavvia il computer
3. Riprova

### ❌ **"Impossibile creare ambiente virtuale"**
**Soluzione:**
```bash
python -m pip install --upgrade pip
python -m venv .venv --clear
```

### ❌ **"WebSocket disconnected"**
**Possibili cause:**
1. Server Python non avviato → Controlla finestra backend
2. Porta 8765 occupata → Chiudi altre app che usano quella porta
3. Firewall blocca connessione → Aggiungi eccezione per Python

### ❌ **File .bat non parte / "Accesso negato"**
**Soluzione:**
1. Click destro sul file → Proprietà
2. Tab "Generale" → Sblocca (se c'è)
3. Esegui come amministratore (se necessario)

### ❌ **Backend si chiude immediatamente**
**Soluzione:**
1. Apri CMD manualmente
2. Esegui:
   ```bash
   cd percorso\della\cartella\assistant-local
   python server\websocket_server.py
   ```
3. Leggi l'errore che compare
4. Probabilmente manca la libreria `websockets`:
   ```bash
   pip install websockets
   ```

---

## 📁 STRUTTURA FILE

```
assistant-local/
│
├── start_jarvis.bat          ← AVVIO NORMALE (con finestre)
├── start_jarvis_stealth.vbs  ← AVVIO INVISIBILE
├── stop_jarvis.bat            ← FERMA JARVIS
│
├── main.js                    ← Electron app principale
├── preload.js                 ← Preload script Electron
├── package.json               ← Dipendenze Node.js
├── requirements.txt           ← Dipendenze Python
│
├── ui/
│   ├── index.html             ← Interfaccia HTML
│   ├── css/
│   │   └── style.css          ← Stili interfaccia
│   └── js/
│       └── app.js             ← Logica frontend (WebSocket)
│
└── server/
    ├── websocket_server.py    ← ⭐ SERVER WEBSOCKET (NUOVO!)
    ├── api_server.py          ← Server REST (opzionale)
    ├── agent.py               ← Agente AI (in sviluppo)
    ├── llm_client.py          ← Client LLM
    └── memory_semantic.py     ← Memoria semantica
```

---

## 🔧 CONFIGURAZIONI AVANZATE

### **Cambiare porta WebSocket**

**File:** `server/websocket_server.py`
```python
# Cerca questa riga (circa riga 30):
def __init__(self, host='localhost', port=8765):

# Cambia 8765 con la porta desiderata
```

**File:** `ui/js/app.js`
```javascript
// Cerca questa riga (circa riga 18):
websocketUrl: 'ws://localhost:8765',

// Cambia 8765 con la stessa porta
```

### **Integrare un LLM vero (ChatGPT, Mistral, ecc.)**

Modifica `server/websocket_server.py`:
1. Aggiungi import per il tuo LLM
2. Nella funzione `generate_response_streaming`, sostituisci la logica con chiamate al LLM
3. Esempio con OpenAI:

```python
from openai import OpenAI

client = OpenAI(api_key="tua-api-key")

async def generate_response_streaming(self, websocket, user_input: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}],
        stream=True
    )

    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            await self.send_message(websocket, {
                'type': 'ai_response_chunk',
                'chunk': delta,
                ...
            })
```

---

## 📊 DIFFERENZA TRA I FILE

### **start_jarvis.bat vs start_jarvis_stealth.vbs**

| Caratteristica | .bat | .vbs |
|---|---|---|
| Finestre visibili | ✅ Sì | ❌ No (invisibile) |
| Debug facile | ✅ Sì | ❌ No |
| Aspetto professionale | ❌ No | ✅ Sì |
| Fermarlo facilmente | ✅ Chiudi finestra | ⚠️ Serve stop_jarvis.bat |
| **Quando usarlo** | **Sviluppo/Test** | **Uso quotidiano** |

---

## 🚀 PROSSIMI PASSI

1. ✅ Sistema funzionante con WebSocket
2. 🔄 **Da fare**: Integrare LLM vero (ChatGPT/Mistral/Llama)
3. 🔄 **Da fare**: Riconoscimento vocale funzionante
4. 🔄 **Da fare**: Text-to-Speech per risposte vocali
5. 🔄 **Da fare**: Memoria persistente migliorata

---

## 💡 SUGGERIMENTI

- **Prima volta**: Usa `start_jarvis.bat` per vedere se tutto funziona
- **Errori**: Controlla le finestre CMD per messaggi di errore
- **Sviluppo**: Tieni aperte le Console DevTools (F12 in Electron)
- **Produzione**: Usa `start_jarvis_stealth.vbs` per esperienza pulita

---

## 📞 SUPPORTO

Se hai problemi:
1. Controlla questa guida
2. Leggi gli errori nelle finestre CMD
3. Verifica che Python e Node.js siano installati correttamente
4. Controlla che le porte 8765 e 5000 siano libere

---

**Buon divertimento con JARVIS! 🎉**

*Creato da Davide Tumolo*
