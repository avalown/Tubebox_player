import varglobal as var
from socket_IO import *
import RPi.GPIO as GPIO
import time
import pickle

def main_menu(id_jukebox):
	lcd = var.lcd
	empty = 0
	#Ouverture du fichier de codes
	
	if os.path.getsize("code_session") != 0:
		code_session = open('code_session','rb')
		code_list = pickle.load(code_session)
		print(code_list)
		object = json.loads(str(code_list[0]))
		code_session.close()
	else:
		empty = 1
	
	if empty == 0:
		i = 0
		lcd.clear()
		lcd.message('    Session:\n       ' + str(i+1) + '       \x01')	
	else:
		lcd.clear()
		lcd.message(' Creer nouvelle\n\x02   Session    ')
		
	while True:
		#On scan les boutons
		gauche = GPIO.input(17)
		droite = GPIO.input(22)
		ok = GPIO.input(27)
		if empty == 0:
			if gauche == False:
				if i > 0:
					i -= 1
					if i == 0:
						lcd.clear()
						lcd.message('    Session:\n       ' + str(i+1) + '       \x01')
						time.sleep(0.2)
					else:
						lcd.clear()
						lcd.message('    Session:\n\x02      ' + str(i+1) + '       \x01')
						time.sleep(0.2)
						
			if ok == False:		
				if i == len(code_list):
					lcd.clear()
					lcd.message('Nouvelle session\n   En attente')
					new_session(id_jukebox)
				else:
					object = json.loads(str(code_list[i]))
					try:
						os.mkdir("data/" + object["_id"])
					except OSError:
						pass
					play_session(object["_id"])

			if droite == False:
				if i < len(code_list)-1:
					i += 1
					if i == len(code_list)-1:
						lcd.clear()
						lcd.message('    Session:\n\x02      ' + str(i+1) + '       \x01')
						time.sleep(0.2)
					else:
						lcd.clear()
						lcd.message('    Session:\n\x02      ' + str(i+1) + '       \x01')
						time.sleep(0.2)
				else:
					i = len(code_list)
					lcd.clear()
					lcd.message(' Creer nouvelle\n\x02   Session    ')
					time.sleep(0.2)
					
		else:
			if ok == False:		
				lcd.clear()
				lcd.message('Nouvelle session !')
				new_session(id_jukebox)
			