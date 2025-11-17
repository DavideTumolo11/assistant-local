' ============================================
' J.A.R.V.I.S - AVVIO STEALTH (INVISIBILE)
' ============================================

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Ottieni la cartella dove si trova questo file .vbs
scriptFolder = fso.GetParentFolderName(WScript.ScriptFullName)

' Cambia directory al progetto
WshShell.CurrentDirectory = scriptFolder

' Avvia il server WebSocket in background (invisibile)
' Parametro 0 = finestra nascosta, False = non aspettare
WshShell.Run "cmd.exe /c cd /d """ & scriptFolder & """ && call .venv\Scripts\activate && python server\websocket_server.py", 0, False

' Attendi 3 secondi per permettere al server di avviarsi
WScript.Sleep 3000

' Avvia l'interfaccia Electron (invisibile anche questa)
WshShell.Run "cmd.exe /c cd /d """ & scriptFolder & """ && npm start", 0, False

' Per fermare JARVIS in modalità stealth:
' - Esegui stop_jarvis.bat
' - OPPURE apri Task Manager (Ctrl+Shift+Esc) e chiudi python.exe ed electron.exe
