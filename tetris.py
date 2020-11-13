# André Philipe Andriotti de Moraes     TIA: 32013965
# Carlos Manoel Pedrosa de Oliveira     TIA: 32068549
# Felipe Padilha Ferreira               TIA: 32013434
# Gabriel Kazuiti Aiura                 TIA: 32047231
# Pedro Galvão Barretto                 TIA: 32016591

import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Tetris')

mainClock = pygame.time.Clock()

font = pygame.font.SysFont(None, 70)

background = pygame.image.load('./imagens/background.png')
tetris_logo = pygame.image.load('./imagens/tetris_logo.png')
gameover = pygame.image.load('./imagens/gameover.png')
icon = pygame.image.load('./imagens/icon.png')
chest = pygame.image.load('./imagens/score.png')
pygame.mixer.music.load('./sounds/pirate.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.display.set_icon(icon)

play_width = 360
play_height = 600
top_left_x = 120
top_left_y = 100
down_right_x = top_left_x + play_width
down_right_y = top_left_y + play_height
block_size = 30
x = top_left_x + play_width // 2
y = top_left_y

# Cores
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BEIGE = (255, 253, 237)
ORANGE = (222, 128, 33)
BROWN = (128, 87, 25)
DARK_BROWN = (56, 32, 3)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PINK = (255, 0, 255)
GRAY = (128, 128, 128)

color_list = [RED, BEIGE, BROWN, ORANGE, YELLOW, GREEN, CYAN]


def draw_text(text, font, color, surface, x, y):

    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def menu():

    screen.blit(tetris_logo, (0, 0))


def gameOver():

    screen.blit(gameover, (0, 0))
    Score(630, 10)


def drawBox():

    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, BROWN, (top_left_x, top_left_y,
                                     play_width, play_height), 4)


def drawGrid():

    x_row = top_left_x
    y_row = top_left_y + block_size
    x_column = top_left_x + block_size
    y_column = top_left_y
    for row in range(19):
        pygame.draw.line(screen, BROWN, (x_row, y_row),
                         (x_row + play_width, y_row))
        y_row += block_size
    for column in range(11):
        pygame.draw.line(screen, BROWN, (x_column, y_column),
                         (x_column, y_column + play_height))
        x_column += block_size


def grayGrid():

    for row in range(20):
        for collumn in range(12):
            if grid[row][collumn] == 1:
                x_block = (collumn * block_size) + top_left_x
                y_block = (row * block_size) + top_left_y
                pygame.draw.rect(
                    screen, DARK_BROWN, (x_block, y_block, block_size, block_size))


def createPieces(x, y):

    I = [[RED, [x, y], [x, y + block_size], [x, y + block_size * 2], [x, y + block_size * 3]],
         [RED, [x-block_size, y+block_size], [x, y+block_size], [x+block_size, y+block_size], [x+block_size*2, y+block_size]]]

    J = [[BEIGE, [x, y], [x, y+block_size], [x, y+block_size*2], [x - block_size, y + block_size*2]],
         [BEIGE, [x, y+block_size], [x-block_size, y+block_size],
             [x-block_size, y], [x+block_size, y+block_size]],
         [BEIGE, [x, y], [x, y + block_size],
             [x, y + block_size * 2], [x+block_size, y]],
         [BEIGE, [x, y+block_size], [x-block_size, y+block_size], [x+block_size, y+block_size*2], [x+block_size, y+block_size]]]

    L = [[PINK, [x, y], [x, y+block_size], [x, y+block_size*2], [x+block_size, y+block_size*2]],
         [PINK, [x, y+block_size], [x-block_size, y+block_size],
             [x+block_size, y+block_size], [x-block_size, y+block_size*2]],
         [PINK, [x, y], [x, y+block_size], [x, y+block_size*2], [x-block_size, y]],
         [PINK, [x, y+block_size], [x-block_size, y+block_size], [x+block_size, y+block_size], [x+block_size, y]]]

    O = [[ORANGE, [x, y], [x-block_size, y],
          [x-block_size, y+block_size], [x, y+block_size]]]

    S = [[YELLOW, [x, y], [x, y+block_size], [x+block_size, y], [x-block_size, y+block_size]],
         [YELLOW, [x, y], [x, y+block_size], [x+block_size, y+block_size], [x+block_size, y+block_size*2]]]

    T = [[GREEN, [x, y], [x, y+block_size], [x+block_size, y+block_size], [x-block_size, y+block_size]],
         [GREEN, [x, y], [x, y+block_size],
             [x+block_size, y+block_size], [x, y+block_size*2]],
         [GREEN, [x, y+block_size*2], [x, y+block_size],
             [x+block_size, y+block_size], [x-block_size, y+block_size]],
         [GREEN, [x, y], [x, y+block_size], [x-block_size, y+block_size], [x, y+block_size*2]]]

    Z = [[CYAN, [x, y], [x, y+block_size], [x-block_size, y], [x+block_size, y+block_size]],
         [CYAN, [x, y], [x, y+block_size], [x-block_size, y+block_size], [x-block_size, y+block_size*2]]]

    pieces = [I, J, L, O, S, T, Z]

    return pieces


def drawPieces(piece, num_piece):

    pygame.draw.rect(screen, piece[0], (piece[1]
                                        [0], piece[1][1], block_size, block_size))
    pygame.draw.rect(screen, piece[0], (piece[2]
                                        [0], piece[2][1], block_size, block_size))
    pygame.draw.rect(screen, piece[0], (piece[3]
                                        [0], piece[3][1], block_size, block_size))
    pygame.draw.rect(screen, piece[0], (piece[4]
                                        [0], piece[4][1], block_size, block_size))


def checkLine():

    global score

    for i in grid:
        if sum(i) == 12:
            grid.remove(i)
            grid.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            score += 1


