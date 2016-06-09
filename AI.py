import time
from random import randint

class AI:
    def __init__(self, game):
        self.game = game
        self.mode = "statistical"
        self.hit = 0
        self.compass = None

    def find_coords(self, i):
        if i == 0:
            self.guess_coords = [self.hit_coords[0] + 1, self.hit_coords[-1]]
        elif i == 1:
            self.guess_coords = [self.hit_coords[0] - 1, self.hit_coords[-1]]
        elif i == 2:
            self.guess_coords = [self.hit_coords[0], self.hit_coords[-1] + 1]
        elif i == 3:
            self.guess_coords = [self.hit_coords[0], self.hit_coords[-1] - 1]
        if self.game.board_com[self.guess_coords[0]][self.guess_coords[1]] in ["G", "H"]:
            self.guess_board[self.guess_coords[0]][self.guess_coords[1]] = 0



    def hit_guess(self):
        self.hit = self.game.hit
        self.previous_miss = self.game.previous_miss
        self.hit_coords = self.game.hit_coords

        #če je prej zadel(je na pravi premici)
        if self.hit >= 2:
            #če je v tej smeri še prostor
            if not self.game.wrong_dir:
                if self.dir == 0:
                    self.guess_coords = [self.guess_coords[0] + 1, self.guess_coords[-1]]
                elif self.dir == 1:
                    self.guess_coords = [self.guess_coords[0] - 1, self.guess_coords[-1]]
                elif self.dir == 2:
                    self.guess_coords = [self.guess_coords[0], self.guess_coords[-1] + 1]
                elif self.dir == 3:
                    self.guess_coords = [self.guess_coords[0], self.guess_coords[-1] - 1]
            #če v tej smeri ni več prostora (ampak je na pravi premici) gre v nasprotno smer
            elif self.game.wrong_dir:
                #če je prejšnjo zgrešil se nanaša na originalen zadetek
                if self.previous_miss:
                    print("self.dir: ", self.dir)
                    if self.dir == 0:
                        self.guess_coords = [self.hit_coords[0] - 1, self.hit_coords[-1]]
                    elif self.dir == 1:
                        self.guess_coords = [self.hit_coords[0] + 1, self.hit_coords[-1]]
                    elif self.dir == 2:
                        self.guess_coords = [self.hit_coords[0], self.hit_coords[-1] - 1]
                    elif self.dir == 3:
                        self.guess_coords = [self.hit_coords[0], self.hit_coords[-1] + 1]
                #če je prejšnjo zadel se nanaša na prejšnjo
                else:
                    if self.dir == 0:
                        self.guess_coords = [self.guess_coords[0] - 1, self.guess_coords[-1]]
                    elif self.dir == 1:
                        self.guess_coords = [self.guess_coords[0] + 1, self.guess_coords[-1]]
                    elif self.dir == 2:
                        self.guess_coords = [self.guess_coords[0], self.guess_coords[-1] - 1]
                    elif self.dir == 3:
                        self.guess_coords = [self.guess_coords[0], self.guess_coords[-1] + 1]

                    print("Say hi to your dads!")

        #če je prvič zadel ali če je prejšnjo zgrešil
        else:
            print("Stage 0")
            self.guess_board = []
            for i in range(len(self.game.board_com)):
                self.guess_board.append([0 for j in range(len(self.game.board_com))])
            for a in self.game.player_ships:
                self.statistical_guess(a)

            x = self.hit_coords[0]
            y = self.hit_coords[-1]
            target_array = [self.guess_board[x+1][y], self.guess_board[x-1][y], self.guess_board[x][y+1], self.guess_board[x][y-1]]
            target = max(target_array)
            for i, j in enumerate(target_array):
                if j == target:
                    self.dir = i
                    self.find_coords(i)




    def statistical_guess(self, n):
        for i in range (1, len(self.game.board_com)-1):
            for j in range(1, len(self.game.board_com[i])-1):
                if self.game.board_com[i][j] not in ["G", "D"]:
                    obstructed = False
                    for k in range(1, n):
                        if self.game.board_com[i][j+k] in ["G", "D"] or j+k > (len(self.game.board_com) - 2):
                            obstructed = True
                            break
                    if not obstructed:
                        for k in range(n):
                            self.guess_board[i][j+k] += 1

        for i in range (1, len(self.game.board_com)-1):
            for j in range(1, len(self.game.board_com[i])-1):
                if self.game.board_com[i][j] not in ["G", "D"]:
                    obstructed_2 = False
                    for k in range(1, n):
                        if self.game.board_com[i+k][j] in ["G", "D"] or i+k > (len(self.game.board_com) - 2):
                            obstructed_2 = True
                            break
                    if not obstructed_2:
                        for k in range(n):
                            self.guess_board[i+k][j] += 1

    def guess(self, board):
        max_list = []
        max_all = 0
        self.pos_guess = []
        self.mode = self.game.style
        print("self.mode: ", self.mode)

        

        if self.mode == "statistical":
            self.guess_board = []
            for i in range(len(self.game.board_com)):
                self.guess_board.append([0 for j in range(len(self.game.board_com))])

            for k in self.game.player_ships:
                self.statistical_guess(k)

            for i in range(len(self.guess_board)):
                max_list.append(max(self.guess_board[i]))
                max_all = max(max_list)

            for i in range(len(self.guess_board)):
                for j in range(len(self.guess_board)):
                    if self.guess_board[i][j] == max_all:
                        self.pos_guess.append([i,j])

            pos = randint(0, len(self.pos_guess) - 1)
            self.guess_coords = self.pos_guess[pos]
            self.game.guess_ship(self.guess_coords[0], self.guess_coords[1], board)
            print(self.guess_coords)
            print()
            print("self.hit: ")
            print(self.hit)

        elif self.mode == "hit":
            self.hit_guess()
            self.game.guess_ship(self.guess_coords[0], self.guess_coords[1], board)

        for row in self.guess_board:
            print(str(row))