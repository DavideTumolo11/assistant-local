@echo off
REM ============================================
REM JARVIS - Reset Memoria ChromaDB
REM ============================================

echo.
echo ================================================
echo    RESET MEMORIA JARVIS
echo ================================================
echo.
echo ATTENZIONE: Questa operazione cancellerà:
echo   - Tutte le conversazioni salvate
echo   - Tutti i fatti utente (nome, età, preferenze)
echo   - Tutta la knowledge acquisita
echo.

REM Attiva virtual environment
call .venv\Scripts\activate

REM Esegui script Python di reset
python reset_memory.py

echo.
pause
