import os
import json
import re
import codecs

from time import localtime, strftime

ScriptName = "HelloTwitch"
Website = "https://github.com/PakL/HelloTwitch"
Description = "Will give you a list of viewers that said hello (Please right-click + Insert API key)"
Creator = "PakL"
Version = "0.0.4"

ht_phrases = []
ht_users = []
ht_usersListed = {}

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
				AppendUserToList(data.User, data.UserName)


				AppendUserToList('aaa', 'aaa')
				AppendUserToList('zzz', 'zzz')
				AppendUserToList('ggg', 'ggg')
				AppendUserToList('uuu', 'uuu')
				AppendUserToList('ccc', 'ccc')

				AppendUserToList('bbb', 'bbb')
				AppendUserToList('yyy', 'yyy')
				AppendUserToList('hhh', 'hhh')
				AppendUserToList('ppp', 'ppp')
				AppendUserToList('ttt', 'ttt')


				AppendUserToList('aaaaaaa', 'aaaaaaa')
				AppendUserToList('bbbbbbb', 'bbbbbbb')
				AppendUserToList('ccccccc', 'ccccccc')
				AppendUserToList('ddddddd', 'ddddddd')
				AppendUserToList('eeeeeee', 'eeeeeee')
				AppendUserToList('fffffff', 'fffffff')
				AppendUserToList('ggggggg', 'ggggggg')
				AppendUserToList('hhhhhhh', 'hhhhhhh')
				AppendUserToList('iiiiiii', 'iiiiiii')
				AppendUserToList('jjjjjjj', 'jjjjjjj')
				AppendUserToList('kkkkkkk', 'kkkkkkk')
				AppendUserToList('lllllll', 'lllllll')
				AppendUserToList('mmmmmmm', 'mmmmmmm')
				AppendUserToList('nnnnnnn', 'nnnnnnn')
				AppendUserToList('ooooooo', 'ooooooo')
				AppendUserToList('ppppppp', 'ppppppp')
				AppendUserToList('qqqqqqq', 'qqqqqqq')
				AppendUserToList('rrrrrrr', 'rrrrrrr')
				AppendUserToList('sssssss', 'sssssss')
				AppendUserToList('ttttttt', 'ttttttt')
				AppendUserToList('uuuuuuu', 'uuuuuuu')
				AppendUserToList('vvvvvvv', 'vvvvvvv')
				AppendUserToList('wwwwwww', 'wwwwwww')
				AppendUserToList('xxxxxxx', 'xxxxxxx')
				AppendUserToList('yyyyyyy', 'yyyyyyy')
				AppendUserToList('zzzzzzz', 'zzzzzzz')

	Parent.BroadcastWsEvent("HELLO_TWITCH_GREETING", json.dumps(ht_users))
	return

def Tick():
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