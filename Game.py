from random import randint
import pygame
from time import sleep

# Definição de tela
screen = pygame.display.set_mode((450, 510))    # Define o tamanho da tela

# Definir cores
black = (0, 0, 0)
green = (21, 237, 54)

# Definir Texto
pygame.font.init()      # Inicia a fonte do pygame
font = pygame.font.SysFont("impact", 35)    # Define a fonte do pygame
text_title = font.render("Campo Minado", True, green)   # Gera o texto

# Definir Imagens
fundo = pygame.image.load("Imagens/fundo/floresta_desfocada.jpg")
default = pygame.image.load("Imagens/tabuleiro/default.png")
mine = pygame.image.load("Imagens/tabuleiro/mine.png")
img_bandeira = pygame.image.load("Imagens/fundo/bandeira-1.png")
tab_bandeira = pygame.image.load("Imagens/tabuleiro/bandeira.png")
voltar_icone = pygame.image.load("Imagens/fundo/icone-voltar.png ")
voltar_icone_clicked = pygame.image.load("Imagens/fundo/icone-voltar-clicked.png")
empty = []

"""Explicar essa parte"""
for i in range(0, 9):
    empty.append(pygame.image.load(f"Imagens/tabuleiro/empty{i}.png"))

# Mostrar local que aparecerá o numero de bombas
screen.blit(img_bandeira, (280, 453))


# Funções
def criarbomba(tam):    # Função responsável por definir os locais das bombas
    quant_bomb = int((tam*tam)*0.20)    # Define a quantidade de bombas, baseado no tamanho do tabuleiro
    bomb = []                           # Lista de bombas
    count = 0                           # Contador
    while count < quant_bomb:           # Enquanto o contador for menor que a quantidade de bombas
        casa = (randint(0, tam-1), randint(0, tam-1))   # Define uma tupla guardando dois numeros gerados aleatóriamente
        if casa not in bomb:                            # Verifica se a casa gerada já está na lista de bombas
            bomb.append(casa)                           # Adiciona a casa sorteada a lista de bombas
            count += 1                                  # Adiciona um numero ao contador
    return bomb                                         # Retorna a lista de bombas que foi gerada


def abrir_casa(pos, list_bomb, tam_casa):   # Função responsável por abrir uma casa
    redor = ((pos[0]-1, pos[1]-1),      # Guarda todas as casas ao redor da casa clicada em uma lista
             (pos[0]-1, pos[1]),
             (pos[0]-1, pos[1]+1),
             (pos[0],   pos[1]-1),
             (pos[0],   pos[1]),
             (pos[0],   pos[1]+1),
             (pos[0]+1, pos[1]-1),
             (pos[0]+1, pos[1]),
             (pos[0]+1, pos[1]+1))

    quant_bomba = 0                 # Variavel para guardar a quantidade de bombas
    for bomb in list_bomb:          # Para cada bomba na lista de bombas
        for casa in redor:          # Pra cada casa na lista "redor"
            if casa == bomb:        # Se a casa for igual a bomba
                quant_bomba += 1    # Adicinar 1 na quantidade de bombas

    posicao_casa = ((pos[0] * tam_casa) + 25), int((pos[1] * tam_casa) + 50)    # Define a posição da casa em pixels
    if pos in list_bomb:        # Se a casa clicada estiver na lista de bombas
        screen.blit(bomb_img, posicao_casa)     # Mostrar na tela a imagem de bomba
        pygame.display.update()                 # Atualizar a tela
        sleep(0.3)                              # Esperar 0.3 segundos (cria um efeito lgl)
        perder()                                # Chama a função perder
        return True                             # retorna verdadeiro
    else:
        screen.blit(empty[quant_bomba], posicao_casa)   # Mostra na tela a imagem da bomba
    return False                                # retorna falso


def ganhar(casas_abertas, tamanho_tabuleiro, casas_marcadas, casas_bombas):     # verifica se o jogador ganhou o jogo
    bombas_marcadas_certas = 0                                                          # variavel que será marcado a quantidade de bombas definidas corretamente
    if len(casas_abertas) == (tamanho_tabuleiro*tamanho_tabuleiro)-len(casas_bombas):   # se a quantidade de casas abertas for igual ao total de casas menos a quantidade de casas que tem bomba
        for casa in casas_marcadas:                                                     # para cada casa nas casas marcadas pelo jogador
            if casas_bombas.count(casa) == 1:                                           # se a quatidade de vezes que a casa marcada pelo jogador aparece na lista de bombas for igual a 1
                bombas_marcadas_certas += 1                                             # Adicinar 1 na quantidade de bombas marcadas corretamente

    if bombas_marcadas_certas == int((tamanho_tabuleiro*tamanho_tabuleiro)*0.20):   # se a quantidade de bombas marcadas corretamente for igual a quantidade de bombas
        return True     # retorna verdadiro, ou seja, o jogador ganhou


def perder():   # Irá mostrar na tela a mensagem de que o jogador perrdeu
    img_lost = pygame.image.load("Imagens/lost-rd.jpg")     # Carrega a imagem
    screen.blit(fundo, (0, 0))                              # mostra a imagem de fundo, ou seja, apaga oq tiver na tela
    screen.blit(img_lost, (25, 110))                        # mostra a imagem de que o jogador perdeu
    pygame.display.update()                                 # atualiza a tela
    sleep(2)                                                # espera dois segundos


