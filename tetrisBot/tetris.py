# imports
import pygame, sys
from config import *
from naturalSelection import *


#--------------estructura principal del juego-------------#
def iddle(piece, rotation):
    p = []
    for x in range(0, 4):
        p.append(piece[x][rotation])
    return p

def board():
    board = []
    for x in range(ROWS):
        row = []
        for y in range(COLS):
            row.append(0)
        board.append(row)
    return board

# determinar si la pieza esta en posibilidades de moverse
def collision(board, piece, offx, offy):
    for y, r in enumerate(piece):
        for x, c in enumerate(r):
            try:
                if c and board[y + offy][x + offx]:
                    return True
                if c and (x + offx < 0):
                    return True
            except IndexError:
                if c:
                    return True
    return False

def remove_row(board, y):
    del board[y]
    return [[0 for i in range(COLS)]] + board

# une la pieza con la superficie y verifica
# que no surjan errores
def merge(a, b, offx, offy):
    d = a
    e = b
    for y, r in enumerate(e):
        for x, c in enumerate(r):
            try:
                if c:
                    d[y + offy][x + offx] = c
            except IndexError:
                if c:
                    print("ERROR MERGING AT " + x + " " + y)
    return d

class Tetris(object):
    def __init__(self, draw):
        pygame.init()
        pygame.key.set_repeat(250, 100)
        self.width = sz * (COLS + 10)
        self.height = sz * (ROWS)
        self.shouldDraw = draw
        self.stuff = 0
        self.myfont = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        self.pop = NatutalSelection(POP_size)

        self.init()

    def new_piece(self):
        #print("New Piece")
        self.curr = self.next[:]
        #self.next = tetrominoes[rand(len(tetrominoes))]
        self.played += 1
        if self.played > len(self.pop.dna):
            self.played = 0

        # pueden surgir ciertas inconsistencias en el proceso
        self.next = tetrominoes[self.pop.dna[self.played]]
        self.curr_x = int(COLS / 2 - 2)
        self.curr_y = 0
        self.rotation = 0
        if collision(self.board, iddle(self.curr, self.rotation), self.curr_x, self.curr_y):
            self.gameOver = True

    # inicializar los valores
    def init(self):
        #print("initialized")
        self.board = board()
        self.played = 0
        self.next = tetrominoes[self.pop.dna[self.played]]
        self.new_piece()
        self.level = 1
        self.score = 0
        self.lines = 0
        self.gameOver = False
        pygame.time.set_timer(pygame.USEREVENT, START_delay)
        self.timeAlive = 0

    def draw(self, m, offx, offy):
        for y, r in enumerate(m):
            for x, c in enumerate(r):
                if c:
                    rect = pygame.Rect((offx + x) * sz, (offy + y) * sz, sz - 1.5, sz - 1.5)
                    pygame.draw.rect(self.screen, pygame.Color(colors[c]), rect, 4)

    def move(self, dir):
        x = self.curr_x + dir
        # revertir movimiento
        if collision(self.board, iddle(self.curr, self.rotation), x, self.curr_y):
                x = self.curr_x
        self.curr_x = x

    def check_clear(self):
        cleared = 0
        while 1:
            for y, r in enumerate(self.board):
                if 0 not in r:
                    self.board = remove_row(self.board, y)
                    cleared += 1
                    break
            else:
                break

        if cleared > 0:
            scores = [0,40,100,300,1200]
            self.score += scores[cleared] * (self.level)
            self.lines += cleared
            self.level = self.lines // 6 + 1

    def gravity(self):
        y = self.curr_y + 1
        # encontrar espacios libres en las filas
        if collision(self.board, iddle(self.curr, self.rotation), self.curr_x, y):
            self.board = merge(self.board, iddle(self.curr, self.rotation), self.curr_x, self.curr_y)
            self.check_clear()
            self.new_piece()

        else:
            self.curr_y = y

    def print_scores(self, i):

        # mostrar la pieza siguiente
        text = self.myfont.render('Next Piece:', False, (0, 0, 0))
        self.screen.blit(text, (COLS * sz + 30, 10))
        self.draw(iddle(self.next, 0), COLS + 2, 1)

        # scores del juego
        text = self.myfont.render('Score: ' + str(self.score + self.pop.pop[i].timeAlive), False, (0, 0, 0))
        self.screen.blit(text, (COLS * sz + 30, 100))
        text = self.myfont.render('Level: ' + str(self.level), False, (0, 0, 0))
        self.screen.blit(text, (COLS * sz + 30, 120))
        text = self.myfont.render('Lines Complete: ' + str(self.lines), False, (0, 0, 0))
        self.screen.blit(text, (COLS * sz + 30, 140))
        text = self.myfont.render('Gen : ' + str(self.pop.gen) + ' person: ' + str(i + 1), False, (0, 0, 0))
        self.screen.blit(text, (COLS * sz + 30, 160))
        text = self.myfont.render('Best Score: ' + str(self.pop.globalBest), False, (0, 0, 0))
        self.screen.blit(text, (COLS * sz + 30, 180))
        text = self.myfont.render('Pieces played: ' + str(self.pop.pop[i].timeAlive), False, (0, 0, 0))
        self.screen.blit(text, (COLS * sz + 30, 200))
        text = self.myfont.render('Last gen best: ' + str(self.pop.currentBest), False, (0, 0, 0))
        self.screen.blit(text, (COLS * sz + 30, 220))

    def neural_input(self, individual):

        # cargar tablero
        n = copy.deepcopy(self.board)
        p = copy.deepcopy(iddle(self.curr, self.rotation))
        for i, r in enumerate(n):
            for k, q in enumerate(r):
                if q:
                    n[i][k] = 1
        # cargar pieza actual
        for i, r in enumerate(p):
            for k, q in enumerate(r):
                if q:
                    n[i][k] = 2

        n = merge(n, p, self.curr_x, self.curr_y)[:]

        # valores obtenidos por la red neuronal
        event = individual.brain.output(n)
        str = " "
        if event == 0:
            str = "left"
            self.move(-1)
        elif event == 1:
            str = "right"
            self.move(+1)
        elif event == 2:
            str = "rotate"
            self.newRotation = self.rotation + 1
            if self.newRotation > 3:
                self.newRotation = 0
            if not collision(self.board, iddle(self.curr, self.newRotation), self.curr_x, self.curr_y):
                self.rotation = self.newRotation
        elif event == 3:
            str = "down"
            # self.gravity()

        text = self.myfont.render("move " + str, False, (0, 0, 0))
        self.screen.blit(text, (COLS * sz + 10, 250))

    def keyboard_input(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    raise SystemExit(0)
                if event.key == pygame.K_p:
                    if self.stuff == 0:
                        self.stuff = 1
                    else:
                        self.stuff = 0
    def play(self):
        self.gameOver = False
        limit = pygame.time.Clock()
        # bucle principal del juego
        while 1:
            for i in range(self.pop.populationSize):
                count = 0
                while 1:
                    if self.gameOver:
                        print(i, "Fitness:", self.pop.pop[i].fitness)
                        self.init()
                        break
                    elif self.shouldDraw:
                        self.screen.fill((255, 255, 255))
                        # sys.stdin.read(1)
                        self.draw(self.board, 0, 0)
                        self.draw(iddle(self.curr, self.rotation), self.curr_x, self.curr_y)
                        pygame.draw.line(self.screen, (0, 0, 0), (COLS * sz + 2, 0), (COLS * sz + 2, self.height))
                        self.print_scores(i)
                        self.neural_input(self.pop.pop[i])
                        self.timeAlive += 1
                        self.pop.pop[i].timeAlive = self.played
                        self.pop.pop[i].score = self.score
                        self.pop.pop[i].lines = self.lines
                        self.pop.pop[i].level = self.level
                        self.pop.pop[i].set_fitness()

                        count += 1
                        if count > VEL:
                            self.gravity()
                            count = 0

                        # print(i)
                        self.keyboard_input()
                        if self.stuff == 0:
                            pygame.display.update()

                    limit.tick(FPS)

            self.pop.pop = self.pop.evolve()
            pygame.event.get()