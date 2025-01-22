Set WshShell = CreateObject("WScript.Shell")
StartupFolder = WshShell.SpecialFolders("Startup")
Set link = WshShell.CreateShortcut(StartupFolder & "\YouTube Viewer Server.lnk")
link.TargetPath = WshShell.CurrentDirectory & "\run_server_background.vbs"
link.WorkingDirectory = WshShell.CurrentDirectory
link.Save