def game(tam):          # Função principal do jogo
    sleep(1/60)     # Trava o jogo em 60 atualizações por minuto (60 FPS)

    global padrao, bandeira_casa, bomb_img  # Define algumas variáveis que possuem escopo global, ou seja, funcionam em qualquer parte do programa

    pygame.init()   # Inciar pygame

    screen.blit(fundo, (0, 0))      # Apagar a tela anterior

    screen.blit(text_title, (120, 2))       # mostrar texto (titulo da janela)

    # Define tamanho de cada tipo de casa da tabela
    tam_casa = int(400 / tam)      # define o tamanho da casa
    for c in range(0, 9):
        empty[c] = pygame.transform.scale(empty[c], (tam_casa, tam_casa))
    padrao = pygame.transform.scale(default, (tam_casa, tam_casa))
    bomb_img = pygame.transform.scale(mine, (tam_casa, tam_casa))
    bandeira_casa = pygame.transform.scale(tab_bandeira, (tam_casa, tam_casa))

    screen.blit(img_bandeira, (280, 453))   # Mostrar local de numero de bombas definidas

    screen.blit(voltar_icone, (50, 453)) # Mostrar botão de voltar

    # Criar tabela
    pos_casa = (25, 50)     # posição da primeira casa da tabela
    for i in range(0, tam):         # cria um contador que vai de 0 até o numero de casas da tabela
        for c in range(0, tam):     # Ccria um contador que vai de 0 até o numero de casas da tabela
            # cria uma linha
            screen.blit(padrao, pos_casa)   # Mostra na tela a figura padrão para formar a tabela
            pos_casa = (pos_casa[0] + tam_casa, pos_casa[1])    # Atualiza a posição para o local da proxima casa (na linha)
        # desce uma coluna
        pos_casa = (25, pos_casa[1] + tam_casa)     # Atualiza a posição para o local da proxima coluna
    pygame.display.update() # Atualiza a tela

    # Variáveis
    casas_bombas = criarbomba(tam)  # Criar Bombas
    bombas_definidas = []           # Casas das bombas marcadas pelo jogador
    casas_abertas = []              # Guarda as casas que já foram abertas
    find_bomb = False               # Guarda se o jogador clicar ou não em uma bomba

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

                    # Se o botão esquerdo do mause for clicado (abrir casa, ou voltar)
                    if pygame.mouse.get_pressed()[0] == 1:      # Confere se o botão esquerdo foi clicado
                        if casa_mouse[0] < tam and casa_mouse[1] < tam:     # Confere se a posição que houve o clique do mouse foi dentro do tabuleiro
                            if casa_mouse not in bombas_definidas:          # Se a casa clicada não estiver sido marcada como bomba pelo jogador
                                find_bomb = abrir_casa(casa_mouse, casas_bombas, tam_casa)  # Armazena o resultado da função (Se o usuario clicar em bomba irá retorna verdadeiro)
                                casas_abertas.append(casa_mouse)            # Adiciona a casa clicada à lista de casas abertas

                        if 90 > pos_mouse[0] > 50 and 453 < pos_mouse[1] < 495: # Confere se o clique foi feito na região do botão de voltar
                            screen.blit(voltar_icone_clicked, (50, 453))    # Mostra a imagem um pouco mais escura do botão de clicar
                            pygame.display.update()     # Atualiza a tela
                            sair = False                # Define o final do loop
                            sleep(0.2)                  # Espera 0.2 segundos

                    # Se o Botão direito for clicado (marcar casa)
                    elif pygame.mouse.get_pressed()[2] == 1:    # Confere se o botão direito foi clicado
                        if casa_mouse[0] < tam and casa_mouse[1] < tam:     # Confere se o clique ocorreu na tabela
                            if casa_mouse in bombas_definidas:              # Se a casa clicada já estiver na lista de bombas definidas
                                bombas_definidas.pop(bombas_definidas.index(casa_mouse))    # Remover a casa da lista de bombas definidas
                                screen.blit(padrao, posicao_casa)       # Mostra a imagem padrão
                            else:
                                bombas_definidas.append(casa_mouse)         # Adicionar a casa na lista de bombas definidas
                                screen.blit(bandeira_casa, posicao_casa)    # Mostrar a imagem de bomba

                            # Atualizar o contador de bombas
                            fonte = pygame.font.SysFont('impact', 30)       # Definir fonte
                            screen.blit(img_bandeira, (280, 453))           # Mostrar a imagem da bandeira
                            txt_num_bombas_abertas = fonte.render(len(bombas_definidas), True, black)   # Gerar a quantidade de bombas marcadas
                            screen.blit(txt_num_bombas_abertas, (335, 457))     # Mostrar na tela o numero de bombas

        if find_bomb:   # Se o usuario tiver clicado em uma bomba
            break       # Finaliza o loop

        if ganhar(casas_abertas, tam, bombas_definidas, casas_bombas):  # Verifica se o usuario ganhou o jogo
            #   Define o nível que a pessoa está jogando, para mostrar na tela
            nivel = 'pessoa'
            if tam == 8: nivel = 'Soldado'
            if tam == 12: nivel = 'sargento'
            if tam == 16: nivel = 'Tenente'
            if tam == 20: nivel = 'capitão'

            fonte = pygame.font.SysFont('impact', 45)                   # Define a fonte do texto
            txt_win = fonte.render(f"Parábens {nivel}", True, black)    # Define o texto
            img_win = pygame.image.load("Imagens/win-rd.jpg")           # Carrega a imagem de quando o jogador ganha
            screen.blit(fundo, (0, 0))                                  # Apaga o que tem na tela
            screen.blit(img_win, (25, 10))                              # Mostra a imagem de vitória
            screen.blit(txt_win, (40, 30))                              # Mostra o texto
            pygame.display.update()                                     # Atualiza a tela
            sleep(5)                                                    # Espera 5 segundos
            break                                                       # Finaliza o jogo

        pygame.display.update()     # Atualiza a tela no final de cada loop

