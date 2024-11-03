import pygame
import sys
import os
import random
import pygame.locals
from pygame.sprite import Group


class dragon(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


        self.images = [pygame.image.load('IMGs/Dragão2.png').convert_alpha(),
                      pygame.image.load('IMGs/Dragão1.png').convert_alpha(),
                      pygame.image.load('IMGs/Dragão3.png').convert_alpha()]

        self.current_image = 0
        self.image = pygame.image.load('IMGs/Dragão2.png').convert_alpha()          
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 4
        self.rect[1] = SCREEN_HEIGTH / 4
        print(self.rect)

    def update(self):
        self.current_image = (self.current_image + 1) % 4
        self.image = self.images[ self.current_image ]
        pass
#inicializar o PYGAME
pygame.init()

#criando uma tela 
SCREEN_WIDTH = 800
SCREEN_HEIGTH = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption("XTEGEN")
dragon_group = pygame.sprite.Group()
dragon = dragon()
dragon_group.add(dragon)
#cor de fundo do display
BACKGROUD_DISPLAY = pygame.transform.scale2x(pygame.image.load(os.path.join('IMGs', 'fundo_XTGEN_GAME.gif')))

#loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.quit:
            pygame.quit()
            sys.exit()
 #preenche a fundo de tela   atualiza  a tela
        screen.blit(BACKGROUD_DISPLAY, (0, 0))
        dragon_group.update()
        dragon_group.draw(screen)
        pygame.display.update() 
        