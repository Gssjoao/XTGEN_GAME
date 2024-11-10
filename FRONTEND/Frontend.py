import pygame
import sys
import os
import random
from pygame.locals import *
from pygame.sprite import Group, Group


class dragon(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        largura, altura = 150, 150

        self.images = [pygame.transform.scale(pygame.image.load('IMGs/Dragão2.png').convert_alpha(),  (largura, altura)),
                      pygame.transform.scale(pygame.image.load('IMGs/Dragão1.png').convert_alpha(),  (largura, altura)),
                      pygame.transform.scale(pygame.image.load('IMGs/Dragão3.png').convert_alpha(),  (largura, altura))]
        
        self.speed = SPEED
        self.current_image = 0
        self.image = pygame.image.load('IMGs/Dragão2.png').convert_alpha()          
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 4
        self.rect[1] = SCREEN_HEIGHT / 4

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]
     
        
        self.speed += GRAVITY
         # Update height
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED


class Ground(pygame.sprite.Sprite):

     def __init__(self, width, height, xpos):
         pygame.sprite.Sprite.__init__(self)
         self.image = pygame.image.load('IMGs/Base_Display.png').convert_alpha()
         self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

         self.rect = self.image.get_rect()
         self.rect[0] = xpos
         self.rect[1] =  SCREEN_HEIGHT - GROUND_HEIGHT

     def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] <  -(sprite.rect[2])

#inicializar o PYGAME
pygame.init()

#criando uma tela 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("XTEGEN")

dragon_group = pygame.sprite.Group()
dragon = dragon()
dragon_group.add(dragon)

ground_group = pygame.sprite.Group()
for i in range(2):
   ground = Ground(GROUND_WIDTH, GROUND_HEIGHT, 0)
   ground_group.add(ground)

#cor de fundo do display
BACKGROUD_DISPLAY = pygame.transform.scale2x(pygame.image.load(os.path.join('IMGs', 'Fundo_Display.jpg')))

clock = pygame.time.Clock()

#loop principal
while True:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                dragon.bump()

   
    

 #preenche a fundo de tela   atualiza  a tela
    screen.blit(BACKGROUD_DISPLAY, (0, 0))
	
    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])


        new_ground = Ground(GROUND_WIDTH, GROUND_HEIGHT, SCREEN_WIDTH - 20)
        ground_group.add(new_ground)
    
    dragon_group.update()
    ground_group.update()
    dragon_group.draw(screen)
    ground_group.draw(screen)
    pygame.display.update() 
        