from random import randint
import pygame
from time import sleep

# Definição de tela
screen = pygame.display.set_mode((450, 510))

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
tab_bandeira = pygame.image.load("Imagens/tabuleiro/bandeira.png")
voltar_icone = pygame.image.load("Imagens/fundo/icone-voltar.png ")
empty = []
for i in range(0, 9):
    empty.append(pygame.image.load(f"Imagens/tabuleiro/empty{i}.png"))

# Mostrar local de numero de bombas
screen.blit(img_bandeira, (280, 453))

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


def Abrir_casa(pos, list_bomb, tam_casa, tamanho_tabuleiro):

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
    global padrao, bandeira_casa, bomb_img
    pygame.init()

    # Apagar a tela anterior
    screen.blit(fundo, (0, 0))

    # mostrar texto
    screen.blit(text_title, (120, 2))

    # Definir tamanho de cada casa da tabela
    tam_casa = int(400 / tam)
    for c in range(0, 9):
        empty[c] = pygame.transform.scale(empty[c], (tam_casa, tam_casa))
        padrao = pygame.transform.scale(default, (tam_casa, tam_casa))
        bomb_img = pygame.transform.scale(mine, (tam_casa, tam_casa))
        bandeira_casa = pygame.transform.scale(tab_bandeira, (tam_casa, tam_casa))

    # Mostrar local de numero de bombas definidas
    screen.blit(img_bandeira, (280, 453))

    screen.blit(voltar_icone, (50, 453))

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

    # Variáveis
    casas_bombas = CriarBomba(tam)  # Criar Bombas
    bombas_definidas = []           # Casas das bombas marcadas pelo jogador
    casas_abertas = []              # Guarda as casas que já foram abertas

    # Loop do jogo
    sair = True
    while sair:
        # Travar FPS
        sleep(1/60)

        for event in pygame.event.get():
        # Clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Posição do mouse
                pos_mouse = pygame.mouse.get_pos()
                casa_mouse = int((pos_mouse[0] - 25) / tam_casa), int((pos_mouse[1] - 50) / tam_casa)

                if casa_mouse not in casas_abertas:
                    posicao_casa = ((casa_mouse[0] * tam_casa) + 25), int((casa_mouse[1] * tam_casa) + 50)

                    # Botão Esquerdo
                    if pygame.mouse.get_pressed()[0] == 1:
                        if casa_mouse not in bombas_definidas:
                            Abrir_casa(casa_mouse, casas_bombas, tam_casa, tam)
                            casas_abertas.append(casa_mouse)

                        if (90, 495) > pos_mouse > (50, 453):
                            break

                    # Botão Direito
                    elif pygame.mouse.get_pressed()[2] == 1:
                        if casa_mouse in bombas_definidas:
                            bombas_definidas.pop(bombas_definidas.index(casa_mouse))
                            screen.blit(padrao, posicao_casa)
                        else:
                            bombas_definidas.append(casa_mouse)
                            screen.blit(bandeira_casa, posicao_casa)

                        font = pygame.font.SysFont('impact', 30)
                        screen.blit(img_bandeira, (280, 453))
                        txt_num_bombas_abertas = font.render(f"{len(bombas_definidas)}", True, black)
                        screen.blit(txt_num_bombas_abertas, (335, 457))

                pygame.display.update()

    pygame.display.update()
    sleep(1)
