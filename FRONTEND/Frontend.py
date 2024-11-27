import pygame
import sys
import os
from pygame.locals import *
from pygame.sprite import Group, Sprite
import random

# Função para carregar as imagens de forma segura
def carregar_imagem(caminho):
    if os.path.exists(caminho):
        return pygame.image.load(caminho).convert_alpha()
    else:
        print(f"Imagem não encontrada: {caminho}")
        return pygame.Surface((100, 100))  

# Classes principais

class Dragon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        largura, altura = 80, 80
        self.images = [pygame.transform.scale(carregar_imagem('IMGs/Dragão2.png'), (largura, altura)),
                       pygame.transform.scale(carregar_imagem('IMGs/Dragão1.png'), (largura, altura)),
                       pygame.transform.scale(carregar_imagem('IMGs/Dragão3.png'), (largura, altura))]

        self.speed = SPEED
        self.current_image = 0
        self.image = self.images[self.current_image]          
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH / 4
        self.rect.y = SCREEN_HEIGHT / 4  

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        
        self.speed += GRAVITY
        self.rect.y += self.speed

    def bump(self):
        self.speed = -SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, width, height, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = carregar_imagem('IMGs/image.png')
        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = SCREEN_HEIGHT - height

    def update(self):
        self.rect.x -= GAME_SPEED
        if self.rect.x <= -GROUND_WIDTH:
            self.rect.x = GROUND_WIDTH * (len(ground_group) - 1)

