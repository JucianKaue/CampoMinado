from random import randint
import pygame
from time import sleep

# Definição de tela
screen = pygame.display.set_mode((450, 500))

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

# Definir Texto
pygame.font.init()
font = pygame.font.SysFont("impact", 35)
text_title = font.render("Campo Minado", True, p_green)

# Definir Imagens
fundo = pygame.image.load("Imagens/fundo/floresta_desfocada.jpg")
default = pygame.image.load("Imagens/tabuleiro/default.png")
mine = pygame.image.load("Imagens/tabuleiro/mine.png")
img_bandeira = pygame.image.load("Imagens/fundo/bandeira-1.png")
empty = []
for i in range(0, 9):
    empty.append(pygame.image.load(f"Imagens/tabuleiro/empty{i}.png"))


# Funções
def CriarBomba(tam):
    quant_bomb = int((tam*tam)*0.25)
    bomb = []
    count = 0
    while count < quant_bomb:
        casa = (randint(0, tam-1), randint(0, tam-1))
        if casa not in bomb:
            bomb.append(casa)
            count += 1
    return bomb


def Abrir_casa(pos, list_bomb, tam_casa, tam_tab):
    redor = ((pos[0]-1, pos[1]-1),
             (pos[0]-1, pos[1]),
             (pos[0]-1, pos[1]+1),
             (pos[0],   pos[1]-1),
             (pos[0],   pos[1]),
             (pos[0],   pos[1]+1),
             (pos[0]+1, pos[1]-1),
             (pos[0]+1, pos[1]),
             (pos[0]+1, pos[1]+1))

    quant_bomba = 0             # Essa variavel não muda
    for bomb in list_bomb:
        for casa in redor:
            if casa == bomb:
                quant_bomba += 1

    posicao_casa = ((pos[0] * tam_casa) + 25), int((pos[1] * tam_casa) + 50)
    if pos in list_bomb:
        screen.blit(bomb_img, posicao_casa)
    else:
        """print(quant_bomba)
        if quant_bomba == 0:
            for c in redor: #Não Saí do primeiro item
                if not c < (0, 0) or c > (tam_tab, tam_tab):
                    print("I'm here")
                    print(c)
                    print(list_bomb)
                    print(tam_casa)
                    Abrir_casa(c, list_bomb, tam_casa, tam_tab)"""
        screen.blit(empty[quant_bomba], posicao_casa)


def Game(tam):
    sleep(1/60)
    # Inciar pygame
    global padrao
    global bomb_img
    pygame.init()

    # Apgar a tela anterior
    screen.blit(fundo, (0, 0))

    # mostrar texto
    screen.blit(text_title, (120, 2))

    # Definir tamanho de cada casa da tabela
    tam_casa = int(400 / tam)
    for c in range(0, 9):
        empty[c] = pygame.transform.scale(empty[c], (tam_casa, tam_casa))
        padrao = pygame.transform.scale(default, (tam_casa, tam_casa))
        bomb_img = pygame.transform.scale(mine, (tam_casa, tam_casa))

    # Mostrar local de numero de bombas definidas
    screen.blit(img_bandeira, (280, 453))

    # Criar tabela
    pos_casa = (25, 50)
    for i in range(0, tam):
        for c in range(0, tam):
            # cria uma linha
            screen.blit(padrao, pos_casa)
            pos_casa = (pos_casa[0] + tam_casa, pos_casa[1])
        # desce uma coluna
        pos_casa = (25, pos_casa[1] + tam_casa)
    pygame.display.update()

    # Criar Bombas
    casas_bombas = CriarBomba(tam)

    # Loop do jogo
    sair = True
    while sair:
        # Travar FPS
        sleep(1/60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = False

        # Clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Posição do mouse
                pos_mouse = pygame.mouse.get_pos()
                pos_mouse = int((pos_mouse[0] - 25) / tam_casa), int((pos_mouse[1] - 50) / tam_casa)

                Abrir_casa(pos_mouse, casas_bombas, tam_casa, tam)
                pygame.display.update()




    pygame.display.update()
    sleep(1)
