# 🤖 JARVIS - TODO LIST

Assistente AI personale locale ispirato a Iron Man

---

## ✅ COMPLETATO (~30%)

### 🎨 Interfaccia Utente
- [x] Setup Electron con finestra principale
- [x] Interfaccia stile Iron Man con anelli animati
- [x] Particelle animate in background
- [x] Nome J.A.R.V.I.S centrato con effetti glow
- [x] Voice activity indicator con onde animate (posizionato sotto JARVIS)
- [x] Pannello SYSTEM STATUS (sinistra) con CPU, Memory, Voice, AI Model
- [x] Indicatore connessione WebSocket (pallino verde/rosso)
- [x] Modal QUICK CONTROLS con icona settings
- [x] Chat panel laterale con apertura/chiusura smooth
- [x] Sistema notifiche toast
- [x] Loading overlay con progress bar animata
- [x] Pulizia interfaccia (rimossi progress-squares non funzionanti)

### 🔧 Funzionalità Base
- [x] WebSocket server Python funzionante
- [x] Connessione client-server stabile con auto-reconnect
- [x] Chat testuale bidirezionale
- [x] Integrazione Ollama con Mistral-7B
- [x] Streaming risposte in tempo reale (word-by-word)
- [x] Cronologia conversazioni (ultimi 10 messaggi)
- [x] Metriche sistema reali (CPU, RAM con psutil)
- [x] Controlli finestra (minimize/fullscreen) con IPC sicuro
- [x] Batch scripts per avvio/stop JARVIS

### 🧠 Intelligenza AI
- [x] System prompt JARVIS personalizzato
- [x] Supporto data/ora nel contesto
- [x] Parametri Mistral ottimizzati (usa default)
- [x] Prompt per apprendimento dinamico (no info hard-coded)
- [x] Gestione errori e fallback

### 🔒 Sicurezza
- [x] Context isolation Electron abilitato
- [x] Node integration disabilitato
- [x] IPC sicuro tramite contextBridge
- [x] Preload script con esposizione minima API

---

## 🚧 IN CORSO (Memoria Persistente)

### 📝 Task Attuali
- [ ] Creare database SQLite per memoria persistente (tabella: user_facts)
- [ ] Implementare estrazione automatica fatti dalle conversazioni
- [ ] Creare funzioni save_fact() e get_relevant_facts() nel server
- [ ] Iniettare fatti rilevanti nel system prompt prima di ogni risposta
- [ ] Testare memoria: dire a JARVIS info personali e verificare che le ricordi

---

## 📋 DA FARE (~70%)

### FASE 1: 🧠 MEMORIA PERMANENTE (PRIORITÀ MASSIMA)
**Obiettivo:** JARVIS ricorda tutto per sempre

#### SQLite Base (Quick)
- [ ] Database SQLite locale (`memory/jarvis_memory.db`)
- [ ] Tabella `user_facts` (key, value, timestamp, category)
- [ ] Funzione `save_fact(key, value, category)`
- [ ] Funzione `get_facts_by_category(category)`
- [ ] Integrazione nel prompt: inietta fatti rilevanti

#### ChromaDB Avanzato (Long-term)
- [ ] Installare ChromaDB (`pip install chromadb`)
- [ ] Setup vector store locale
- [ ] Embedding model locale (sentence-transformers)
- [ ] Salvare ogni conversazione con metadata
- [ ] Semantic search nella memoria
- [ ] Retrieval contestuale automatico

**Output atteso:**
- JARVIS ricorda nome, età, preferenze, fatti personali
- Cerca informazioni rilevanti nella memoria
- Usa il contesto di conversazioni passate

---

### FASE 2: 🎙️ RICONOSCIMENTO VOCALE (PRIORITÀ MEDIA)
**Obiettivo:** Parlare a JARVIS invece di scrivere

#### Input Vocale
- [ ] Installare Vosk (`pip install vosk`)
- [ ] Scaricare modello italiano Vosk
- [ ] Creare `voice_recognition.py`
- [ ] Catturare audio da microfono (pyaudio)
- [ ] Transcription in tempo reale
- [ ] Invio testo al WebSocket
- [ ] Bottone "Push to Talk" nel frontend
- [ ] Indicatore "Listening..." attivo durante registrazione

**Output atteso:**
- Premere bottone → parlare → JARVIS trascrive e risponde

---

### FASE 3: 🔊 TEXT-TO-SPEECH (PRIORITÀ MEDIA)
**Obiettivo:** JARVIS risponde con voce

#### Output Vocale
- [ ] Installare pyttsx3 (`pip install pyttsx3`)
- [ ] Creare `text_to_speech.py`
- [ ] Setup voce italiana
- [ ] Regolazione velocità/tono
- [ ] Toggle voice output on/off
- [ ] Sincronizzazione con animazione voice-activity
- [ ] Opzione: Coqui TTS per voce più naturale

**Output atteso:**
- JARVIS risponde sia con testo che con voce
- Voice activity indicator si anima durante parlato

---

### FASE 4: 🌐 WEB SEARCH (PRIORITÀ ALTA)
**Obiettivo:** "JARVIS, cerca su internet..."

#### Ricerca Web
- [ ] Installare duckduckgo_search (`pip install duckduckgo-search`)
- [ ] Creare `web_search.py` con tool search
- [ ] Integrazione Wikipedia API
- [ ] Parser risultati search
- [ ] Limit risultati (top 3-5)
- [ ] Cache risultati per evitare spam
- [ ] JARVIS riconosce quando deve cercare

