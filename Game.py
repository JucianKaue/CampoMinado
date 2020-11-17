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
voltar_icone_clicked = pygame.image.load("Imagens/fundo/icone-voltar-clicked.png")
empty = []
for i in range(0, 9):
    empty.append(pygame.image.load(f"Imagens/tabuleiro/empty{i}.png"))

# Mostrar local de numero de bombas
screen.blit(img_bandeira, (280, 453))


# Funções
def criarBomba(tam):
    quant_bomb = int((tam*tam)*0.20)
    bomb = []
    count = 0
    while count < quant_bomb:
        casa = (randint(0, tam-1), randint(0, tam-1))
        if casa not in bomb:
            bomb.append(casa)
            count += 1
    print(bomb)
    return bomb


def abrir_casa(pos, list_bomb, tam_casa):
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
            pygame.display.update()
            sleep(0.3)
            perder()
            return True
        else:
            screen.blit(empty[quant_bomba], posicao_casa)
        return False


def ganhar(casas_abertas, tamanho_tabuleiro, casas_marcadas, casas_bombas):
    bombas_marcadas_certas = 0
    print(f'casas abertas: {len(casas_abertas)}')
    print(f'casas bombas: {len(casas_bombas)}')
    print(f'tam-casas: {tamanho_tabuleiro*tamanho_tabuleiro}')
    print(len(casas_abertas) == (tamanho_tabuleiro*tamanho_tabuleiro)-len(casas_bombas))
    if len(casas_abertas) == (tamanho_tabuleiro*tamanho_tabuleiro)-len(casas_bombas):
        print('im here')
        for casa in casas_marcadas:
            print(casa)
            if casas_bombas.count(casa) == 1:
                bombas_marcadas_certas += 1
                print(f'Bombas Marcadas: {bombas_marcadas_certas}')

    if bombas_marcadas_certas == int((tamanho_tabuleiro*tamanho_tabuleiro)*0.20):
        return True


def perder():
    img_lost = pygame.image.load("Imagens/lost-rd.jpg")
    screen.blit(fundo, (0, 0))
    screen.blit(img_lost, (25, 110))
    pygame.display.update()
    sleep(2)


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

    # Mostrar botão de voltar
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
    casas_bombas = criarBomba(tam)  # Criar Bombas
    bombas_definidas = []           # Casas das bombas marcadas pelo jogador
    casas_abertas = []              # Guarda as casas que já foram abertas
    find_bomb = False

    # Loop do jogo
    sair = True
    while sair:
        sleep(1/60)     # Travar FPS
        for event in pygame.event.get():
            # Clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:                                                        # Se clicar com o mouse
                pos_mouse = pygame.mouse.get_pos()                                                          # Pega a posição do mause em pixels
                casa_mouse = int((pos_mouse[0] - 25) / tam_casa), int((pos_mouse[1] - 50) / tam_casa)       # Converte a posição do mause para a posição das casas

                if casa_mouse not in casas_abertas:                                                         # Confere se as casas já foram abertas ou não
                    posicao_casa = ((casa_mouse[0] * tam_casa) + 25), int((casa_mouse[1] * tam_casa) + 50)  # Converte a casa que o mause está de volta para pixels
                    # Se o botão esquerdo do mause for clicado
                    if pygame.mouse.get_pressed()[0] == 1:
                        if casa_mouse[0] < tam and casa_mouse[1] < tam:   # Confere a posição que houve o clique do mouse foi dentro do tabuleiro
                            if casa_mouse not in bombas_definidas:
                                find_bomb = abrir_casa(casa_mouse, casas_bombas, tam_casa)
                                casas_abertas.append(casa_mouse)

                        if 90 > pos_mouse[0] > 50 and 453 < pos_mouse[1] < 495:
                            screen.blit(voltar_icone_clicked, (50, 453))
                            pygame.display.update()
                            sair = False
                            sleep(0.2)

                    # Botão Direito
                    elif pygame.mouse.get_pressed()[2] == 1:
                        if casa_mouse[0] < tam and casa_mouse[1] < tam:
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
        if find_bomb:
            break
        if ganhar(casas_abertas, tam, bombas_definidas, casas_bombas):

            nivel = 'pessoa'
            if tam == 8: nivel = 'Soldado'
            if tam == 12: nivel = 'sargento'
            if tam == 16: nivel = 'Tenente'
            if tam == 20: nivel = 'capitão'

            font = pygame.font.SysFont('impact', 45)
            txt_win = font.render(f"Parábens {nivel}", True, black)
            img_win = pygame.image.load("Imagens/win-rd.jpg")
            screen.blit(fundo, (0, 0))
            screen.blit(img_win, (25, 10))
            screen.blit(txt_win, (40, 30))
            pygame.display.update()
            sleep(5)
            break
        pygame.display.update()

