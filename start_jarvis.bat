@echo off
title JARVIS - Avvio Sistema
color 0B
cls
echo.
echo ============================================
echo        J.A.R.V.I.S AI ASSISTANT
echo ============================================
echo.

REM Vai sempre nella cartella dove si trova questo .bat
cd /d "%~dp0"

echo Percorso progetto: %CD%
echo.

REM ===== CHECK PYTHON =====
echo [1/4] Controllo Python...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo [ERRORE] Python NON trovato!
    echo.
    echo Scarica Python da: https://www.python.org/downloads/
    echo IMPORTANTE: Spunta "Add Python to PATH"!
    echo.
    pause
    exit /b 1
)
python --version
echo OK!
echo.

REM ===== CHECK NODE.JS =====
echo [2/4] Controllo Node.js...
npm --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo [ERRORE] Node.js NON trovato!
    echo.
    echo Scarica Node.js da: https://nodejs.org/
    echo.
    pause
    exit /b 1
)
npm --version
echo OK!
echo.

REM ===== AMBIENTE VIRTUALE =====
echo [3/4] Ambiente virtuale Python...
if not exist ".venv" (
    echo Creo ambiente virtuale...
    python -m venv .venv
    if errorlevel 1 (
        color 0C
        echo ERRORE nella creazione!
        pause
        exit /b 1
    )
    echo Creato!
)

echo Attivo ambiente virtuale...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    color 0C
    echo ERRORE nell'attivazione!
    pause
    exit /b 1
)
echo OK!
echo.

REM ===== DIPENDENZE =====
echo [4/4] Installo websockets (se mancante)...
pip install websockets >nul 2>&1
echo OK!
echo.

REM ===== AVVIO JARVIS =====
echo ============================================
echo           AVVIO COMPONENTI
echo ============================================
echo.

echo [BACKEND] Avvio server WebSocket (porta 8765)...
start /B .venv\Scripts\pythonw.exe server\websocket_server.py
echo Avviato in background (nessuna finestra)!
echo.

echo Attendo 4 secondi per il backend...
timeout /t 4 /nobreak >nul
echo.

echo [FRONTEND] Avvio interfaccia Electron...
echo.
echo ============================================
echo    JARVIS AVVIATO! Questa finestra si chiudera'
echo    Per chiudere JARVIS: stop_jarvis.bat
echo ============================================
timeout /t 2 /nobreak >nul

start "" npm start

REM Chiudi questa finestra CMD
exit
