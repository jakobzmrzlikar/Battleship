import tkinter as tk
from add_ship import make_board, add_ship
import time
from random import randint

'''
S = ship tile
X = tile next to a ship and border
O = empty tile
H = hit ship tile
D = destroyed ship tile
G = guessed tile
'''

class Battleship:
    def __init__(self):
        # makes both boards and adds ships
        self.player = 1
        self.board1 = make_board(10)
        self.board2 = make_board(10)
        for i in range(2, 6):
            add_ship(i, self.board1)
            add_ship(i, self.board2)
        add_ship(3, self.board1)
        add_ship(1, self.board1)
        add_ship(3, self.board2)
        add_ship(1, self.board2)

        self.num_ships_1 = 7
        self.num_ships_2 = 7

        self.repeat_player = True
        self.repeat_com = True

    def debug(self):
        # we should do something usefull here
        pass


    def guess_player(self, row, column):
        # calls guess_ship for the player and checks the victory condition
        self.guess_ship(int(row), int(column), self.board1)
        if self.num_ships_1 == 0:
            print("Player 1 wins!")
            return 0

    def guess_com(self):
        # calls guess_ship for the computer and checks the victory condition
        self.guess_ship(randint(1,10), randint(1,10), self.board2)
        if self.num_ships_2 == 0:
            print("Player 2 wins!")
            return 0

    def guess_ship(self, row, column, board):
        # checks if the guessed tile is inside the board
        if row > 10 or column > 10:
            print("Outside of the board!")

        else:
            # it finds an S tile and you have another turn after this one
            if board[row][column] == "S":
                pos_direct = [0,1,2,3]
                cur_0 = []
                cur_1 = []
                cur_2 = []
                cur_3 = []
                count = 0

                # it looks in all directions for another S tile
                # if it finds an X or a G tile, it no longer cheks that direction
                while True:
                    count += 1

                    if 0 in pos_direct:
                        cur_0.append(board[row][column - count])
                        if cur_0[-1] in ["X", "G"]:
                            pos_direct.remove(0)

                        elif cur_0[-1] == "S":
                            break

                    if 1 in pos_direct:
                        cur_1.append(board[row][column + count])
                        if cur_1[-1] in ["X", "G"]:
                            pos_direct.remove(1)

                        elif cur_1[-1] == "S":
                            break

                    if 2 in pos_direct:
                        cur_2.append(board[row - count][column])
                        if cur_2[-1] in ["X", "G"]:
                            pos_direct.remove(2)

                        elif cur_2[-1] == "S":
                            break

                    if 3 in pos_direct:
                        cur_3.append(board[row + count][column])
                        if cur_3[-1] in ["X", "G"]:
                            pos_direct.remove(3)

                        elif cur_3[-1] == "S":
                            break

                    # if there is no connected S tiles, it goes and changes all the connected H tiles into D tiles and draws a border of G tiles
                    if len(pos_direct) == 0:

                        board[row - 1][column] = "G"
                        board[row + 1][column] = "G"

                        board[row][column - 1] = "G"
                        board[row][column + 1] = "G"

                        board[row][column] = "D"

                        for i in range(1, len(cur_0)):
                            if cur_0[i - 1] == "H":
                                board[row - 1][column - i] = "G"
                                board[row][column - i] = "D"
                                board[row + 1][column - i] = "G"                               
                                
                        for i in range(1, len(cur_1)):                        
                            if cur_1[i - 1] == "H":
                                board[row - 1][column - i] = "G"
                                board[row][column + i] = "D"
                                board[row + 1][column - i] = "G"                         

                        for i in range(1, len(cur_2)):         
                            if cur_2[i - 1] == "H":
                                board[row - i][column - 1] = "G"
                                board[row - i][column] = "D"
                                board[row - i][column + 1] = "G"                              
                
                        for i in range(1, len(cur_3)):        
                            if cur_3[i - 1] == "H":
                                board[row + i][column - 1] = "G"
                                board[row + i][column] = "D"
                                board[row + i][column + 1] = "G"

                        board[row - 1][column - len(cur_0)] = "G"       
                        board[row][column - len(cur_0)] = "G"
                        board[row + 1][column - len(cur_0)] = "G"

                        board[row - 1][column + len(cur_1)] = "G"
                        board[row][column + len(cur_1)] = "G"
                        board[row + 1][column + len(cur_1)] = "G"

                        board[row - len(cur_2)][column - 1] = "G"
                        board[row - len(cur_2)][column] = "G"
                        board[row - len(cur_2)][column + 1] = "G"

                        board[row + len(cur_3)][column - 1] = "G"
                        board[row + len(cur_3)][column] = "G"
                        board[row + len(cur_3)][column + 1] = "G"

                        # it decreases the number of ships on the board
                        if board == self.board1:
                            self.num_ships_2 -= 1
                        else:
                            self.num_ships_1 -= 1

                        print("Destroyed!")
                        break

                # if it found another S tile, than the guessed tile becomes an H tile
                if len(pos_direct) > 0:
                    board[row][column] = "H"
                    print("Hit!") 

            # if the guessed tile was not a ship, it changes it into a G tile and it's the opponent's turn
            elif board[row][column] in ["O", "X"]:
                board[row][column] = "G"
                self.repeat_player = False
                self.repeat_com = False
                print("Miss!")


            # if the guessed tile was previously guessed, it warns the player
            elif board[row][column] in ["H", "D", "G"]:
                print("Already guessed there!")


