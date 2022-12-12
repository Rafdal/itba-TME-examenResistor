"""
Autor: Rafael Dalzotto (rdalzotto@itba.edu.ar)
Fecha: 7 Dic 2022
"""

import pygame

from button import Button,renderButtons,setButtonFont
from TextBoxCheck import TextBoxCheck

# pygame.init() will initialize all
# imported module
pygame.init()

from Resistors import *
from Capacitors import *

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
	MultiplierElement(screen=screen),
	TantalumElement(screen=screen),
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
Button(650, 10, 230, 50, 'Cambiar test', swapElement)


def isCorrectAnswer(ansLst, correctLst):
	if len(ansLst) == 0:
		return False
		
	for a, correctOpts in zip(ansLst, correctLst):
		if len(a) == 0:
			return False

		foundCorrect = False
		for opt in correctOpts:
			if opt == None or len(opt) == '':
				continue

			# opt = str(opt).rstrip('0').rstrip('.')
			a = a.replace('%','')
			opt = opt.replace('%','')
			if opt == a:
				foundCorrect = True
				break
		if not foundCorrect:
			return False
		else:
			print ('Correct!')
	return True

def textSendEvent(text):
	global popupAnswer
	txtLst = text
	ansLst = element.correctAnswer
	element.totalCount += 1
	if isCorrectAnswer(txtLst, ansLst):
		popupAnswer = "CORRECTO!"
		element.streak += 1
		element.correctCount += 1
		# pygame.mixer.Sound.play()
		acierto_sound.play()
		if (element.streak % 20 == 0):
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

		txtAnswer = ""
		for corrOpts in element.correctAnswer:
			i = 0
			for opt in corrOpts:
				if opt == None or len(opt) == 0:
					i += 1
					continue
				elif i == 0:
					txtAnswer += opt
				elif i == 1:
					txtAnswer += " ({})".format(opt) # hint
				else:
					i += 1
					continue
				txtAnswer += ' '
				i += 1
			txtAnswer += "   "
					
		text_reveal = big_font.render(txtAnswer, True, (0,0,0))
		screen.blit(text_reveal, (200, 250))
		screen.blit(text_popup, (200, 200 + text_reveal.get_height() + 100))

	renderButtons(screen)

	text_title = base_font.render(element.title, True, (0,0,0))
	screen.blit(text_title, (200, 15))


	element.draw()

	precision = 100
	if element.totalCount != 0:
		precision = (element.correctCount / float(element.totalCount))*100.0
	
	text_streak = medium_font.render("streak: "+str(element.streak), True, (0,0,0))
	text_correctCount = base_font.render("correctas: "+str(element.correctCount), True, 'grey')
	text_precision = base_font.render("precision: "+str(int(precision))+'%', True, 'grey')
	screen.blit(text_streak, (650, 150))
	screen.blit(text_correctCount, (650, 185))
	screen.blit(text_precision, (650, 210))

	text_hint = base_font.render(element.hint, True, "grey60")
	screen.blit(text_hint, (150, 450))


	# update screen
	pygame.display.flip()

	# 60 frames should be passed.
	clock.tick(60)
