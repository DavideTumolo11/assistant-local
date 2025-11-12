' ============================================
' J.A.R.V.I.S - AVVIO STEALTH (INVISIBILE)
' ============================================

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Ottieni la cartella dove si trova questo file .vbs
scriptFolder = fso.GetParentFolderName(WScript.ScriptFullName)

' Avvia start_jarvis_silent.bat (versione ottimizzata per stealth)
' Parametro 0 = finestra nascosta, False = non aspettare
WshShell.Run "cmd.exe /c """ & scriptFolder & "\start_jarvis_silent.bat""", 0, False

' Per fermare JARVIS in modalità stealth:
' - Esegui stop_jarvis.bat
' - OPPURE apri Task Manager (Ctrl+Shift+Esc) e chiudi python.exe ed electron.exe
