@echo off
title JARVIS AI Assistant - Avvio Sistema
color 0B
echo.
echo ========================================================
echo           JARVIS AI ASSISTANT - AVVIO SISTEMA
echo                    BY DAVIDE TUMOLO
echo ========================================================
echo.

REM Vai nella directory del progetto
cd /d "%~dp0"

REM ============================================
REM STEP 1: Controlla Python
REM ============================================
echo [1/5] Verifica Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRORE] Python non trovato!
    echo.
    echo Installa Python da: https://www.python.org/downloads/
    echo IMPORTANTE: Spunta "Add Python to PATH" durante installazione!
    echo.
    pause
    exit /b 1
)
echo [OK] Python trovato
echo.

REM ============================================
REM STEP 2: Controlla/Crea ambiente virtuale
REM ============================================
echo [2/5] Verifica ambiente virtuale...
if not exist ".venv" (
    echo [INFO] Ambiente virtuale non trovato, lo creo...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERRORE] Impossibile creare ambiente virtuale!
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtuale creato
) else (
    echo [OK] Ambiente virtuale trovato
)
echo.

REM ============================================
REM STEP 3: Attiva ambiente virtuale
REM ============================================
echo [3/5] Attivazione ambiente virtuale...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRORE] Impossibile attivare ambiente virtuale!
    pause
    exit /b 1
)
echo [OK] Ambiente virtuale attivo
echo.

REM ============================================
REM STEP 4: Installa dipendenze Python
REM ============================================
echo [4/5] Verifica dipendenze Python...
pip show websockets >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installo dipendenze Python (potrebbe richiedere alcuni minuti)...
    pip install websockets
    if errorlevel 1 (
        echo [WARNING] Alcune dipendenze potrebbero non essere installate
        echo Il sistema funzionera' in modalita' base
    )
) else (
    echo [OK] Dipendenze base trovate
)
echo.

REM ============================================
REM STEP 5: Verifica Node.js/npm
REM ============================================
echo [5/5] Verifica Node.js...
npm --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRORE] Node.js/npm non trovato!
    echo.
    echo Installa Node.js da: https://nodejs.org/
    echo.
    pause
    exit /b 1
)
echo [OK] Node.js trovato
echo.

REM ============================================
REM AVVIO JARVIS
REM ============================================
echo ========================================================
echo                  AVVIO COMPONENTI JARVIS
echo ========================================================
echo.

echo [BACKEND] Avvio server WebSocket Python (porta 8765)...
echo.
start "JARVIS Backend - WebSocket Server" cmd /k "python server\websocket_server.py"

echo [INFO] Attendo 3 secondi per avvio backend...
timeout /t 3 /nobreak >nul
echo.

echo [FRONTEND] Avvio interfaccia Electron...
echo.
npm start

REM Se Electron si chiude, chiudi anche il backend
echo.
echo [INFO] Interfaccia chiusa. Chiudo componenti...
taskkill /FI "WINDOWTITLE eq JARVIS Backend*" /F >nul 2>&1
echo.
echo ========================================================
echo              JARVIS TERMINATO CORRETTAMENTE
echo ========================================================
echo.
pause
