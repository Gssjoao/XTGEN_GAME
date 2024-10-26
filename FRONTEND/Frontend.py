import pygame
import sys

#inicializar o PYGAME
pygame.init()

#criando uma tela 
largura = 600
altura = 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("XTEGEN")

#cor de fundo do display
BACKGROUD_COLOR = (0, 0, 0)

#loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.quit:
            pygame.quit()
            sys.exit()

 #preenche a fundo de tela   atualiza  a tela
 
        tela.fill(BACKGROUD_COLOR)
 
        pygame.display.update() 