def Score(x, y):

    x_text = x + 59
    y_text = y + 140
    score_text = font.render(str(score), 1, BROWN)
    screen.blit(chest, (x, y))
    screen.blit(score_text, (x_text, y_text))


def nextShape():

    return random.randint(0, 6)


def sizePiece(piece, pieceIndex):

    max_x = top_left_x
    min_x = down_right_x
    max_y = top_left_y
    min_y = down_right_y

    for i in range(4):
        if piece[i+1][0] > max_x:
            max_x = piece[i+1][0]
        if piece[i+1][0] < min_x:
            min_x = piece[i+1][0]

        if piece[i+1][1] > max_y:
            max_y = piece[i+1][1]
        if piece[i+1][1] < min_y:
            min_y = piece[i+1][1]

    width = (max_x - min_x) + block_size
    height = (max_y - min_y) + block_size

    return width, height, min_x, max_x


def collision(piece, collide_y, next_rotation):

    game_over = False
    collide_x_left = False
    collide_x_right = False
    can_rotate = True

    pos_blocks = []

    for i in range(4):
        row = (piece[i+1][1] - top_left_y) // block_size
        collumn = (piece[i+1][0] - top_left_x) // block_size
        pos_blocks.append([row, collumn])

    for i in range(4):
        row = pos_blocks[i][0]
        collumn = pos_blocks[i][1]

        if next_rotation == False:

            # Colisão com o topo da tela
            if row == 0 and grid[row+1][collumn] == 1:
                game_over = True

            # Colisão com o fim da tela
            if row+1 == 20:
                collide_y = True

            # Colisão com o chão da peça
            elif collumn < 12:
                if grid[row+1][collumn] == 1:
                    collide_y = True

            if 0 < collumn < 11:

                # Colisão com a esquerda da peça
                if grid[row][collumn-1] == 1:
                    collide_x_left = True

                # Colisão com a direita da peça
                if grid[row][collumn+1] == 1:
                    collide_x_right = True

            if collide_y == True:
                for b in range(4):
                    row = pos_blocks[b][0]
                    collumn = pos_blocks[b][1]
                    grid[row][collumn] = 1

        else:

            if 0 < collumn < 11 and row < 20:

                # Verifica espaço vago
                if grid[row][collumn] == 1:
                    can_rotate = False

    return game_over, collide_x_left, collide_x_right, collide_y, can_rotate


def rotatePiece(rotation, pieces, pieceIndex):

    if rotation == len(pieces[pieceIndex])-1:
        rotation = 0

    elif rotation < len(pieces[pieceIndex])-1:
        rotation += 1

    return rotation


def canRotate(pieces, pieceIndex, rotation, can_rotate):

    collide_x_left = False
    collide_x_right = False
    collide_y = False
    next_rotation = True

    if rotation == len(pieces[pieceIndex])-1:
        end, collide_x_left, collide_x_right, collide_y, can_rotate = collision(
            pieces[pieceIndex][0], collide_y, next_rotation)

    elif rotation < len(pieces[pieceIndex])-1:
        end, collide_x_left, collide_x_right, collide_y, can_rotate = collision(
            pieces[pieceIndex][rotation+1], collide_y, next_rotation)

    return can_rotate


def checkExcess(piece, x_atual, y_atual, pieceIndex, rotation):

    pos_blocks = []

    for i in range(4):
        row = (piece[i+1][1] - top_left_y) // block_size
        collumn = (piece[i+1][0] - top_left_x) // block_size
        pos_blocks.append([row, collumn])

    for i in range(4):
        row = pos_blocks[i][0]
        collumn = pos_blocks[i][1]

        if collumn < 0:
            excess = collumn * -1
            x_atual += excess * block_size

        elif collumn > 11:
            excess = collumn - 11
            x_atual -= excess * block_size

    pieces = createPieces(x_atual, y_atual)
    piece = pieces[pieceIndex][rotation]

    return pieces, piece, x_atual


def gameLoop():

    x_atual = x
    y_atual = y
    rotation = 0
    pieceIndex = nextShape()

    collide_y = False

    while not collide_y:

        drawBox()
        drawGrid()
        grayGrid()

        pieces = createPieces(x_atual, y_atual)
        piece = pieces[pieceIndex][rotation]

        pieces, piece, x_atual = checkExcess(
            piece, x_atual, y_atual, pieceIndex, rotation)
        width_piece, height_piece, min_x, max_x = sizePiece(piece, pieceIndex)
        end, collide_x_left, collide_x_right, collide_y, can_rotate = collision(
            piece, collide_y, False)
        can_rotate = canRotate(pieces, pieceIndex, rotation, can_rotate)

        drawPieces(piece, pieceIndex)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if collide_x_left == False:
                        if min_x > top_left_x:
                            x_atual -= block_size
                            min_x -= block_size
                            max_x -= block_size

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if collide_x_right == False:
                        if max_x < down_right_x - block_size:
                            x_atual += block_size
                            min_x += block_size
                            max_x += block_size

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if can_rotate == True:
                        rotation = rotatePiece(rotation, pieces, pieceIndex)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if y_atual < down_right_y - height_piece - block_size:
                        y_atual += block_size

        y_atual += 1

        checkLine()
        Score(550, 170)
        pygame.display.update()
        mainClock.tick(60)

        if end == True:
            return end


def main():

    menu()

    while True:

        pygame.mixer.music.play(-1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    global score
                    global grid

                    score = 0
                    grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

                    run = True
                    end = False
                    while run:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        end = gameLoop()
                        if end == True:
                            gameOver()
                            pygame.mixer.music.stop()
                            run = False

            pygame.display.update()
            mainClock.tick(60)


main()
