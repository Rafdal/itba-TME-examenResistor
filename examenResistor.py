"""
Autor: Rafael Dalzotto
Fecha: 7 Dic 2022
"""

import pygame
import sys
import secrets	# cryptographic secure random engine
import numpy as np

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


# pygame.init() will initialize all
# imported module
pygame.init()

clock = pygame.time.Clock()

# it will display on screen
screen = pygame.display.set_mode([800, 600])

# basic font for user typed
base_font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 58)
user_text = ''

# create rectangle
input_rect = pygame.Rect(300, 500, 350, 40)

color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive # default

objects = []

active = False

def drawResist(x, y, colorPairs=[[]]):
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
		rectColorBand = pygame.Rect(x+widthLR+bandStepX, y+centerOffset, 15, heightCenter)
		pygame.draw.rect(screen, resistColorNames[color], rectColorBand)
		bandStepX += 30

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



class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': 'lightblue',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = base_font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()
        
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)




# INIT VARIABLES

colorCodes, valueStr = getRandomResistValue()

drawNewResist = True

intentoAcertar = False	# Indicar si intento acertar (falso por defecto)

popupAnswer = ""

def flipResistor():
	colorCodes.reverse()	

def newResistor():
	global drawNewResist
	drawNewResist = True

Button(20, 50, 100, 50, 'Girar', flipResistor)
Button(20, 110, 100, 50, 'Nuevo', newResistor)

# 	MAIN LOOP

while True:

	for event in pygame.event.get():

		# if user types QUIT then the screen will close
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if input_rect.collidepoint(event.pos):
				active = True
			else:
				active = False

		if event.type == pygame.KEYDOWN:
			# Check for backspace
			if event.key == pygame.K_BACKSPACE:

				# get text input from 0 to -1 i.e. end.
				user_text = user_text[:-1]

			else:
				c = event.unicode	# OJO: Unicode es un string (mas de un byte)
				if(c.isalnum() or c == ' ' or c == '\t' or c == '%' or c == '.'):
					user_text += event.unicode

				elif (c == '\n' or c == '\r'):
					
					if not intentoAcertar:
						if(user_text.replace(' ', '') == valueStr.replace(' ','')):
							popupAnswer = "CORRECTO!"
						else:
							popupAnswer = "INCORRECTO!"
						intentoAcertar = True
					else:
						user_text = ""
						drawNewResist = True
						intentoAcertar = False


	# it will set background color of screen
	screen.fill((255, 255, 255))

	if active:
		color = color_active
	else:
		color = color_passive

	# draw rectangle and argument passed which should
	# be on screen
	pygame.draw.rect(screen, color, input_rect)

	text_surface = base_font.render(user_text, True, (0, 0, 0))
	text_hint = base_font.render("Su respuesta:", True, (0, 0, 0))

	if intentoAcertar:
		text_popup = big_font.render(popupAnswer, True, (0,0,0))
		text_reveal = big_font.render(valueStr, True, (0,0,0))

		screen.blit(text_reveal, (200, 200))
		screen.blit(text_popup, (200, 200 + text_reveal.get_height() + 100))

	# render at position stated in arguments
	screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))

	screen.blit(text_hint, (input_rect.x-text_hint.get_width()-10, input_rect.y+5))

	# Debe estar antes de dibujar nuevo resistor
	for obj in objects:
		obj.process()


	if(drawNewResist):
		# dibujar el resist
		colorCodes, valueStr = getRandomResistValue()
		drawNewResist = False

	drawResist(200, 60, colorCodes)

	# set width of textfield so that text cannot get
	# outside of user's text input
	input_rect.w = max(150, text_surface.get_width()+10)


	# update screen
	pygame.display.flip()

	# 60 frames should be passed.
	clock.tick(60)
