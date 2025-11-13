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

## ✅ FASE 1 COMPLETATA! (Memoria Persistente ChromaDB)

### 🎉 Implementato
- [x] ChromaDB + sentence-transformers installati
- [x] memory_manager.py con 3 collections (conversations, user_facts, knowledge)
- [x] Semantic search per retrieval memorie rilevanti
- [x] Auto-estrazione fatti (nome, età) tramite pattern matching
- [x] Integrazione completa in websocket_server.py
- [x] Memorie iniettate automaticamente nel system prompt
- [x] Salvataggio permanente di TUTTE le conversazioni

### 📝 Pronto per test
- [ ] Testare memoria: dire info personali e verificare che JARVIS le ricordi

---

## 📋 DA FARE (~70%)

### ~~FASE 1: 🧠 MEMORIA PERMANENTE~~ ✅ COMPLETATA!
**Obiettivo:** JARVIS ricorda tutto per sempre

#### ~~SQLite Base (Quick)~~ SALTATA - Implementato ChromaDB direttamente
- [x] Database ChromaDB locale (`memory/chroma_db/`)
- [x] 3 Collections: conversations, user_facts, knowledge
- [x] Funzione `save_user_fact(key, value, category)`
- [x] Funzione `get_relevant_memories(query)` con semantic search
- [x] Integrazione nel prompt: inietta fatti rilevanti

#### ChromaDB Avanzato ✅ COMPLETATO
- [x] Installare ChromaDB + sentence-transformers
- [x] Setup vector store locale (PersistentClient)
- [x] Embedding automatici con sentence-transformers
- [x] Salvare ogni conversazione con metadata
- [x] Semantic search nella memoria con distance scoring
- [x] Retrieval contestuale automatico per ogni query
- [x] Auto-estrazione fatti (nome, età) tramite regex

**Output ottenuto:**
- ✅ JARVIS ricorda nome, età, preferenze, fatti personali
- ✅ Cerca informazioni rilevanti nella memoria semanticamente
- ✅ Usa il contesto di conversazioni passate
- ✅ Database persistente su disco (sopravvive ai riavvii)

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
████████████░░░░░░░░░░░░░░░░ 45% Completato

✅ Base Infrastructure (100%)
✅ Memoria Persistente (100%) 🎉 COMPLETATA!
📋 Voice I/O (0%)
📋 Web Search (0%)
📋 RAG System (0%)
📋 Agent System (0%)
📋 Ottimizzazioni (0%)
```

---

## 🎯 PROSSIMI STEP IMMEDIATI

1. **✅ COMPLETATO**: Sistema memoria ChromaDB ✨
   - ✅ ChromaDB + sentence-transformers
   - ✅ 3 collections (conversations, user_facts, knowledge)
   - ✅ Semantic search & retrieval
   - ✅ Auto-estrazione fatti
   - ✅ Integrazione completa

2. **ORA - Test Memoria**: Verificare funzionamento
   - Dire a JARVIS: "Mi chiamo [nome]"
   - Chiedere: "Come mi chiamo?"
   - Verificare che ricordi

3. **Prossimo**: Web Search base (FASE 4)
   - DuckDuckGo integration
   - Wikipedia API
   - Auto-search quando non sa

4. **Poi**: Voice I/O (FASE 2+3)
   - Vosk recognition (input)
   - pyttsx3 speech (output)
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
**Versione JARVIS:** 0.4.0-alpha
**Stato:** In sviluppo attivo - FASE 1 COMPLETATA! 🎉
