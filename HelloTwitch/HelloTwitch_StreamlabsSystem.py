import os
import json
import re
import codecs

from time import localtime, strftime

ScriptName = "HelloTwitch"
Website = "https://github.com/PakL/HelloTwitch"
Description = "Will give you a list of viewers that said hello (Please right-click + Insert API key)"
Creator = "PakL"
Version = "0.1.1"

ht_phrases = []
ht_userFilter = []
ht_users = []
ht_usersListed = {}
ht_wasOnline = False

def SetupSettings(data):
	global ht_phrases, ht_userFilter
	Parent.Log(ScriptName, '[' + strftime("%H:%M:%S", localtime()) + "] Set up settings")

	ht_phrases = data["filterPhrases"].split(';')
	for index in range(len(ht_phrases)):
		ht_phrases[index] = ht_phrases[index].strip()

	ht_userFilter = data["filterUsers"].split(';')
	for index in range(len(ht_userFilter)):
		ht_userFilter[index] = ht_userFilter[index].strip()
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
	if len(data.User) > 0 and data.IsChatMessage() and data.IsFromTwitch():
		if not data.IsWhisper():
			onMessage(data)

	if ht_wasOnline and not Parent.IsLive():
		clearUserList()
	ht_wasOnline = Parent.IsLive()
	Parent.BroadcastWsEvent("HELLO_TWITCH_GREETING", json.dumps(ht_users))
	return

def Tick():
	return

def onMessage(data):
	doesMatch = False
	doFilter = False

	if len(''.join(ht_phrases)) <= 0:
		doesMatch = True
	else:
		for index in range(len(ht_phrases)):
			match = re.search("(^| )" + re.escape(ht_phrases[index]) + "( |$)", data.Message, re.IGNORECASE)
			if match:
				doesMatch = True

	if len(''.join(ht_userFilter)) > 0:
		for index in range(len(ht_userFilter)):
			if data.User.lower() == ht_userFilter[index].lower():
				doFilter = True
	
	if doesMatch and not doFilter:
		Parent.Log(ScriptName, '[' + strftime("%H:%M:%S", localtime()) + "] Found matching message from " + data.User + ': ' + data.Message)
		AppendUserToList(data.User, data.UserName)

	return


def AppendUserToList(user, username):
	global ht_users, ht_usersListed
	if not user in ht_usersListed:
		ht_users.append(username)
		ht_usersListed[user] = username
		Parent.Log(ScriptName, '[' + strftime("%H:%M:%S", localtime()) + "] Users in the list now: " + ', '.join(ht_users))


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
	global ht_users, ht_usersListed
	ht_users = []
	ht_usersListed = {}
	Parent.BroadcastWsEvent("HELLO_TWITCH_GREETING", json.dumps(ht_users))
	return

def debugMessages():
	onMessage(type('',(object,),{"User": "uSera", "UserName": "UserA", "Message": "Hello"})())
	onMessage(type('',(object,),{"User": "usErb", "UserName": "UserB", "Message": "Hi"})())
	onMessage(type('',(object,),{"User": "userc", "UserName": "UserC", "Message": "Hey"})())
	onMessage(type('',(object,),{"User": "userd", "UserName": "UserD", "Message": "What's up?"})())

	Parent.BroadcastWsEvent("HELLO_TWITCH_GREETING", json.dumps(ht_users))
	return