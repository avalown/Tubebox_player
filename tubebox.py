#!/usr/bin/python3.5
# -*-coding:utf-8 -*

import os
import math
import string
import varglobal as var
from interface import *

#Lecture id  jukebox
id = open('id','r')
id_jukebox = id.read()
id.close() 

#Gestion du Volume
#On définie le volume au demarage a 50%
os.system("amixer set PCM " + str(var.VOL) + "%")

#On affiche le menu
main_menu(id_jukebox)
