Set WshShell = CreateObject("WScript.Shell")

' Percorso base del progetto
projectPath = "C:\Users\Davide\assistant-local"

' Attiva il virtual environment e avvia il server WebSocket in background
WshShell.Run "cmd /c cd /d " & projectPath & " && call .venv\Scripts\activate && python server\websocket_server.py", 0, False

' Attendi qualche secondo per permettere al server WebSocket di partire
WScript.Sleep 3000

' Avvia l'interfaccia Electron
WshShell.Run "cmd /c cd /d " & projectPath & " && npm start", 0, False
