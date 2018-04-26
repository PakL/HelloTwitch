import os
import json
import re
import codecs

from time import localtime, strftime

ScriptName = "HelloTwitch"
Website = "https://github.com/PakL/HelloTwitch"
Description = "Will give you a list of viewers that said hello (Please right-click + Insert API key)"
Creator = "PakL"
Version = "0.0.3"

ht_phrases = []
ht_users = {}

def SetupSettings(data):
	global ht_phrases
	Parent.Log(ScriptName, '[' + strftime("%H:%M:%S", localtime()) + "] Set up settings")

	ht_phrases = data["filterPhrases"].split(';')
	for index in range(len(ht_phrases)):
		ht_phrases[index] = ht_phrases[index].strip()
	return

def Init():
	Parent.Log(ScriptName, '[' + strftime("%H:%M:%S", localtime()) + "] Preparing script")
	try:
		filepath = os.path.join(os.path.dirname(__file__), "settings.json")
		with codecs.open(filepath, encoding='utf-8-sig', mode='r') as file:
			data = json.load(file, encoding='utf-8-sig')
			SetupSettings(data)
	except:
		Parent.Log(ScriptName, '[' + strftime("%H:%M:%S", localtime()) + "] Could not load settings")
		return
	Parent.Log(ScriptName, '[' + strftime("%H:%M:%S", localtime()) + '] Done')
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
				Parent.Log(ScriptName, '[' + strftime("%H:%M:%S", localtime()) + "] Found matching message from " + data.User + ': ' + data.Message)
				ht_users[data.User] = data.UserName
				Parent.Log(ScriptName, '[' + strftime("%H:%M:%S", localtime()) + "] Users in the list now: " + ', '.join(ht_users))

	Parent.BroadcastWsEvent("HELLO_TWITCH_GREETING", json.dumps(ht_users))
	return

def Tick():
	return

def ReloadSettings(jsonData):
	global ht_phrases
	Parent.Log(ScriptName, '[' + strftime("%H:%M:%S", localtime()) + "] Loading settings")
	try:
		data = json.loads(jsonData)
		SetupSettings(data)
	except:
		Parent.Log(ScriptName, '[' + strftime("%H:%M:%S", localtime()) + "] Could not load settings")
		return
	return

def openHelloWindow():
	path = os.path.join(os.path.dirname(__file__), 'frame', 'index.html')
	Parent.Log(ScriptName, '[' + strftime("%H:%M:%S", localtime()) + "] Open file " + path)
	os.startfile(path, 'open')
	return

def clearUserList():
	global ht_users
	ht_users = {}
	Parent.BroadcastWsEvent("HELLO_TWITCH_GREETING", json.dumps(ht_users))
	return