"""
Autor: Rafael Dalzotto (rdalzotto@itba.edu.ar)
Fecha: 7 Dic 2022
"""

import pygame
import numpy as np

from  resistor import getRandomResistValue,drawResist
from button import Button,renderButtons,setButtonFont

from textBoxCheck import TextBoxCheck

# pygame.init() will initialize all
# imported module
pygame.init()

clock = pygame.time.Clock()

# it will display on screen
screen = pygame.display.set_mode([800, 600])

# basic font for user typed
base_font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 58)


# INIT VARIABLES

colorCodes, valueStr = getRandomResistValue()

drawNewResist = True

popupAnswer = ""

def flipResistor():
	colorCodes.reverse()	

def newResistor():
	global drawNewResist
	drawNewResist = True

setButtonFont(base_font)

Button(20, 50, 100, 50, 'Girar', flipResistor)
Button(20, 110, 100, 50, 'Nuevo', newResistor)

def textSendEvent(text):
	global popupAnswer
	if(text.replace(' ', '') == valueStr.replace(' ','')):
		popupAnswer = "CORRECTO!"
	else:
		popupAnswer = "INCORRECTO!"
	
def textResetEvent():
	global drawNewResist
	drawNewResist = True


textBox = TextBoxCheck(screen=screen, font=base_font, onSend=textSendEvent, onReset=textResetEvent)

# 	MAIN LOOP

while True:
	# it will set background color of screen
	screen.fill((255, 255, 255))

	textBox.run()

	textBox.draw()

	if textBox.sendFlag:
		text_popup = big_font.render(popupAnswer, True, (0,0,0))
		text_reveal = big_font.render(valueStr, True, (0,0,0))

		screen.blit(text_reveal, (200, 200))
		screen.blit(text_popup, (200, 200 + text_reveal.get_height() + 100))

	renderButtons(screen)

	if(drawNewResist):
		# dibujar el resist
		colorCodes, valueStr = getRandomResistValue()
		drawNewResist = False

	drawResist(screen, 200, 60, colorCodes)

	# update screen
	pygame.display.flip()

	# 60 frames should be passed.
	clock.tick(60)