#### Esempio conversazione:
```
User: Chi è stato Nikola Tesla?
JARVIS: Cerco su Wikipedia... [fetch e risposta]
```

**Output atteso:**
- JARVIS cerca automaticamente quando non conosce qualcosa
- Usa Wikipedia per info enciclopediche
- DuckDuckGo per ricerche generali

---

### FASE 5: 📚 RAG - "STUDIARE" ARGOMENTI (PRIORITÀ MASSIMA)
**Obiettivo:** "JARVIS, vai su Wikipedia e studia la fisica quantistica"

#### Retrieval Augmented Generation
- [ ] Installare LangChain (`pip install langchain`)
- [ ] Document loaders (Wikipedia, PDF, web)
- [ ] Text splitter per chunking
- [ ] Embedding locale con sentence-transformers
- [ ] Vector store (ChromaDB)
- [ ] Retrieval chain
- [ ] JARVIS "studia" e salva knowledge base

#### Workflow:
1. User: "Studia la fisica quantistica"
2. JARVIS: "Accesso a Wikipedia, elaborazione in corso..."
3. Scarica articolo → chunk → embed → salva in ChromaDB
4. JARVIS: "Ho studiato la fisica quantistica. Posso rispondere a domande."
5. User: "Cos'è l'entanglement quantistico?"
6. JARVIS: [cerca in knowledge base] → risponde

**Output atteso:**
- JARVIS accumula conoscenza permanente
- Risponde su argomenti che ha "studiato"
- Knowledge base persistente su disco

---

### FASE 6: 🤖 AGENT CON TOOL CALLING (PRIORITÀ FINALE)
**Obiettivo:** JARVIS decide da solo quali strumenti usare

#### LangChain Agent
- [ ] Setup ReAct Agent
- [ ] Tool: search_web
- [ ] Tool: search_memory
- [ ] Tool: calculator
- [ ] Tool: study_topic
- [ ] Tool: set_reminder (opzionale)
- [ ] Tool: file_operations (opzionale)
- [ ] Agent reasoning loop
- [ ] JARVIS spiega cosa sta facendo

#### Esempio conversazione:
```
User: Ho un incontro tra 2 ore, ricordamelo e cerca informazioni su GPT-4
JARVIS: [Usa tool: set_reminder] Promemoria impostato.
        [Usa tool: search_web] Cerco informazioni su GPT-4...
        [Risponde con riassunto]
```

**Output atteso:**
- JARVIS agisce autonomamente
- Usa tool multipli per task complessi
- Spiega i suoi processi di ragionamento

---

### FASE 7: 🎯 OTTIMIZZAZIONI FINALI
**Obiettivo:** Performance, UX, Stabilità

#### Performance
- [ ] Caching risposte frequenti
- [ ] Lazy loading per knowledge base
- [ ] Background tasks per operazioni lunghe
- [ ] Ottimizzazione query ChromaDB

#### User Experience
- [ ] Hotkeys globali (es. Ctrl+Alt+J per attivare)
- [ ] System tray icon con menu
- [ ] Modalità "always on top"
- [ ] Dark/Light theme
- [ ] Personalizzazione voce
- [ ] Export/Import conversazioni

#### Stabilità
- [ ] Error recovery robusto
- [ ] Logging completo
- [ ] Health checks automatici
- [ ] Auto-restart su crash
- [ ] Backup automatico database

---

## 📊 PROGRESSO COMPLESSIVO

```
████████░░░░░░░░░░░░░░░░░░░░ 30% Completato

✅ Base Infrastructure (30%)
🚧 Memoria Persistente (0%)
📋 Voice I/O (0%)
📋 Web Search (0%)
📋 RAG System (0%)
📋 Agent System (0%)
📋 Ottimizzazioni (0%)
```

---

## 🎯 PROSSIMI STEP IMMEDIATI

1. **✅ OGGI**: Sistema memoria SQLite base
   - Database creazione
   - Save/get facts
   - Integrazione prompt

2. **Domani**: Test memoria + Web Search base
   - Testare memoria con info personali
   - DuckDuckGo integration

3. **Questa settimana**: RAG System
   - LangChain setup
   - ChromaDB integration
   - Wikipedia study capability

4. **Prossima settimana**: Voice I/O
   - Vosk recognition
   - pyttsx3 speech
   - Full voice interaction

---

## 📝 NOTE TECNICHE

### Stack Corrente
- **Frontend**: Electron + HTML/CSS/JS vanilla
- **Backend**: Python 3.12 + WebSocket (websockets)
- **AI**: Ollama + Mistral-7B
- **Metriche**: psutil
- **Database**: (Da implementare) SQLite → ChromaDB

### Dipendenze Future
```bash
pip install chromadb sentence-transformers
pip install langchain langchain-community
pip install duckduckgo-search wikipedia-api
pip install vosk pyaudio
pip install pyttsx3
```

### Performance Target
- Response time: < 2s (con streaming inizia subito)
- Memory footprint: < 1GB RAM
- Startup time: < 5s
- Voice latency: < 500ms

---

**Ultimo aggiornamento:** 13/11/2025
**Versione JARVIS:** 0.3.0-alpha
**Stato:** In sviluppo attivo
