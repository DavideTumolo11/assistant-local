@echo off
title Avvio Jarvis Assistant
echo ===========================================
echo     AVVIO ASSISTANT LOCALE - BY DAVIDE
echo ===========================================

REM Attiva l'ambiente virtuale
call .venv\Scripts\activate

REM Avvia il server WebSocket in una nuova finestra
start cmd /k "python server\websocket_server.py"

REM Aspetta 3 secondi per dare tempo al server di avviarsi
timeout /t 3 /nobreak >nul

REM Avvia l'interfaccia grafica Electron
npm start
