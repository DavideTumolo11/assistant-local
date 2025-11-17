# 🚀 COME AVVIARE JARVIS

## ⚡ METODO CONSIGLIATO (npm scripts)

### 1️⃣ Setup Iniziale (solo prima volta)
```bash
npm install
npm run setup
```

### 2️⃣ Avvia JARVIS
```bash
npm run dev
```

Questo comando:
- ✅ Avvia il backend Python (WebSocket server)
- ✅ Avvia il frontend Electron
- ✅ Tutto in una finestra
- ✅ Ctrl+C per fermare tutto

---

## 🔧 COMANDI DISPONIBILI

### `npm run dev`
Avvia backend + frontend insieme (CONSIGLIATO)

### `npm run backend`
Avvia solo il server Python WebSocket

### `npm start`
Avvia solo l'interfaccia Electron

### `npm run setup`
Installa dipendenze Python

---

## 📝 REQUISITI

- **Python 3.10+** (installato e nel PATH)
- **Node.js 18+** (installato e nel PATH)
- **Ollama** (installato e in esecuzione in background)
  ```bash
  ollama pull mistral
  ollama serve
  ```

---

## ⚠️ PROBLEMI COMUNI

### "python non trovato"
Aggiungi Python al PATH di Windows:
1. Cerca "Variabili d'ambiente" in Windows
2. Aggiungi il percorso di Python a PATH

### "Backend non si connette"
1. Verifica che Ollama sia in esecuzione: `ollama list`
2. Controlla che la porta 8765 sia libera

### "Electron non si apre"
```bash
npm install
npm start
```

---

## 🗑️ FILE .BAT DEPRECATI

I file .bat sono obsoleti e non funzionano bene. Usa gli npm scripts sopra.

File rimossi:
- ~~start_jarvis.bat~~ → usa `npm run dev`
- ~~start_jarvis_silent.bat~~ → usa `npm run dev`
- ~~stop_jarvis.bat~~ → usa `Ctrl+C`
- ~~SETUP_WINDOWS.bat~~ → usa `npm run setup`

---

## 📊 VERIFICA INSTALLAZIONE

1. Verifica Python:
   ```bash
   python --version
   ```
   Dovrebbe mostrare: Python 3.10+

2. Verifica Node:
   ```bash
   node --version
   ```
   Dovrebbe mostrare: v18+

3. Verifica Ollama:
   ```bash
   ollama list
   ```
   Dovrebbe mostrare: mistral

---

**Tutto pronto? Avvia JARVIS con `npm run dev`!** 🤖
