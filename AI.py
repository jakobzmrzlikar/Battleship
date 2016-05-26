import time
from random import randint

class AI:
    def __init__(self, game):
        self.game = game
        self.mode = "statistical"
        self.hit = 0
        self.wrong_dir = False
        self.compass = None


    def statistical_guess(self, n):
        self.mode = self.game.style

        if self.mode == "hit":
            self.hit = self.game.hit
            self.previous_miss = self.game.previous_miss
            self.hit_coords = self.game.hit_coords

            #če je prej zadel(je na pravi premici)
            if self.hit >= 2:
                #če je v tej smeri še prostor
                if not self.wrong_dir:
                   self.guess_coords = [self.guess_coords[0] + self.compass[0], self.guess_coords[-1] + self.compass[-1]]
                   #če je naslednji že zaseden
                   if self.game.board_com[self.guess_coords[0], self.guess_coords[-1]] in ["G", "H", "D"]:
                        self.wrong_dir = True
                        self.guess_coords = [self.hit_coords[0] - compass[0], self.hit_coords[-1] - compass[-1]]
                #če v tej smeri ni več prostora (ampak je na pravi premici) gre v nasprotno smer
                elif self.wrong_dir:
                    #če je prejšnjo zgrešil se nanaša na originalen zadetek
                    if self.previous_miss:
                        self.guess_coords = [self.hit_coords[0] - compass[0], self.hit_coords[-1] - compass[-1]]
                    #če je prejšnjo zadel se nanaša na prejšnjo
                    else:
                        self.guess_coords = [self.guess_coords[0] - compass[0], self.guess_coords[-1] - compass[-1]]
            #če prej v tej smeri ni zadel
            elif self.compass and self.game.board_com[self.hit_coords[0] + self.compass[0]][self.hit_coords[-1] + self.compass[-1]]:
                self.compass_array.remove(self.compass)
                print(self.compass_array)
                if len(self.compass_array) == 1:
                    self.compass = self.compass_array[0]
                else:   
                    self.compass = self.compass_array[randint(0, len(self.compass_array)-1)]
                self.guess_coords = [self.hit_coords[0] + self.compass[0], self.hit_coords[-1] + self.compass[-1]]
            #če je prvič zadel
            else:
                self.compass_array = [[0, 1], [0, -1], [1, 0], [-1, 0]]
                for i in self.compass_array:
                    if self.game.board_com[self.guess_coords[0]+i[0]][self.guess_coords[1]+i[-1]] in ["G", "H", "D"]:
                        self.compass_array.remove(i)
                    #here goes the hepler function :)
                if len(self.compass_array) == 1:
                    self.compass = self.compass_array[0]
                else:   
                    self.compass = self.compass_array[randint(0, len(self.compass_array)-1)]
                self.guess_coords = [self.guess_coords[0] + self.compass[0], self.guess_coords[-1] + self.compass[-1]]


        if self.mode == "statistical":
            for i in range (1, len(self.game.board_com)-1):
                for j in range(1, len(self.game.board_com[i])-1):
                    if self.game.board_com[i][j] not in ["G", "H", "D"]:
                        obstructed = False
                        for k in range(1, n):
                            if self.game.board_com[i][j+k] in ["G", "H", "D"] or j+k > (len(self.game.board_com) - 2):
                                obstructed = True
                                break
                        if not obstructed:
                            for k in range(n):
                                self.guess_board[i][j+k] += 1

            for i in range (1, len(self.game.board_com)-1):
                for j in range(1, len(self.game.board_com[i])-1):
                    if self.game.board_com[i][j] not in ["G", "H", "D"]:
                        obstructed_2 = False
                        for k in range(1, n):
                            if self.game.board_com[i+k][j] in ["G", "H", "D"] or i+k > (len(self.game.board_com) - 2):
                                obstructed_2 = True
                                break
                        if not obstructed_2:
                            for k in range(n):
                                self.guess_board[i+k][j] += 1

    def guess(self, board):
        self.guess_board = []
        max_list = []
        max_all = 0
        self.pos_guess = []

        # if self.mode == "random":
        for i in range(len(self.game.board_com)):
            self.guess_board.append([0 for j in range(len(self.game.board_com))])

        for k in self.game.player_ships:
            self.statistical_guess(k)

        for row in self.guess_board:
            print(str(row))
        print()

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
        

        # else:
            # pass            

