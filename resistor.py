import secrets	# cryptographic secure random engine
import numpy as np
import pygame
from TestElement import *

IMPRIMIR_VALORES = False		# Imprimir los valores (Para debug)
PROB_RESIST_INVERT = 0.2	# Probabilidad de que la resistencia este al reves (Hay que saber la E12)

# mapa de nombres
resistColorNames = {
	"n":'black',
	"m":'brown',
	"r":'red2',
	"na":'darkorange2',
	"am":'yellow',
	"v":'springgreen2',
	"a":'blue3',
	"vi":'violetred2',
	"g":'grey60',
	"b":'white',
	"d":'goldenrod3',
	"p":'silver',
}

# mapa de multiplicadores
resistColorMult = {
	"n": 0,
	"m": 1,
	"r": 2,
	"na": 3,
	"am": 4,
	"v": 5,
	"a": 6,
	"vi": 7,
	"g": 8,
	"b": 9,
	"d": -1,
	"p": -2,
}

# mapa de tolerancias 'color': [valor, potencia, %tolerancia, tolerancia]
tolColorMult = {
	"m":	[1,		'F'],
	"r":	[2,		'G'],
	"v":	[0.5,	'D'],
	"a":	[0.25,	'C'],
	"vi":	[0.10,	'B'],
	"g":	[0.05,	'-'],
	"d":	[5,		'J'],
	"p":	[10,	'K'],
}

# mapa de codigos
resistColorCodes = {
	'0': "n",
	'1': "m",
	'2': "r",
	'3': "na",
	'4': "am",
	'5': "v",
	'6': "a",
	'7': "vi",
	'8': "g",
	'9': "b",
}

e12series = [
	10.0,
	18.0,
	33.0,
	56.0,
	12.0,
	22.0,
	39.0,
	68.0,
	15.0,
	27.0,
	47.0,
	82.0,
]


def roundResistVal(value):
	highMults = ['u','m','','K','M','G']
	multCount = 0
	if(value >= 1):
		while (value // 1000 > 0):
			value = value / 1000
			multCount += 1
	elif(value < 0.1):
		while (value < 0.1):
			value = value * 1000
			multCount -= 1

	if multCount < -2 or multCount > 3:
		print("OUT OF RANGE:", multCount)
		multCount = 0
	return str(round(value,3)).rstrip('0').rstrip('.') + highMults[2 + multCount]


def e12toColorCodes(e12value):
	e12str = str(round(e12value,3)).rstrip('0').rstrip('.')
	return [resistColorCodes[e12str[0]], resistColorCodes[e12str[1]]]

def tolStrPretty(tolVal):
	return "    "+str(round(tolVal,3)).rstrip('0').rstrip('.') + '%'

def getRandomResistValue():

	# elegir valor de E12
	e12val = secrets.choice(e12series)

	# elegir multiplicador (potencia de 10)
	mult = list(secrets.choice(list(resistColorMult.items())))

	# elegir tolerancia
	tol = list(secrets.choice(list(tolColorMult.items())))

	# Color pairs list
	colorPairs = e12toColorCodes(e12val)
	colorPairs.append(mult[0]) # agrego multiplicador
	colorPairs.append(tol[0])

	value = e12val * (10 ** mult[1])
	valueStrPretty = roundResistVal(value) + tolStrPretty(tol[1][0])

	valueStrRAW = str(round(value,3)).rstrip('0').rstrip('.')

	if(IMPRIMIR_VALORES):
		print('value', valueStrRAW, '\tpretty: "{}"'.format(valueStrPretty), 'codes:', colorPairs)

	if PROB_RESIST_INVERT > 0:
		prob = PROB_RESIST_INVERT
		inverted = np.random.choice([True, False], p=[prob, 1.0 - prob])
		if inverted:
			colorPairs.reverse()

	# hardcoded
	# colorPairs = ["v", "vi", "d", "g", "p"]
	return colorPairs, valueStrPretty


def drawResist(screen, x, y, colorPairs=[[]]):
	baseColor = (150,150,255)
	widthLR = 80
	heightLR = 120
	heightCenter = 80
	centerOffset = (heightLR//2) - (heightCenter//2)
	distLR = 255
	rectL = pygame.Rect(x, y, widthLR, heightLR)
	rectR = pygame.Rect(x+distLR, y, widthLR, heightLR)
	rectCenter = pygame.Rect(x+widthLR, y+centerOffset, distLR-widthLR, heightCenter)
	pygame.draw.rect(screen, baseColor, rectL, border_radius=15)
	pygame.draw.rect(screen, baseColor, rectR, border_radius=15)
	pygame.draw.rect(screen, baseColor, rectCenter)
	bandStepX = 20

	for color in colorPairs:
		rectColorBand = pygame.Rect(x+widthLR+bandStepX, y+centerOffset, 20, heightCenter)
		pygame.draw.rect(screen, resistColorNames[color], rectColorBand)
		bandStepX += 35




class ResistorElement(TestElement):

	def __init__(self, screen):
		self.title = "Resistor"
		self.screen = screen
		self.colorCodes, self.correctAnswer = getRandomResistValue()

	def new(self):
		self.colorCodes, self.correctAnswer = getRandomResistValue()

	def flipOrder(self):
		self.colorCodes.reverse()

	# instance method
	def draw(self):
		drawResist(self.screen, 200, 60, self.colorCodes)



class ColorCodeElement(TestElement):

	def __init__(self, screen):
		self.title = "Codigo de color"
		self.screen = screen
		self.correctAnswer, self.color = self._getRandomColorCode()

	def new(self):
		self.correctAnswer, self.color = self._getRandomColorCode()

	def flipOrder(self):
		_ = None

	def _getRandomColorCode(self):
		colorPair = list(secrets.choice(list(resistColorCodes.items())))
		return colorPair[0], colorPair[1]

	# instance method
	def draw(self):
		rect = pygame.Rect(400, 100, 100, 100)
		border = pygame.Rect(rect.left-1, rect.top-1, rect.width+2, rect.height+2)
		pygame.draw.rect(self.screen, 'black', border, border_radius=16)
		pygame.draw.rect(self.screen, resistColorNames[self.color], rect, border_radius=15)

class E12SeriesElement(TestElement):

	def __init__(self, screen):
		self.title = "Valor normalizado E12 (10%)"
		self.screen = screen
		self.correctAnswer, self.colorPair = self._getRandomCode()

	def new(self):
		self.correctAnswer, self.colorPair = self._getRandomCode()

	def flipOrder(self):
		self.colorPair.reverse()

	def _getRandomCode(self):
		e12value = secrets.choice(e12series)
		e12str = str(round(e12value,3)).rstrip('0').rstrip('.')
		colorPair = e12toColorCodes(e12value)

		inverted = np.random.choice([True, False], p=[0.5, 0.5])
		if inverted:
			colorPair.reverse()

		return e12str, colorPair

	# instance method
	def draw(self):
		rect1 = pygame.Rect(250, 100, 100, 100)
		rect2 = pygame.Rect(250+rect1.width, 100, 100, 100)
		border1 = pygame.Rect(rect1.left-1, rect1.top-1, rect1.width+2, rect1.height+2)
		border2 = pygame.Rect(rect2.left-1, rect2.top-1, rect2.width+2, rect2.height+2)
		pygame.draw.rect(self.screen, 'black', border1, border_radius=16)
		pygame.draw.rect(self.screen, 'black', border2, border_radius=16)
		pygame.draw.rect(self.screen, resistColorNames[self.colorPair[0]], rect1, border_radius=15)
		pygame.draw.rect(self.screen, resistColorNames[self.colorPair[1]], rect2, border_radius=15)