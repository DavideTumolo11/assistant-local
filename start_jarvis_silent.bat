@echo off
REM JARVIS - Avvio STEALTH (senza finestre, senza controlli)
REM Questo script è ottimizzato per essere lanciato dal .vbs

cd /d "%~dp0"

REM Attiva ambiente virtuale (silenzioso)
call .venv\Scripts\activate.bat 2>nul

REM Avvia server Python in background
start /B python server\websocket_server.py >nul 2>&1

REM Attendi 3 secondi
timeout /t 3 /nobreak >nul

REM Avvia Electron
start "" npm start >nul 2>&1
