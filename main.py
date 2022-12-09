"""
Autor: Rafael Dalzotto (rdalzotto@itba.edu.ar)
Fecha: 7 Dic 2022
"""

import pygame
import numpy as np

from  resistor import getRandomResistValue,drawResist
from button import Button,renderButtons,setButtonFont

from textBoxCheck import TextBoxCheck

from resistor import ResistorElement, ColorCodeElement, E12SeriesElement, ToleranceColorElement

# pygame.init() will initialize all
# imported module
pygame.init()

clock = pygame.time.Clock()

# it will display on screen
screen = pygame.display.set_mode([900, 600])

# basic font for user typed
base_font = pygame.font.Font(None, 32)
medium_font = pygame.font.Font(None, 46)
big_font = pygame.font.Font(None, 58)

# sounds
acierto_sound = pygame.mixer.Sound("acierto.wav")
error_sound = pygame.mixer.Sound("error.wav")
streak_sound = pygame.mixer.Sound("nice_streak.wav")

# INIT VARIABLES
elementList = [
	ResistorElement(screen=screen),
	ColorCodeElement(screen=screen),
	E12SeriesElement(screen=screen),
	ToleranceColorElement(screen=screen),
]

elementId = 0
element = elementList[elementId]

popupAnswer = ""

setButtonFont(base_font)

def swapElement():
	global elementId, elementList, element

	if elementId < (len(elementList)-1):
		elementId += 1
	else:
		elementId = 0
	element = elementList[elementId]

def newElement():
	global elementList, elementId
	elementList[elementId].new()

def flipElement():
	global elementList, elementId
	elementList[elementId].flipOrder()

Button(20, 50, 100, 50, 'Girar', flipElement)
Button(20, 110, 100, 50, 'Nuevo', newElement)
Button(650, 10, 230, 50, 'Cambiar elemento', swapElement)

def textSendEvent(text):
	global popupAnswer
	if(text.replace(' ', '') == element.correctAnswer.replace(' ','')):
		popupAnswer = "CORRECTO!"
		element.streak += 1
		# pygame.mixer.Sound.play()
		acierto_sound.play()
		if (element.streak % 10 == 0):
			streak_sound.play()
	else:
		popupAnswer = "INCORRECTO!"
		element.streak = 0
		error_sound.play()
	
def textResetEvent():
	element.new()

textBox = TextBoxCheck(screen=screen, font=base_font, onSend=textSendEvent, onReset=textResetEvent)


# 	MAIN LOOP

while True:
	# it will set background color of screen
	screen.fill((255, 255, 255))

	textBox.run()
	textBox.draw()

	if textBox.sendFlag:
		text_popup = big_font.render(popupAnswer, True, (0,0,0))
		text_reveal = big_font.render(element.correctAnswer, True, (0,0,0))
		screen.blit(text_reveal, (200, 200))
		screen.blit(text_popup, (200, 200 + text_reveal.get_height() + 100))

	renderButtons(screen)

	text_title = base_font.render(element.title, True, (0,0,0))
	screen.blit(text_title, (200, 5))


	element.draw()

	text_streak = medium_font.render("streak: "+str(element.streak), True, (0,0,0))
	screen.blit(text_streak, (650, 150))

	# update screen
	pygame.display.flip()

	# 60 frames should be passed.
	clock.tick(60)
