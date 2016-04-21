import tkinter as tk
from add_ship_alpha import make_board, add_ship
import time
import random

'''
S = ship
X = next to a ship and border
O = empty
H = hit
D = destroyed
'''

class Battleship:
    def __init__(self):
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

    def debug(self):
        for row in self.board1:
            print(" ".join(row))
        print(self.player)


    def guess(self, row, column):
        self.guess_ship(int(row), int(column), self.board1)
        print(row, column)
        if self.num_ships_1 == 0:
            print("Player 1 wins!")
            return 0

        self.guess_ship(random.randint(1,10), random.randint(1,10), self.board2)
        if self.num_ships_2 == 0:
            print("Player 2 wins!")
            return 0

    def guess_ship(self, row, column, board):
        print("Guessing", row, column, "for", self.player)
        if row > 10 or column > 10:
            print("Outside of the board!")
        else:
            if board[row][column] == "S":
                pos_direct = [0,1,2,3]
                cur_0 = []
                cur_1 = []
                cur_2 = []
                cur_3 = []

                # for i in range(1, max_ship_length):
                for i in range(1, 6):
                    if 0 in pos_direct:
                        cur_0.append(board[row][column - i])
                        if cur_0[-1] in ["X", "G"]:
                            pos_direct.remove(0)

                        elif cur_0[-1] == "S":
                            break

                    if 1 in pos_direct:
                        cur_1.append(board[row][column - i])
                        if cur_1[-1] in ["X", "G"]:
                            pos_direct.remove(0)

                        elif cur_1[-1] == "S":
                            break

                    if 2 in pos_direct:
                        cur_2.append(board[row][column - i])
                        if cur_2[-1] in ["X", "G"]:
                            pos_direct.remove(0)

                        elif cur_2[-1] == "S":
                            break

                    if 3 in pos_direct:
                        cur_3.append(board[row][column - i])
                        if cur_3[-1] in ["X", "G"]:
                            pos_direct.remove(0)

                        elif cur_3[-1] == "S":
                            break

                if len(pos_direct) > 0:
                    board[row][column] = "H"
                    print("Hit!")
                else:
                    print(cur_0, cur_1, cur_2, cur_3)
                    board[row][column] = "D"
                    for i in range(1, len(cur_0)):
                        if cur_0[i - 1] == "H":
                            board[row][column - i] = "D"
                            
                    for i in range(1, len(cur_1)):                        
                        if cur_1[i - 1] == "H":
                            board[row][column + i] = "D"

                    for i in range(1, len(cur_2)):         
                        if cur_2[i - 1] == "H":
                            board[row - i][column] = "D"

                    for i in range(1, len(cur_3)):        
                        if cur_3[i - 1] == "H":
                            board[row + i][column] = "D"
                            
                    print("Destroyed!")
                    
                    if board == self.board1:
                        self.num_ships_2 -= 1
                    else:
                        self.num_ships_1 -= 1

            elif board[row][column] in ["O", "X"]:
                board[row][column] = "G"
                print("Miss!")

            elif board[row][column] in ["H", "D"]:
                print("Already guessed there!")


class GUI:
    def __init__(self, game):
        self.root = tk.Tk()
        self.height, self.width = 360, 360
        self.grid = self.height / 12
        self.game = game

        self.map1 = tk.Canvas(self.root, height=self.height, width=self.width)
        self.map1.pack()

        self.map2 = tk.Canvas(self.root, height=self.height, width=self.width)
        self.map2.pack()

        self.load(self.game.board1, self.map1)
        self.load(self.game.board2, self.map2)

        frame = tk.Frame(self.root)
        self.label1 = tk.Label(frame, text="Ugibaj vrstico:")
        self.label2 = tk.Label(frame, text="Ugibaj stolpec:")
        self.entry_row = tk.Entry(frame)
        self.entry_col = tk.Entry(frame)
        self.button = tk.Button(frame, text="Guess", command=self.guess)
        self.debug = tk.Button(frame, text="debug", command=self.game.debug)

        frame.pack()
        self.label1.grid(row=0, column=0)
        self.entry_row.grid(row=0, column=1)
        self.label2.grid(row=1, column=0)
        self.entry_col.grid(row=1, column=1)
        self.button.grid(row=2, column=0)
        self.debug.grid(row=3, column=0)

        self.root.mainloop()

    def guess(self):
        if self.game.player:
            self.game.guess(self.entry_row.get(), self.entry_col.get())
            self.load(self.game.board1, self.map1)
            self.load(self.game.board2, self.map2)


    def load(self, board, map_num):
        self.map = map_num
        self.map.delete("all")
        for i in range(len(board)):
            self.map.create_line(0, i * self.grid, len(board) * self.grid, i * self.grid)
            self.map.create_line(i * self.grid, 0, i * self.grid, len(board) * self.grid)

        self.map.create_rectangle(0, 0, len(board) * self.grid, self.grid, fill="black")
        self.map.create_rectangle(0, 0, self.grid, len(board) * self.grid, fill="black")        
        self.map.create_rectangle(0, (len(board) - 1) * self.grid, len(board) * self.grid, len(board) * self.grid, fill="black")
        self.map.create_rectangle((len(board) - 1) * self.grid, 0, len(board) * self.grid, len(board) * self.grid, fill="black")

        if self.map == self.map1:
            for i in range(1, len(board)-1):
                for j in range(1, len(board)-1):
                    if board[j][i] == "H":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="orange")
                    elif board[j][i] == "D":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="red")
                    elif board[j][i] == "G":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="grey")
                    else:
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="blue")
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
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="grey")
                    else:
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="blue")

def main():
    game = Battleship()
    gui = GUI(game)

start = time.time()
main()
end = time.time() - start
print("\n" + str(end) + "s")
