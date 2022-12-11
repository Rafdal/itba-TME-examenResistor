import secrets	# cryptographic secure random engine
import numpy as np
import pygame
from TestElement import *
from utils import *

#   ["ratedCapSymbol", "ratedCap_uF", 'pSize_ratedCap']
tantalumCodes = [
    ['0.1u',104,'A_'],
    ['0.15u',154,'E_'],
    ['0.22u',224,'J_'],
    ['0.33u',334,'N_'],
    ['0.47u',474,'S_'],
    ['0.68u',684,'W_'],
    ['1u',105,'A'],
    ['1.5u',155,'E'],
    ['2.2u',225,'J'],
    ['3.3u',335,'N'],
    ['4.7u',475,'S'],
    ['6.8u',685,'W'],
    ['10u',106,'A-'],
    ['15u',156,'E-'],
    ['22u',226,'J-'],
    ['33u',336,'N-'],
    ['47u',476,'S-'],
    ['68u',686,'W-'],
    ['100u',107,'-'],
]

tantalumRatedV = [
    ['e','2.5'],
    ['G','4'],
    ['J','6.3'],
    ['A','10'],
    ['C','16'],
    ['D','20'],
    ['E','25'],
    ['V','35'],
]

def drawTantalum(screen, x, y):
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


class TantalumElement(TestElement):

	def __init__(self, screen):
		self.title = "Resistor"
		self.screen = screen
		self.colorCodes, self.correctAnswer = '', [['']]

	def new(self):
		self.colorCodes, self.correctAnswer = '', [['']]

	def flipOrder(self):
		pass

	# instance method
	def draw(self):
		drawTantalum(self.screen, 200, 60)