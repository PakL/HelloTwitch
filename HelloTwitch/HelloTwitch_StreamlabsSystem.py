import os

ScriptName = "HelloTwitch"
Website = "https://pakl.github.io"
Description = "Will give you a list of viewers that said hello"
Creator = "PakL"
Version = "0.0.1"

def Init():
	Parent.Log(ScriptName, 'Init')
	return

def Execute(data):
	return

def Tick():
	return

def openHelloWindow():
	path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'index.html')
	Parent.Log(ScriptName, 'Open file ' + path)
	os.startfile(path, 'open')
	return