class Ceiling(pygame.sprite.Sprite):  
    def __init__(self, width, height, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = carregar_imagem('IMGs/image.png')  
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image = pygame.transform.flip(self.image, False, True)  

        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = 0  
    def update(self):
        self.rect.x -= GAME_SPEED
        if self.rect.x <= -GROUND_WIDTH:
            self.rect.x = GROUND_WIDTH * (len(ceiling_group) - 1)

class Pipe(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        self.width = 80
        self.gap = 150  

        # Limites para a altura dos pipes
        min_top_height = 170  
        max_top_height = SCREEN_HEIGHT // 2    
        
        # Garantir que a altura máxima do topo não seja muito pequena
        if max_top_height < min_top_height:
            max_top_height = min_top_height
        
        # Gerar a altura aleatória para o topo do pipe
        self.top_height = random.randint(min_top_height, max_top_height)  
        self.bottom_height = SCREEN_HEIGHT - self.top_height - self.gap  

        # Carregar a imagem e ajustar o tamanho
        self.top_image = pygame.transform.scale(carregar_imagem('IMGs/Pedra.png'), (self.width, self.top_height))
        self.bottom_image = pygame.transform.scale(carregar_imagem('IMGs/Pedra.png'), (self.width, self.bottom_height))

        # Flipando a imagem do topo para que fique invertida verticalmente
        self.top_image = pygame.transform.flip(self.top_image, False, True)  

        self.top_rect = self.top_image.get_rect()
        self.bottom_rect = self.bottom_image.get_rect()

        # Gerar a posição aleatória para o topo e para a parte inferior do cano
        self.top_rect.x = SCREEN_WIDTH
        self.bottom_rect.x = SCREEN_WIDTH
        
        # O topo será posicionado aleatoriamente entre 0 e a altura máxima permitida
        self.top_rect.y = random.randint(0, max_top_height - self.top_height)

        # A parte inferior é posicionada logo abaixo do "gap", mas aleatoriamente, em cima ou embaixo
        if random.choice([True, False]):  
            self.bottom_rect.y = self.top_rect.y + self.top_height + self.gap
        else:
            self.bottom_rect.y = self.top_rect.y - self.bottom_height - self.gap

        # Associando a imagem principal do Pipe
        self.image = self.top_image  
        self.rect = pygame.Rect(self.top_rect.x, self.top_rect.y, self.width, self.top_height + self.gap + self.bottom_height)

    def update(self):
        # Movimento para a esquerda
        self.rect.x -= GAME_SPEED
        if self.rect.x <= -GROUND_WIDTH:
            self.rect.x = GROUND_WIDTH * (len(pipe_group) - 1)

        # Se o cano sai da tela, ele será removido
        if self.top_rect.x < -self.width:
            self.kill()
        if self.bottom_rect.x < -self.width:
            self.kill()

    def draw(self, screen):
        # Desenha os dois canos: o topo e a parte inferior
        screen.blit(self.top_image, self.top_rect)
        screen.blit(self.bottom_image, self.bottom_rect)

# Função para verificar se um sprite saiu da tela
def is_off_screen(sprite):
    return sprite.rect.x < -(sprite.rect.width)

# Função para mostrar a tela de Game Over
def game_over():
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over!", True, (255, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2.7, SCREEN_HEIGHT // 2 - 60))

# Função para reiniciar o jogo
def reset_game():
    global dragon, dragon_group, ground_group, ceiling_group, pipe_group, last_pipe, score
    dragon = Dragon()
    dragon_group = pygame.sprite.Group()
    dragon_group.add(dragon)

    ground_group = pygame.sprite.Group()
    ground_group.add(Ground(GROUND_WIDTH, GROUND_HEIGHT, 0))
    ground_group.add(Ground(GROUND_WIDTH, GROUND_HEIGHT, GROUND_WIDTH))

    ceiling_group = pygame.sprite.Group()  
    ceiling_group.add(Ceiling(GROUND_WIDTH, GROUND_HEIGHT, 0))  
    ceiling_group.add(Ceiling(GROUND_WIDTH, GROUND_HEIGHT, GROUND_WIDTH))  

    pipe_group = pygame.sprite.Group()  # Reseta o grupo de pipes
    last_pipe = pygame.time.get_ticks()  # Reseta o temporizador de pipes para o tempo atual
    score = 0  # Resetando o placar de pedras passadas

# Função para desenhar a tela inicial
def draw_start_screen():
    background_image = pygame.image.load('IMGs/Fundo_Display.jpg')
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background_image, (0, 0))

    font = pygame.font.Font(None, 70)
    text = font.render("Clique para Iniciar o Jogo", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

# Função para desenhar o botão de reinício
def draw_restart_button():
    font = pygame.font.Font(None, 40)
    button_width, button_height = 300, 60
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    button_y = SCREEN_HEIGHT // 2 + 20
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 200, 0), button_rect)
    else:
        pygame.draw.rect(screen, (0, 255, 0), button_rect)

    text = font.render("Restart Game", True, (0, 0, 0))
    screen.blit(text, (button_x + button_width // 5, button_y + button_height // 3.5))

    return button_rect

def check_restart_button_click(button_rect):
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            return True
    return False

# Função para desenhar o placar
def draw_score(score):
    font = pygame.font.Font(None, 40)
    text = font.render(f"Pedras Passadas: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

# Inicializando o Pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
SPEED = 10
GRAVITY = 1
GAME_SPEED = 5  
GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("XTEGEN")

dragon_group = pygame.sprite.Group()
dragon = Dragon()
dragon_group.add(dragon)

ground_group = pygame.sprite.Group()
ground_group.add(Ground(GROUND_WIDTH, GROUND_HEIGHT, 0))
ground_group.add(Ground(GROUND_WIDTH, GROUND_HEIGHT, GROUND_WIDTH))

ceiling_group = pygame.sprite.Group()
ceiling_group.add(Ceiling(GROUND_WIDTH, GROUND_HEIGHT, 0))
ceiling_group.add(Ceiling(GROUND_WIDTH, GROUND_HEIGHT, GROUND_WIDTH))

pipe_group = pygame.sprite.Group()

BACKGROUND_DISPLAY = pygame.transform.scale2x(pygame.image.load(os.path.join('IMGs', 'Fundo_Display.jpg')))

clock = pygame.time.Clock()

game_running = False
in_game = False
last_pipe = 0  
PIPE_INTERVAL = 1500  
score = 0

while True:
    clock.tick(25)  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE and game_running:
                dragon.bump()

        if event.type == MOUSEBUTTONDOWN:  
            if not in_game:
                in_game = True
                game_running = True
                reset_game()

    if not in_game:
        screen.fill((0, 0, 0))
        draw_start_screen()
    else:
        if dragon.rect.y > SCREEN_HEIGHT or dragon.rect.y < 0:
            game_running = False

        screen.blit(BACKGROUND_DISPLAY, (0, 0))

        ground_group.update()
        ceiling_group.update()  
        pipe_group.update()

        if game_running:
            dragon_group.update()
            pipe_group.update()

            # Verifica colisões entre o dragão e os obstáculos
            if pygame.sprite.spritecollideany(dragon, pipe_group, pygame.sprite.collide_mask):
                game_running = False  
            if pygame.sprite.spritecollideany(dragon, ceiling_group, pygame.sprite.collide_mask):
                game_running = False 
            if pygame.sprite.spritecollideany(dragon, ground_group):
                game_running = False  

            # Incrementa o placar quando o dragão passa por um pipe
            for pipe in pipe_group:
                if pipe.rect.x + pipe.width < dragon.rect.x and not hasattr(pipe, "scored"):
                    score += 1
                    pipe.scored = True  

            dragon_group.draw(screen)
            ground_group.draw(screen)
            ceiling_group.draw(screen)  
            pipe_group.draw(screen)

            draw_score(score)  

        else:
            game_over()
            restart_button_rect = draw_restart_button()

            if check_restart_button_click(restart_button_rect):
                reset_game()
                game_running = True

    # Cria novos pipes a intervalos regulares
        if game_running and pygame.time.get_ticks() - last_pipe > random.randint(1900, 4000):  
            last_pipe = pygame.time.get_ticks() 
            pipe_group.add(Pipe())  

    pygame.display.update()
