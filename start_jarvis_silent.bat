@echo off
REM JARVIS - Avvio STEALTH (senza finestre, senza controlli)

cd /d "%~dp0"

REM Attiva ambiente virtuale
call .venv\Scripts\activate.bat

REM Avvia server Python in nuova finestra nascosta
start /MIN "JARVIS Backend" python server\websocket_server.py

REM Attendi 4 secondi
timeout /t 4 /nobreak >nul

REM Avvia Electron
start "" npm start
