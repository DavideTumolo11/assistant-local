@echo off
title JARVIS - Stop Sistema
color 0C
echo.
echo ========================================================
echo              JARVIS AI ASSISTANT - STOP
echo ========================================================
echo.
echo Chiusura componenti JARVIS in corso...
echo.

REM Chiudi server Python WebSocket
echo [1/2] Chiudo server WebSocket...
taskkill /FI "WINDOWTITLE eq JARVIS Backend*" /F >nul 2>&1
taskkill /IM python.exe /F >nul 2>&1
echo [OK] Server Python chiuso

REM Chiudi Electron
echo [2/2] Chiudo interfaccia Electron...
taskkill /IM electron.exe /F >nul 2>&1
echo [OK] Interfaccia Electron chiusa

echo.
echo ========================================================
echo           JARVIS TERMINATO COMPLETAMENTE
echo ========================================================
echo.
timeout /t 3
