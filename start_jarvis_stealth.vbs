' ============================================
' J.A.R.V.I.S - AVVIO STEALTH (INVISIBILE)
' ============================================

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Ottieni la cartella dove si trova questo file .vbs
scriptFolder = fso.GetParentFolderName(WScript.ScriptFullName)

' Cambia directory al progetto
WshShell.CurrentDirectory = scriptFolder

' Avvia il server WebSocket usando Python del venv (senza attivare il venv)
' Parametro 0 = finestra nascosta, False = non aspettare
pythonPath = scriptFolder & "\.venv\Scripts\python.exe"
serverScript = scriptFolder & "\server\websocket_server.py"
WshShell.Run """" & pythonPath & """ """ & serverScript & """", 0, False

' Attendi 3 secondi per permettere al server di avviarsi
WScript.Sleep 3000

' Avvia l'interfaccia Electron (invisibile anche questa)
WshShell.Run "cmd.exe /c cd /d """ & scriptFolder & """ && npm start", 0, False

' Per fermare JARVIS in modalità stealth:
' - Esegui stop_jarvis.bat
' - OPPURE apri Task Manager (Ctrl+Shift+Esc) e chiudi python.exe ed electron.exe
