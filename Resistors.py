import secrets	# cryptographic secure random engine
import numpy as np
import pygame
from TestElement import *
from utils import *

IMPRIMIR_VALORES = False		# Imprimir los valores (Para debug)
PROB_RESIST_INVERT = 0.2	# Probabilidad de que la resistencia este al reves (Hay que saber la E12)

# mapa de nombres
resistColorNames = {
	"n":'black',
	"m":'brown4',
	"r":'red2',
	"na":'darkorange2',
	"am":'yellow',
	"v":'springgreen2',
	"a":'blue3',
	# "vi":'blueviolet',
	# "vi":'violetred2',
	"vi":'magenta3',
	"g":'grey45',
	"b":'white',
	# "d":'orange3',
	"d":'darkgoldenrod3',
	"p":'grey85',
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

# mapa de tolerancias 'color': [valor, potencia, %tolerancia, tolerancia]
tolColorMult = [
	["m",	1.0,	'F'],
	["r",	2.0,	'G'],
	["v",	0.5,	'D'],
	["a",	0.25,	'C'],
	["vi",	0.10,	'B'],
	["g",	0.05,	'-'],
	["d",	5.0,	'J'],
	["p",	10.0,	'K'],
]


def e12toColorCodes(e12str):
	colorCodeLst = []
	for c in e12str:
		colorCodeLst.append(resistColorCodes[c])
	return colorCodeLst

def tolStrPretty(tolVal):
	return "    "+str(round(tolVal,3)).rstrip('0').rstrip('.') + '%'

def getRandomResistValue():
	
	pTol = [0.05, 0.07, 0.05, 0.01, 0.01, 0.01, 0.4, 0.4]	# probabilitades

	# elegir tolerancia
	tolID = np.random.choice(list(range(8)), p=pTol)
	tol = tolColorMult[tolID]

	eSeriesVal = ''
	if tol[1] == 10.0:
		eSeriesVal = secrets.choice(e12series)
	elif tol[1] == 5.0:
		eSeriesVal = secrets.choice(e24series)
	elif tol[1] == 2.0:
		eSeriesVal = secrets.choice(e48series)
	else:
		eSeriesVal = secrets.choice(e96series)

	# elegir multiplicador (potencia de 10)
	mult = list(secrets.choice(list(resistColorMult.items())))

	# Color pairs list
	colorPairs = e12toColorCodes(eSeriesVal)
	colorPairs.append(mult[0]) # agrego multiplicador
	colorPairs.append(tol[0])

	value = float(eSeriesVal) * (10 ** mult[1])
	valueStrPretty = roundWithMultiplier(value)[0] + tolStrPretty(tol[1])

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
	# TODO: colocar la opcion de tolerancia
	ans = valueStrPretty.split()
	return colorPairs, [[ans[0]], [ans[1], tol[2]]]


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

	bandPosX = 0
	bandStepIncrement = 0
	if len(colorPairs) == 4:
		bandStepIncrement = 35
		bandPosX = 25
	else:
		bandStepIncrement = 30
		bandPosX = 17

	for color in colorPairs:
		rectColorBand = pygame.Rect(x+widthLR+bandPosX, y+centerOffset, 20, heightCenter)
		pygame.draw.rect(screen, resistColorNames[color], rectColorBand)
		bandPosX += bandStepIncrement



def secretShuffle(in_list):
	out_list = []
	while len(in_list) > 0:
		item = secrets.choice(in_list)
		out_list.append(item)
		in_list.remove(item)
	return out_list




class ResistorElement(TestElement):

	def __init__(self, screen):
		self.title = "Resistor"
		self.hint = "formato: resistencia tolerancia (ej: 47K 0.5)"
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
		self.hint = "formato: numero (ej: 4)"
		self.screen = screen
		self.colorCodesPool = []
		self.correctAnswer, self.color = self._getRandomColorCode()

	def new(self):
		self.correctAnswer, self.color = self._getRandomColorCode()

	def flipOrder(self):
		_ = None

	def _getRandomColorCode(self):
		if len(self.colorCodesPool) == 0:
			self.colorCodesPool = secretShuffle(list(resistColorCodes.items()))

		colorPair = list( self.colorCodesPool.pop() )
		return [[colorPair[0]]], colorPair[1]

	# instance method
	def draw(self):
		rect = pygame.Rect(400, 100, 100, 100)
		border = pygame.Rect(rect.left-1, rect.top-1, rect.width+2, rect.height+2)
		pygame.draw.rect(self.screen, 'black', border, border_radius=16)
		pygame.draw.rect(self.screen, resistColorNames[self.color], rect, border_radius=15)


class MultiplierElement(TestElement):

	def __init__(self, screen):
		self.title = "Multiplicador"
		self.hint = "formato: numero con multiplicador (ej: 100M)"
		self.screen = screen
		self.multipliersPool = []
		self.correctAnswer, self.color = self._getRandomMultiplier()

	def new(self):
		self.correctAnswer, self.color = self._getRandomMultiplier()

	def flipOrder(self):
		_ = None

	def _getRandomMultiplier(self):
		if len(self.multipliersPool) == 0:
			self.multipliersPool = secretShuffle(list(resistColorMult.items()))

		multPair = list( self.multipliersPool.pop() )
		power = multPair[1]
		value = 10.0**power
		return [roundWithMultiplier(value)], multPair[0]

	# instance method
	def draw(self):
		rect = pygame.Rect(400, 100, 100, 100)
		border = pygame.Rect(rect.left-1, rect.top-1, rect.width+2, rect.height+2)
		pygame.draw.rect(self.screen, 'black', border, border_radius=16)
		pygame.draw.rect(self.screen, resistColorNames[self.color], rect, border_radius=15)


class ToleranceColorElement(TestElement):

	def __init__(self, screen):
		self.title = "Tolerancia"
		self.hint = "formato: tolerancia numero o letra (ej: 0.25 o C)"
		self.screen = screen
		self.toleranceCodesPool = []
		self.correctAnswer, self.code = self._getRandomColorCode()

	def new(self):
		self.correctAnswer, self.code = self._getRandomColorCode()

	def flipOrder(self):
		_ = None

	def _getRandomColorCode(self):
		if len(self.toleranceCodesPool) == 0:
			self.toleranceCodesPool = secretShuffle(tolColorMult[:])

		tolPair = list( self.toleranceCodesPool.pop() )

		tolCode = str(round(tolPair[1], 3)).rstrip('0').rstrip('.') + '%'
		# TODO: Colocar aca la otra opcion de tolerancia
		return [[tolCode, tolPair[2]]], tolPair[0]

	# instance method
	def draw(self):
		rect = pygame.Rect(400, 100, 100, 100)
		border = pygame.Rect(rect.left-1, rect.top-1, rect.width+2, rect.height+2)
		pygame.draw.rect(self.screen, 'black', border, border_radius=16)
		pygame.draw.rect(self.screen, resistColorNames[self.code], rect, border_radius=15)

class E12SeriesElement(TestElement):

	def __init__(self, screen):
		self.title = "Valor normalizado E12 (10%)"
		self.hint = "formato: 2 numeros o guion (si no es valido) (ej: 47)"
		self.screen = screen
		self.seriesPool = []
		self.correctAnswer, self.colorPair = self._getRandomCode()

	def new(self):
		self.correctAnswer, self.colorPair = self._getRandomCode()

	def flipOrder(self):
		self.colorPair.reverse()

	# Pick a pair of colors which is not a valid E12 value
	def _pickInvalidPairs(self):
		pair = ''
		valid = False
		while not valid:
			pair = ''
			pair += secrets.choice(list(resistColorCodes.keys()))
			pair += secrets.choice(list(resistColorCodes.keys()))
			revPair = list(pair)
			revPair.reverse()
			revPair = ''.join(revPair)
			if (pair in e12series) or (revPair in e12series):
				pass
			else:
				valid = True
		return pair

	def _getRandomCode(self):
		if len(self.seriesPool) == 0:
			self.seriesPool = e12series.copy()
			for _ in range(len(e12series)//2):
				self.seriesPool.append(self._pickInvalidPairs())

			self.seriesPool = secretShuffle(self.seriesPool)

		e12str = self.seriesPool.pop()

		try:
			colorPair = e12toColorCodes(e12str)
		except Exception as ex:
			print("EXCEPCION:", ex)
			print("valores: '{}'".format(e12str))


		inverted = np.random.choice([True, False], p=[0.5, 0.5])
		if inverted:
			colorPair.reverse()

		if not (e12str in e12series):
			return [['-','No es un valor E12','n','no']], colorPair

		return [[e12str]], colorPair

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