import os
import json
import re
import codecs

ScriptName = "HelloTwitch"
Website = "https://github.com/PakL/HelloTwitch"
Description = "Will give you a list of viewers that said hello (Please right-click + Insert API key)"
Creator = "PakL"
Version = "0.0.2"

ht_phrases = []
ht_users = {}

def SetupSettings(data):
	global ht_phrases
	Parent.Log(ScriptName, "Set up settings")

	ht_phrases = data["filterPhrases"].split(';')
	for index in range(len(ht_phrases)):
		ht_phrases[index] = ht_phrases[index].strip()
	return

def Init():
	Parent.Log(ScriptName, 'Preparing script')
	try:
		filepath = os.path.join(os.path.dirname(__file__), "settings.json")
		with codecs.open(filepath, encoding='utf-8-sig', mode='r') as file:
			data = json.load(file, encoding='utf-8-sig')
			SetupSettings(data)
	except:
		Parent.Log(ScriptName, "Could not load settings")
		return
	Parent.Log(ScriptName, 'Done')
	return

def Execute(data):
	global ht_users
	if len(data.User) > 0 and data.IsChatMessage() and data.IsFromTwitch():
		if not data.IsWhisper():
			doesMatch = False
			if len(''.join(ht_phrases)) <= 0:
				doesMatch = True
			else:
				for index in range(len(ht_phrases)):
					match = re.search("(^| )" + re.escape(ht_phrases[index]) + "( |$)", data.Message, re.IGNORECASE)
					if match:
						doesMatch = True
			if doesMatch:
				Parent.Log(ScriptName, 'Found matching message from ' + data.User + ': ' + data.Message)
				ht_users[data.User] = data.UserName
				Parent.Log(ScriptName, ', '.join(ht_users))

	Parent.BroadcastWsEvent("HELLO_TWITCH_GREETING", json.dumps(ht_users))
	return

def Tick():
	#Parent.BroadcastWsEvent("HELLO_TWITCH_GREETING", json.dumps(ht_users))
	return

def ReloadSettings(jsonData):
	global ht_phrases
	Parent.Log(ScriptName, "Loading settings")
	try:
		data = json.loads(jsonData)
		SetupSettings(data)
	except:
		Parent.Log(ScriptName, "Could not load settings")
		return
	return

def openHelloWindow():
	path = os.path.join(os.path.dirname(__file__), 'frame', 'index.html')
	Parent.Log(ScriptName, "Open file " + path)
	os.startfile(path, 'open')
	return

def clearUserList():
	global ht_users
	ht_users = {}
	Parent.BroadcastWsEvent("HELLO_TWITCH_GREETING", json.dumps(ht_users))
	return