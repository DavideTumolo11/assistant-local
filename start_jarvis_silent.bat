@echo off
REM JARVIS - Avvio STEALTH (senza finestre, senza controlli)

cd /d "%~dp0"

REM Attiva ambiente virtuale
call .venv\Scripts\activate.bat

REM Avvia server Python senza finestra
start /B .venv\Scripts\pythonw.exe server\websocket_server.py

REM Attendi 4 secondi
timeout /t 4 /nobreak >nul

REM Avvia Electron in background (senza finestra)
start /B npm start

REM Chiudi questa finestra CMD
exit
