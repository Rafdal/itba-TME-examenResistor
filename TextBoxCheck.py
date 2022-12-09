import pygame
import sys


# Text box for input data
class TextBoxCheck:
    # create rectangle
    _input_rect = pygame.Rect(300, 500, 350, 40)
    user_text = ''
    sendFlag = False	# Indicar si intento acertar (falso por defecto)

    # color_active = 
    # color_passive = pygame.Color('chartreuse4')
    _color = pygame.Color('lightskyblue3') # default

    # instance attributes
    def __init__(self, screen, font, onSend, onReset):
        self.screen = screen
        self.font = font
        self.onSend = onSend
        self.onReset = onReset

    # instance method
    def run(self):
        for event in pygame.event.get():

            # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    self.user_text = self.user_text[:-1]

                else:
                    c = event.unicode	# OJO: Unicode es un string (mas de un byte)
                    if(c.isalnum() or (c in " \t%.-")):
                        self.user_text += event.unicode

                    elif (c == '\n' or c == '\r'):
                        
                        if not self.sendFlag:
                            
                            self.onSend(self.user_text.split())
                            self.sendFlag = True
                        else:
                            self.user_text = ""
                            self.sendFlag = False
                            self.onReset()
                        

    def draw(self):
        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(self.screen, self._color, self._input_rect)

        text_surface = self.font.render(self.user_text, True, (0, 0, 0))
        text_hint = self.font.render("Su respuesta:", True, (0, 0, 0))

        # render at position stated in arguments
        self.screen.blit(text_surface, (self._input_rect.x+5, self._input_rect.y+5))

        self.screen.blit(text_hint, (self._input_rect.x-text_hint.get_width()-10, self._input_rect.y+5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        self._input_rect.w = max(150, text_surface.get_width()+10)
