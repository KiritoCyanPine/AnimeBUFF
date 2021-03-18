siteA = "http://localhost:8123/"
Const OneSecond = 1000 
Set browobj = CreateObject("Wscript.Shell")
browobj.Run "shell:AppsFolder\Microsoft.MicrosoftEdge_8wekyb3d8bbwe!MicrosoftEdge http://localhost:8123/"
'-url "&siteA
WScript.Sleep 1500
browobj.AppActivate "MicrosoftEdge"
browobj.SendKeys "~"
browobj.SendKeys "{F11}"