class GUI:
    def __init__(self, game):
        # sets the window and tile size
        self.root = tk.Tk()
        self.height, self.width = 360, 360
        self.grid = self.height / 12
        self.game = game

        # makes a canvas for each board and loads the board
        self.map1 = tk.Canvas(self.root, height=self.height, width=self.width)
        self.map1.pack()

        self.map2 = tk.Canvas(self.root, height=self.height, width=self.width)
        self.map2.pack()

        self.load_map(self.game.board1, self.map1)
        self.load_map(self.game.board2, self.map2)

        # makes a frame for all the buttons and guessing mechanism
        frame = tk.Frame(self.root)
        self.label1 = tk.Label(frame, text="Ugibaj vrstico:")
        self.label2 = tk.Label(frame, text="Ugibaj stolpec:")
        self.entry_row = tk.Entry(frame)
        self.entry_col = tk.Entry(frame)
        self.button = tk.Button(frame, text="Guess", command=self.call_guess)
        self.debug = tk.Button(frame, text="Useless", state=tk.DISABLED, command=game.debug)

        frame.pack()
        self.label1.grid(row=0, column=0)
        self.entry_row.grid(row=0, column=1)
        self.label2.grid(row=1, column=0)
        self.entry_col.grid(row=1, column=1)
        self.button.grid(row=2, column=0)
        self.debug.grid(row=3, column=0)

        self.root.mainloop()

    def call_guess(self):
        # it calls the game's guess function with the numbers in the entries
        self.game.guess_player(self.entry_row.get(), self.entry_col.get())

        # if it's your turn, the computer can't guess
        if not self.game.repeat_player:
            self.game.repeat_com = True

            # the computer guesses until it's no longer his turn
            while self.game.repeat_com:
                self.game.guess_com()

            self.game.repeat_player = True

        else:
            print("You have another guess!")

        # it reloads both boards
        self.load_map(self.game.board1, self.map1)
        self.load_map(self.game.board2, self.map2)


    def load_map(self, board, map_num):
        # it deletes the entire canvas
        self.map = map_num
        self.map.delete("all")

        #it draws the background
        self.map.create_rectangle(0, 0, len(board) * self.grid, len(board) * self.grid, fill="blue")

        # it draws the tile grid
        for i in range(len(board)):
            self.map.create_line(0, i * self.grid, len(board) * self.grid, i * self.grid)
            self.map.create_line(i * self.grid, 0, i * self.grid, len(board) * self.grid)

        # it draws the border
        self.map.create_rectangle(0, 0, len(board) * self.grid, self.grid, fill="black")
        self.map.create_rectangle(0, 0, self.grid, len(board) * self.grid, fill="black")        
        self.map.create_rectangle(0, (len(board) - 1) * self.grid, len(board) * self.grid, len(board) * self.grid, fill="black")
        self.map.create_rectangle((len(board) - 1) * self.grid, 0, len(board) * self.grid, len(board) * self.grid, fill="black")

        # it doesn't draw the S tiles on the computer's board, so that the player can't cheat
        if self.map == self.map1:
            for i in range(1, len(board)-1):
                for j in range(1, len(board)-1):
                    if board[j][i] == "H":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="orange")
                    elif board[j][i] == "D":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="red")
                    elif board[j][i] == "G":
                        self.map.create_line(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, width=2)
                        self.map.create_line((i + 1) * self.grid, j * self.grid, i * self.grid, (j + 1) * self.grid, width=2)
                    
        else:
            for i in range(1, len(board)-1):
                for j in range(1, len(board)-1):
                    if board[j][i] == "S":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="deeppink")
                    elif board[j][i] == "H":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="orange")
                    elif board[j][i] == "D":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="red")
                    elif board[j][i] == "G":
                        self.map.create_line(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, width=2)
                        self.map.create_line((i + 1) * self.grid, j * self.grid, i * self.grid, (j + 1) * self.grid, width=2)

# it initiates the game
start = time.time()

game = Battleship()
gui = GUI(game)

end = time.time() - start
print("\n" + str(end) + "s")