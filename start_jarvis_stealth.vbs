' ========================================================
' JARVIS AI ASSISTANT - STEALTH LAUNCHER
' Avvia JARVIS senza finestre visibili (modalità invisibile)
' ========================================================

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Ottieni il percorso della directory dove si trova questo script
scriptPath = fso.GetParentFolderName(WScript.ScriptFullName)

' Metodo 1: Esegui il .bat in modalità nascosta
' Il parametro 0 = finestra nascosta, False = non aspettare il completamento
WshShell.Run """" & scriptPath & "\start_jarvis.bat""", 0, False

' Nota: Per chiudere JARVIS in modalità stealth:
' - Apri Task Manager (Ctrl+Shift+Esc)
' - Cerca "python.exe" e "Electron" e chiudi i processi
' OPPURE
' - Crea un file "stop_jarvis.bat" con i comandi di kill
