import pygame
from Game import Game
from time import sleep

# Definir cores
black = (0, 0, 0)
gray = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
p_blue = (21, 180, 237)
p_light_blue = (22, 247, 247)
p_blue_green = (32, 224, 168)
p_green_azul = (22, 247, 120)
p_green = (21, 237, 54)

# Imagens
fundo_floresta = pygame.image.load("Imagens/fundo/floresta_desfocada.jpg")
icon = pygame.image.load("Imagens/bomb.png")

soldier1 = pygame.image.load("Imagens/soldiers/sol1.png")
soldier2 = pygame.image.load("Imagens/soldiers/sol2.png")
soldier3 = pygame.image.load("Imagens/soldiers/sol3.png")
soldier4 = pygame.image.load("Imagens/soldiers/sol4.png")
soldier1_click = pygame.image.load("Imagens/soldiers/sol1_click.png")
soldier2_click = pygame.image.load("Imagens/soldiers/sol2_click.png")
soldier3_click = pygame.image.load("Imagens/soldiers/sol3_click.png")
soldier4_click = pygame.image.load("Imagens/soldiers/sol4_click.png")

# Frases
pygame.font.init()
font = pygame.font.SysFont("impact", 35)
text_title_menu1 = font.render("Campo Minado", True, (p_green))
text_title_menu2 = font.render("Escolha um nível", True, (black))

# Iniciar Pygame
try:
    pygame.init()
except:
    print('ERRO! Pygame não foi iniciado')

# Definição de tela e icone
pygame.display.set_icon(icon)
pygame.display.set_caption('Campo Minado')
screen = pygame.display.set_mode((450, 500))

# Definição de váriáveis
run = True

# Programa principal
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(fundo_floresta, (0, 0))
    screen.blits([(text_title_menu1, (120, 2)),
                  (soldier1, (45, 50)),
                  (soldier2, (237, 50)),
                  (soldier3, (45, 250)),
                  (soldier4, (237, 250)),
                  (text_title_menu2, (110, 450))])

    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if 45 <= pos[0] <= 213 and 50 <= pos[1] <= 243:
            screen.blit(soldier1_click, (45, 50))
            Game(8)
        if 237 <= pos[0] <= 405 and 50 <= pos[1] <= 243:
            screen.blit(soldier2_click, (237, 50))
            Game(12)
        if 45 <= pos[0] <= 213 and 250 <= pos[1] <= 443:
            screen.blit(soldier3_click, (45, 250))
            Game(16)
        if 237 <= pos[0] <= 405 and 250 <= pos[1] <= 443:
            screen.blit(soldier4_click, (237, 250))
            Game(20)

    pygame.display.update()
