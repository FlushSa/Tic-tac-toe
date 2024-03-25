import sys
import copy
import pygame
import numpy as np
from data import *


pygame.init()
obraz = pygame.display.set_mode((SIRKA, VYSKA))
pygame.display.set_caption('Piškvorky')
obraz.fill(POZADI)

class Board:

    def __init__(self):
        self.squares = np.zeros((ROW, COLUMN))
        self.marked_sqrs = 0

    def mark_sqr(self, row, column, player):
        self.squares[row][column] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, column):
        return self.squares[row][column] == 0

    def get_empty_sqr(self):
    	empty_sqr = []
    	for row in range(ROW):
    		for column in range(COLUMN):
    			if self.empty_sqr(row, column):
    				empty_sqr.append ((row, column))
    	return empty_sqr

    

    def winner(self, show=False):
    # svislé
        for column in range(COLUMN):
            for row in range(ROW - 3):
                if self.squares[row][column] == self.squares[row + 1][column] == self.squares[row + 2][column] == self.squares[row + 3][column] != 0:
                    if show:
                        start = (column * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
                        end = (column * SQSIZE + SQSIZE // 2, (row + 4) * SQSIZE - SQSIZE // 2)
                        pygame.draw.line(obraz, LINE_COLOR, start, end, LINE_WIDTH)
                    return self.squares[row][column]

        # vodorovné
        for row in range(ROW):
            for column in range(COLUMN - 3):
                if self.squares[row][column] == self.squares[row][column + 1] == self.squares[row][column + 2] == self.squares[row][column + 3] != 0:
                    if show:
                        start = (column * SQSIZE + SQSIZE // 4, row * SQSIZE + SQSIZE // 2)
                        end = ((column + 4) * SQSIZE - SQSIZE // 4, row * SQSIZE + SQSIZE // 2)
                        pygame.draw.line(obraz, LINE_COLOR, start, end, LINE_WIDTH)
                    return self.squares[row][column]

        # diagonály
        for row in range(ROW - 3):
            for column in range(COLUMN - 3):
                if self.squares[row][column] == self.squares[row + 1][column + 1] == self.squares[row + 2][column + 2] == self.squares[row + 3][column + 3] != 0:
                    if show:
                        start = (column * SQSIZE + SQSIZE // 4, row * SQSIZE + SQSIZE // 4)
                        end = ((column + 4) * SQSIZE - SQSIZE // 4, (row + 4) * SQSIZE - SQSIZE // 4)
                        pygame.draw.line(obraz, LINE_COLOR, start, end, LINE_WIDTH)
                    return self.squares[row][column]

        for row in range(ROW - 3):
            for column in range(3, COLUMN):
                if self.squares[row][column] == self.squares[row + 1][column - 1] == self.squares[row + 2][column - 2] == self.squares[row + 3][column - 3] != 0:
                    if show:
                        start = ((column + 1/ 2) * SQSIZE + SQSIZE // 4, row * SQSIZE + SQSIZE // 4)
                        end = ((column - 3) * SQSIZE + SQSIZE // 4, (row + 4) * SQSIZE - SQSIZE // 4)
                        pygame.draw.line(obraz, LINE_COLOR, start, end, LINE_WIDTH)
                    return self.squares[row][column]

        return 0



    def isfull(self):
        return self.marked_sqrs == 36

    def isempty(self):
        return self.marked_sqrs == 0


class Game:

    def __init__(self):
        self.board = Board()
        self.player = 1
        self.running = True
        self.show_lines()
       
        #Čáry na rozdělení desky
    def show_lines(self):

        obraz.fill(POZADI)
        
        #Diagonální 
        for i in range(1, 6):
            x = i * SQSIZE
            pygame.draw.line(obraz, LINE_COLOR, (x, SQSIZE), (x, VYSKA), LINE_WIDTH)

            #Vodorovné
        for i in range(1, 7):
            y = i * SQSIZE
            pygame.draw.line(obraz, LINE_COLOR, (0, y), (SIRKA, y), LINE_WIDTH)


        #Přehazování hráčů (křížek a kolečko)
   
    def next_turn(self):
    	self.player = self.player % 2 + 1

        
        # Hráč 1 - kříž
   
    def draw_fig(self, row, column):
        if self.player == 1:
            start = (column * SQSIZE + ODSAZENI, row * SQSIZE + ODSAZENI)
            end = (column * SQSIZE + SQSIZE - ODSAZENI, row * SQSIZE + SQSIZE - ODSAZENI)

            pygame.draw.line(obraz, CROSS_COLOR, start, end, CROSS_WIDTH)
            pygame.draw.line(obraz, CROSS_COLOR, (start[0], end[1]), (end[0], start[1]), CROSS_WIDTH)

        # Hráč 2 - kolečko
        elif self.player == 2:
            center = (column * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(obraz, CIRC_COLOR, center, PRUMER, CIRC_WIDTH)

        # definování funkce, kdy končí
   
    def isover(self):
        return self.board.winner(show=True) != 0 or self.board.isfull()
    
    def reset(self):
        self.__init__()

    def make_move(self, row, column):
        self.board.mark_sqr(row, column, self.player)
        self.draw_fig(row, column)
        self.next_turn()



def main():
    game = Game()
    board = game.board

    while True:
        
        # pygame events
        for event in pygame.event.get():

            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # keydown event
            if event.type == pygame.KEYDOWN:

                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board

            # click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                column = pos[0] // SQSIZE
                
                # human mark sqr
                if board.empty_sqr(row, column) and game.running:
                    game.make_move(row, column)

                    if game.isover():
                        game.running = False



        pygame.display.update()

main()