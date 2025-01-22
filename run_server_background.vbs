Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw """ & WshShell.CurrentDirectory & "\server.py""", 0, False
