import time
from random import randint

class AI:
    def __init__(self, game):
        self.game = game

    def guess(self):
        if self.game.style == 'statistical':
            self.normal_guess()
        elif self.game.style == 'hit':
            self.hit_guess()

        self.game.guess_ship(self.guess_coords[0], self.guess_coords[1], self.game.board_com)

    def hit_guess(self):
        #if it's on the right line
        if self.game.hit >= 2:
            #if there's still space in this direction
            if not self.game.wrong_dir:
                if self.direct == 0:
                    self.guess_coords = [self.guess_coords[0], self.guess_coords[-1] - 1]
                elif self.direct == 1:
                    self.guess_coords = [self.guess_coords[0], self.guess_coords[-1] + 1]
                elif self.direct == 2:
                    self.guess_coords = [self.guess_coords[0] - 1, self.guess_coords[-1]]
                elif self.direct == 3:
                    self.guess_coords = [self.guess_coords[0] + 1, self.guess_coords[-1]]

                if (   self.guess_coords[0] > 10
                    or self.guess_coords[0] < 0
                    or self.guess_coords[1] > 10
                    or self.guess_coords[1] < 0
                    or self.game.board_com[self.guess_coords[0]][self.guess_coords[1]] == 'G'
                    ):
                    self.game.wrong_dir = True

            #if there is no more space it goes in the opposite direction
            else:
                #if it missed the previous one it makes a guess based on the original hit
                if self.game.previous_miss:
                    if self.direct == 0:
                        self.guess_coords = [self.game.hit_coords[0], self.game.hit_coords[-1] + 1]
                    elif self.direct == 1:
                        self.guess_coords = [self.game.hit_coords[0], self.game.hit_coords[-1] - 1]
                    elif self.direct == 2:
                        self.guess_coords = [self.game.hit_coords[0] + 1, self.game.hit_coords[-1]]
                    elif self.direct == 3:
                        self.guess_coords = [self.game.hit_coords[0] - 1, self.game.hit_coords[-1]]

                #if it hit the previos one it makes a guess based on the previous hit
                else:
                    if self.direct == 0:
                        self.guess_coords = [self.guess_coords[0], self.guess_coords[-1] + 1]
                    elif self.direct == 1:
                        self.guess_coords = [self.guess_coords[0], self.guess_coords[-1] - 1]
                    elif self.direct == 2:
                        self.guess_coords = [self.guess_coords[0] + 1, self.guess_coords[-1]]
                    elif self.direct == 3:
                        self.guess_coords = [self.guess_coords[0] - 1, self.guess_coords[-1]]

        #if it hit the first tile in a ship or missed after hitting only the original tile
        else:
            self.guess_board = [[0] * len(self.game.board_com) for i in range(len(self.game.board_com))]

            for a in self.game.player_ships:
                self.statistical_guess(a)

            x = self.game.hit_coords[0]
            y = self.game.hit_coords[-1]

            if self.game.board_com[x][y-1] == 'G':
                self.guess_board[x][y-1] = 0

            if self.game.board_com[x][y+1] == 'G':
                self.guess_board[x][y+1] = 0

            if self.game.board_com[x-1][y] == 'G':
                self.guess_board[x-1][y] = 0

            if self.game.board_com[x+1][y] == 'G':
                self.guess_board[x+1][y] = 0

            target_array = [
                            self.guess_board[x][y-1],
                            self.guess_board[x][y+1],
                            self.guess_board[x-1][y],
                            self.guess_board[x+1][y]
                            ]

            target = max(target_array)
            for i, j in enumerate(target_array):
                if j == target:
                    self.direct = i
            
            self.find_coords(self.direct)

    def statistical_guess(self, n):
        # it maps all posibble horizontal placments of a n-sized ship
        for i in range (1, len(self.game.board_com)-1):
            for j in range(1, len(self.game.board_com[i])-1):
                if self.game.board_com[i][j] not in ['G', 'D']:
                    for k in range(1, n):
                        if self.game.board_com[i][j+k] in ['G', 'D']: break
                        elif j + k > len(self.game.board_com) - 2: break
                    else:
                        for k in range(n):
                            self.guess_board[i][j+k] += 1

        # it maps all posibble vertical placments of a n-sized ship
        for i in range (1, len(self.game.board_com)-1):
            for j in range(1, len(self.game.board_com[i])-1):
                if self.game.board_com[i][j] not in ['G', 'D']:
                    for k in range(1, n):
                        if self.game.board_com[i+k][j] in ['G', 'D']: break
                        elif i + k > (len(self.game.board_com) - 2): break
                    else:
                        for k in range(n):
                            self.guess_board[i+k][j] += 1

    def normal_guess(self):
        max_list = []
        self.pos_guess = []
        self.guess_board = [[0] * len(self.game.board_com) for i in range(len(self.game.board_com))]

        for k in self.game.player_ships:
            self.statistical_guess(k)

        for row in self.guess_board:
            max_list.append(max(row))

        for i in range(len(self.guess_board)):
            for j in range(len(self.guess_board)):
                if self.guess_board[i][j] == max(max_list):
                    self.pos_guess.append([i,j])

        pos = randint(0, len(self.pos_guess) - 1)
        self.guess_coords = self.pos_guess[pos]

    def find_coords(self, i):
        if i == 0:
            self.guess_coords = [self.game.hit_coords[0], self.game.hit_coords[-1] - 1]
        elif i == 1:
            self.guess_coords = [self.game.hit_coords[0], self.game.hit_coords[-1] + 1]
        elif i == 2:
            self.guess_coords = [self.game.hit_coords[0] - 1, self.game.hit_coords[-1]]
        elif i == 3:
            self.guess_coords = [self.game.hit_coords[0] + 1, self.game.hit_coords[-1]]

        if self.game.board_com[self.guess_coords[0]][self.guess_coords[1]] == 'G':
            self.guess_board[self.guess_coords[0]][self.guess_coords[1]] = 0