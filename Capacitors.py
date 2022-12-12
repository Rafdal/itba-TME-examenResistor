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
    ['1u',105,'A '],
    ['1.5u',155,'E '],
    ['2.2u',225,'J '],
    ['3.3u',335,'N '],
    ['4.7u',475,'S '],
    ['6.8u',685,'W '],
    ['10u',106,'A-'],
    ['15u',156,'E-'],
    ['22u',226,'J-'],
    ['33u',336,'N-'],
    ['47u',476,'S-'],
    ['68u',686,'W-'],
    # ['100u',107,'-'],
]

tantalumSizesSMD = {
    # 'size': (anodeU, X_box, Y_box)
    'P': (2, 2, 1), # P size
    'B': (1, 2, 2), # B,C,D0 sizes
    'A': (1, 2, 1), # A,A2
    'G': (0,0,0),   # Gota
}

tantalumColorsSMD = [
    # ('anode','background','text')
    ('darkorange3','darkgoldenrod1','darkorange3'),
    ('grey50','black','grey70'),
]

tantalumRatedV = [
    # [P-A size, B size]
    ['e','2.5'],
    ['G','4'],
    ['J','6.3'],
    ['A','10'],
    ['C','16'],
    ['D','20'],
    ['E','25'],
    ['V','35'],
]

ceramicTolerances = [
    # ['0.25pF', 'C'],
    ['0.5pF', 'D'],
    # ['0.5%', 'E'],
    ['1%', 'F'],
    ['2%', 'G'],
    ['3%', 'H'],
    ['5%', 'J'],
    ['10%', 'K'],
    ['20%', 'M'],
    ['+100,-0%', 'p'],
    ['+80,-20%', 'Z'],
]

cap_font = pygame.font.Font(None, 38)

def drawTantalum(screen, x, y, size, colors, ratedV, capCode):
    boxUnit = 50
    anodUnit = 22

    # Metal contact padding
    mY = 12
    mX = 5
    mRad = 3

    # ratedV = ['C','16']
    # capCode = ['0.47u',474,'S_']
    # capCode = ['22u',226,'J-']

    cA, cM, cT = colors

    # Draw cap base
    if size == 'G': # gota
        rect = pygame.Rect(x, y, (boxUnit*1.5), boxUnit*2)
        rectMetalB1 = pygame.Rect(x+mY-2, y+boxUnit*2-5, 4, boxUnit)
        rectMetalB2 = pygame.Rect(x-mY+(boxUnit*1.5), y+boxUnit*2-5, 4, boxUnit)

        pygame.draw.rect(screen, 'grey70', rectMetalB1)
        pygame.draw.rect(screen, 'grey70', rectMetalB2)
        pygame.draw.rect(screen, cM, rect, 
            border_top_left_radius=35, 
            border_top_right_radius=35,
            border_bottom_left_radius=10,
            border_bottom_right_radius=10,)
    else:
        aU, xU, yU = tantalumSizesSMD[size]
        rectMark = pygame.Rect(x, y, boxUnit*xU, boxUnit*yU)
        rectAnod = pygame.Rect(x, y, anodUnit*aU, boxUnit*yU)
        rectMetal = pygame.Rect(x-mX, y+mY, boxUnit*xU + mX*2, boxUnit*yU - mY*2)
        rectMetalB = pygame.Rect(x-mX-1, y+mY-1, boxUnit*xU + mX*2 + 2, boxUnit*yU - mY*2 + 2)
        pygame.draw.rect(screen, 'grey70', rectMetalB, border_radius=mRad+1)
        pygame.draw.rect(screen, 'lightcyan', rectMetal, border_radius=mRad)
        pygame.draw.rect(screen, cM, rectMark)
        pygame.draw.rect(screen, cA, rectAnod)

    # Draw cap marking
    if size == 'P':
        hint = ratedV[0] + capCode[2][0]
        cap_title = cap_font.render(hint, True, cT)
        screen.blit(cap_title, (x + anodUnit*aU + 5, y + 15))
        if capCode[2][1] == '-':
            xLine = x + anodUnit*aU + cap_title.get_width()//2 + 5
            yLine = y + 12
            pygame.draw.line(screen, cT, (xLine, yLine), (xLine+(cap_title.get_width()//2), yLine))
        elif capCode[2][1] == '_':
            xLine = x + anodUnit*aU + cap_title.get_width()//2 + 5
            yLine = y + 15 + cap_title.get_height()
            pygame.draw.line(screen, cT, (xLine, yLine), (xLine+(cap_title.get_width()//2), yLine))

    elif size == 'A':
        hint = ratedV[0] + str(capCode[1])
        cap_title = cap_font.render(hint, True, cT)
        screen.blit(cap_title, (x + anodUnit*aU + 5, y + 15))

    elif size == 'B':
        ratCap_title = cap_font.render(capCode[0].rstrip('u'), True, cT)
        screen.blit(ratCap_title, (x + anodUnit*aU + 20, y + 15))
        ratVolt_title = cap_font.render(ratedV[1]+'V', True, cT)
        screen.blit(ratVolt_title, (x + anodUnit*aU + 10, y + 15 + boxUnit))

    elif size == 'G':
        ratCap_title = cap_font.render(capCode[0].rstrip('u'), True, cT)
        screen.blit(ratCap_title, (x + 15, y + 25))
        ratVolt_title = cap_font.render(ratedV[1]+'  +', True, cT)
        screen.blit(ratVolt_title, (x + 10, y + 5 + boxUnit))



class CapacitorMarking(TestElement):
        def __init__(self, screen):
            self.title = "Nomenclatura Capacitor"
            self.hint = "formato: capacitancia tolerancia (ej: 0.22u 2%)"
            self.screen = screen
            self.correctAnswer = [['null','NULL']]
            self.new()

        def new(self):
            self.tol = secrets.choice(ceramicTolerances)
            e12 = secrets.choice(e12series)
            power = secrets.choice([4,5,6,7])



class TantalumElement(TestElement):

    def __init__(self, screen):
        self.title = "Capacitor"
        self.hint = "formato: tipo capacitancia voltaje (ej: tant 0.22u 16V)"
        self.screen = screen
        self.correctAnswer = [['null','NULL']]
        self.new()

    def _genTalantum(self):
        sizeProb = [0.15, 0.35, 0.15, 0.35]
        self.size = str(np.random.choice(list(tantalumSizesSMD.keys()), p=sizeProb))
        self.colors = secrets.choice(tantalumColorsSMD)
        self.ratedCap = secrets.choice(tantalumCodes)
        self.ratedVolt = secrets.choice(tantalumRatedV)
        self.type = "tantalo"
        self.correctAnswer = [
            ['tantalo',None,'t','ta','tan','tant','tantalum'],
            [self.ratedCap[0]+'F',None,self.ratedCap[0]],
            [self.ratedVolt[1]+'V', None, self.ratedVolt[1]]
        ]

    def new(self):
        self._genTalantum()

    def flipOrder(self):
        pass

    # instance method
    def draw(self):
        drawTantalum(self.screen, 200, 60, self.size, self.colors, self.ratedVolt, self.ratedCap)