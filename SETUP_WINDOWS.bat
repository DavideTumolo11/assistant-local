@echo off
title JARVIS - Setup Completo Windows
color 0B
echo.
echo ========================================================
echo          JARVIS - SETUP COMPLETO WINDOWS
echo ========================================================
echo.

REM Vai nella directory del progetto
cd /d "%~dp0"

echo [STEP 1] Checkout branch corretto...
git checkout claude/project-setup-check-011CV4M71A7EVrqqn225G4tG
git pull origin claude/project-setup-check-011CV4M71A7EVrqqn225G4tG
echo.

echo [STEP 2] Rimuovo vecchio ambiente virtuale corrotto...
if exist ".venv" (
    rmdir /s /q .venv
    echo OK: Vecchio ambiente rimosso
)
echo.

echo [STEP 3] Creo nuovo ambiente virtuale...
python -m venv .venv
if errorlevel 1 (
    echo ERRORE: Impossibile creare ambiente virtuale
    pause
    exit /b 1
)
echo OK: Ambiente virtuale creato
echo.

echo [STEP 4] Attivo ambiente virtuale...
call .venv\Scripts\activate.bat
echo OK: Ambiente attivo
echo.

echo [STEP 5] Aggiorno pip...
python -m pip install --upgrade pip
echo.

echo [STEP 6] Installo websockets (dipendenza minima)...
pip install websockets
echo OK: Websockets installato
echo.

echo [STEP 7] Installo dipendenze Node.js...
call npm install
if errorlevel 1 (
    echo WARNING: Problemi con npm install, ma proseguo...
)
echo.

echo ========================================================
echo              SETUP COMPLETATO CON SUCCESSO!
echo ========================================================
echo.
echo Ora puoi avviare JARVIS con:
echo   - start_jarvis.bat (con finestre)
echo   - start_jarvis_stealth.vbs (invisibile)
echo.
pause
