import pafy
import os
import time
import RPi.GPIO as GPIO
from threading import Thread
import varglobal as var
from subprocess import Popen

lcd = var.lcd

class defreeze(Thread):
	def __init__(self):
		Thread.__init__(self)
	def run(self):
		time.sleep(3)
		var.FREEZE = 0

class lcd_move(Thread):
	def __init__(self, code):
		Thread.__init__(self)
		self.code = code

	def run(self):
		i = 1
		while True:
			if var.FREEZE == 0:
				nbcharlcd = len(var.CHARLCD)
				lcd.clear()
				lcd.message('   Code: ' + str(self.code) + '\n' + var.CHARLCD[i:nbcharlcd])
				i += 1
				time.sleep(0.5)
				if i == (nbcharlcd):
					i = 1
			
class play(Thread):
	def __init__(self, code):
		Thread.__init__(self)
		self.code = code
	
	def run(self):
		while True:
			if var.SESSION == {}:
				lcd.clear()
				lcd.message('      ' + str(self.code) + '\n  Session vide')
			for song in var.SESSION:
				video = pafy.new(var.SESSION[song])
				lcd.clear()
				lcd.message('   Chargement   \n	en cours	')
				bestaudio = video.getbestaudio()
				sound = song + '.' + bestaudio.extension
				bestaudio.download(filepath = str(self.code) + '/' + sound )
				lcd.clear()
				lcd.message('   Chargement   \n	Terminer	')
				var.CHARLCD = video.title
				var.FREEZE = 0
				time.sleep(1)
				in_play = Popen(['mplayer', 'data' + str(self.code) + '/' + sound])
				in_play.wait()
		
class player_command(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		i = 1
		while True:
			#On scan les boutons
			voldown = GPIO.input(20)
			volup = GPIO.input(21)
			if voldown == False:
				if var.VOL > 0:
					var.FREEZE = 1
					volumedown()
					i += 1
			
			if volup == False:
				if var.VOL < 100:
					var.FREEZE = 1
					volumeup()
					i += 1
			
#Fonction lecture
def play_music(code):	
	proc_play = play(code)
	proc_volume = player_command()
	proc_lcd = lcd_move(code)
	proc_lcd.start()
	proc_play.start()
	proc_volume.start()
	proc_lcd.join()
	proc_play.join()
	proc_volume.join()

def volume():
	os.system("amixer set PCM " + str(var.VOL) + "%")

def volumedown():
	var.VOL -= 10
	k = 0
	l = 0
	volume()
	nbcharvol = var.VOL/10
	nbcharset = 10 - nbcharvol
	lcd.clear()
	lcd.message("Volume:\n")
	lcd.message("[")
	while k < nbcharvol:
		lcd.message('\x00')
		k += 1
	while l < nbcharset:
		lcd.message(' ')
		l += 1
	lcd.message('] ' + str(var.VOL) + '%')
	time.sleep(0.1)
	
def volumeup():
	var.VOL += 10
	k = 0
	l = 0
	volume()
	nbcharvol = var.VOL/10
	nbcharset = 10 - nbcharvol
	lcd.clear()
	lcd.message("Volume:\n")
	lcd.message("[")
	while k < nbcharvol:
		lcd.message('\x00')
		k += 1
	while l < nbcharset:
		lcd.message(' ')
		l += 1
	lcd.message('] ' + str(var.VOL) + '%')
	time.sleep(0.1)