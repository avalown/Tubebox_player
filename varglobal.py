import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#LCD PIN CONFIGURATION
LCD_RS = 26
LCD_EN = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11
LCD_BACKLIGHT = 4

#LCD colonne et ligne
LCD_COLUMNS = 16
LCD_ROWS = 2

#Initialisation du LCD
lcd = LCD.Adafruit_CharLCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LCD_COLUMNS, LCD_ROWS, LCD_BACKLIGHT)

#Charactere personalisé
#Charactere plein
lcd.create_char(0,[31,31,31,31,31,31,31,31])
#Fleche droite
lcd.create_char(1,[16,24,28,30,30,28,24,16])
#Fleche gauche
lcd.create_char(2,[1,3,7,15,15,7,3,1])

VOL = 50
SESSION = ""
FREEZE = 1
CHARLCD = ""