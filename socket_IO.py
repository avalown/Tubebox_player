from socketIO_client import SocketIO, LoggingNamespace
from player import *
import varglobal as var
import json
import requests
import pickle

def on_new_session_response(arg):
    print(arg)

def on_code(arg):
    print(arg)
	
def on_session(arg):
	var.SESSION  = json.loads(str(arg))
	
#Connection au socket et création d'une nouvelle session
def new_session(id_jukebox):
	print(id_jukebox)
	r = requests.put('http://86.237.132.74:8767/session',{"rpi":id_jukebox})
	print(r.text)
	if os.path.getsize("code_session") != 0:
		code_session = open('code_session','rb')
		code_list = pickle.load(code_session)
		code_session.close()
		if len(code_list) <= 5:
			code_list.append(r.text)
			code_session = open("code_session", "wb")
			pickle.dump(code_list,code_session)
			code_session.close()
		else:
			code_list[0] = r.text
			code_session = open("code_session", "wb")
			pickle.dump(code_list,code_session)
			code_session.close()
	else:
		code_session = open("code_session", "wb")
		code_list = []
		code_list.append(r.text)
		pickle.dump(code_list,code_session)
		code_session.close()
	
def play_session(code):
	r = requests.get('http://86.237.132.74:8767/session',{"code":str(code)})
	print("contenu:" + r.text)
	var.SESSION = json.loads(str(r.text))
	print(var.SESSION)
	# with SocketIO('86.237.132.74',8767,LoggingNamespace) as socketIO:
	#with SocketIO('192.168.0.101',8767,LoggingNamespace) as socketIO:
	#	socketIO.on('session', on_session)
	play_music(code)