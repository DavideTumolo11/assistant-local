@echo off
title JARVIS - Stop
color 0C
cls
echo.
echo ============================================
echo        CHIUSURA J.A.R.V.I.S
echo ============================================
echo.

echo Chiudo server Python...
taskkill /FI "WINDOWTITLE eq JARVIS Backend*" /F >nul 2>&1
taskkill /IM python.exe /F >nul 2>&1
echo OK!

echo Chiudo interfaccia Electron...
taskkill /IM electron.exe /F >nul 2>&1
echo OK!

echo.
echo ============================================
echo       JARVIS FERMATO COMPLETAMENTE
echo ============================================
echo.
timeout /t 2
