Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "ollama serve", 0, False
WScript.Sleep 3000
WshShell.Run "pythonw C:\Users\Ayaan\gen-z-assistant\assistant.py", 0, False