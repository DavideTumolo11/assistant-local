// renderer.js
// Gestisce UI, voice recognition e TTS, comunicazione con Flask
// COMMENTI: spiegazioni in italiano riga per riga quando utile

// === CONFIG ===
const API_URL = "http://127.0.0.1:5000/chat"; // Cambia se il tuo endpoint è diverso

// === ELEMENTI DOM ===
const backendStatus = document.getElementById('backend-status');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const chatSendBtn = document.getElementById('chat-send');
const toggleChatBtn = document.getElementById('toggle-chat');
const chatPanel = document.getElementById('chat-panel');
const jarvisCenter = document.getElementById('jarvis-center');
const jarvisSpeechText = document.getElementById('jarvis-speech-text');

const voiceToggle = document.getElementById('voice-toggle');
const voiceStop = document.getElementById('voice-stop');

let isChatVisible = true;
let recognition = null;
let recognizing = false;

// Controllo backend - semplice ping per cambiare stato (non invasivo)
async function checkBackend() {
    try {
        const res = await fetch(API_URL, { method: 'OPTIONS' });
        backendStatus.textContent = 'online';
    } catch (e) {
        backendStatus.textContent = 'offline';
    }
}
setInterval(checkBackend, 4000);
checkBackend();

// --- Helper per aggiungere messaggi nella chat ---
function addMessage(text, from = 'bot') {
    const div = document.createElement('div');
    div.classList.add('msg', from === 'user' ? 'user' : 'bot');
    div.textContent = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// --- Invio messaggio testuale al server ---
async function sendTextMessage(text, options = { voice: false }) {
    if (!text) return;
    addMessage(text, 'user');
    // Mostriamo subito che stiamo aspettando
    addMessage('⏳ elaborazione...', 'bot');

    try {
        const resp = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await resp.json();
        const reply = data.reply || data.message || "Nessuna risposta";

        // Rimuovo messaggio 'elaborazione...' e aggiungo la risposta reale
        const last = chatMessages.querySelectorAll('.msg.bot');
        if (last.length) last[last.length - 1].remove();

        addMessage(reply, 'bot');

        // Se l'opzione voice è true riproduci con TTS e mostra in modalità invisibile
        if (options.voice) {
            speakAndDisplay(reply);
        }
    } catch (err) {
        // errore di rete / backend
        const last = chatMessages.querySelectorAll('.msg.bot');
        if (last.length) last[last.length - 1].remove();
        addMessage("Errore: impossibile contattare il server.", 'bot');
        console.error(err);
    }
}

// --- TTS e visualizzazione "invisibile" ---
function speakAndDisplay(text) {
    // Metti il testo al centro (modalità invisibile)
    jarvisSpeechText.textContent = text;
    jarvisCenter.classList.add('speaking'); // puoi usare questa classe per animazioni

    // Usa SpeechSynthesis del browser per parlare
    const utter = new SpeechSynthesisUtterance(text);
    utter.rate = 1.0;
    utter.pitch = 1.0;
    utter.onend = () => {
        // pulisco dopo la fine o lascio il testo? qui lo lascio ma puoi cancellare dopo N secondi
        setTimeout(() => jarvisCenter.classList.remove('speaking'), 700);
    };
    speechSynthesis.cancel(); // cancella eventuali utter in corso
    speechSynthesis.speak(utter);
}

// --- RICONOSCIMENTO VOCALE (browser) ---
function initSpeechRecognition() {
    // WebKitSpeechRecognition for Chrome/Electron
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return null;

    const r = new SpeechRecognition();
    r.lang = 'it-IT';
    r.interimResults = false;
    r.maxAlternatives = 1;
    r.continuous = false;

    r.onstart = () => {
        recognizing = true;
        voiceToggle.classList.add('hidden');
        voiceStop.classList.remove('hidden');
        jarvisSpeechText.textContent = "🎤 Sto ascoltando...";
        jarvisCenter.classList.add('speaking');
    };

    r.onresult = (ev) => {
        const transcript = ev.results[0][0].transcript;
        jarvisCenter.classList.remove('speaking');
        jarvisSpeechText.textContent = ""; // svuoto il centro perché useremo la chat per il testo dell'utente
        // invio il testo come messaggio ma facendo sapere che è stato da voce
        sendTextMessage(transcript, { voice: true });
    };

    r.onerror = (ev) => {
        console.warn('Speech error', ev);
        jarvisCenter.classList.remove('speaking');
        jarvisSpeechText.textContent = "Errore riconoscimento vocale";
        voiceToggle.classList.remove('hidden');
        voiceStop.classList.add('hidden');
        recognizing = false;
    };

    r.onend = () => {
        // fine dell'ascolto
        recognizing = false;
        voiceToggle.classList.remove('hidden');
        voiceStop.classList.add('hidden');
        jarvisCenter.classList.remove('speaking');
    };

    return r;
}

// Inizializza recognition se disponibile
recognition = initSpeechRecognition();

// --- Event listeners UI ---
chatSendBtn.addEventListener('click', () => {
    const text = chatInput.value.trim();
    if (!text) return;
    chatInput.value = '';
    sendTextMessage(text, { voice: false });
});
chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') chatSendBtn.click();
});

toggleChatBtn.addEventListener('click', () => {
    isChatVisible = !isChatVisible;
    chatPanel.style.display = isChatVisible ? 'flex' : 'none';
});

// Voice start/stop
voiceToggle.addEventListener('click', () => {
    // Se recognition è disponibile, usalo
    if (recognition) {
        try { recognition.start(); } catch (e) { console.warn(e); }
    } else {
        // fallback: mostra overlay e chiedi di digitare (o inviare file audio al server)
        jarvisSpeechText.textContent = "Il riconoscimento vocale non è supportato in questa build. Puoi inviare messaggi testuali.";
        jarvisCenter.classList.add('speaking');
        setTimeout(() => { jarvisCenter.classList.remove('speaking'); jarvisSpeechText.textContent = ""; }, 2000);
    }
});

voiceStop.addEventListener('click', () => {
    if (recognition && recognizing) recognition.stop();
    voiceStop.classList.add('hidden');
    voiceToggle.classList.remove('hidden');
});

// --- All'avvio: prova a pingare il server (visualmente) ---
(async function init() {
    try {
        // small check; ovviamente il server potrebbe non rispondere a OPTIONS, quindi ignore
        await fetch(API_URL, { method: 'OPTIONS' });
        backendStatus.textContent = 'online';
    } catch (e) {
        backendStatus.textContent = 'offline';
    }
})();
