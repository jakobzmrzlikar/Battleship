import tkinter as tk
from add_ship_alpha import make_board, add_ship
import time

'''
S = ship
X = next to a ship and border
O = empty
H = hit
D = destroyed
'''

class Battleship:
    def __init__(self):
        self.board1 = make_board(10)
        self.board2 = make_board(10)
        for i in range(2, 6):
            add_ship(i, self.board1)
            add_ship(i, self.board2)
        add_ship(3, self.board1)
        add_ship(1, self.board1)
        add_ship(3, self.board2)
        add_ship(1, self.board2)

        self.num_ships_1 = 8
        self.num_ships_2 = 8

    def guess_ship(self, row, column, board):
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
                for i in range(1, 5):
                    if 0 in pos_direct:
                        cur_0.append(board[row][column - i])
                        if cur_0[-1] == "X":
                            pos_direct.remove(0)

                        elif cur_0[-1] == "S":
                            break

                    if 1 in pos_direct:
                        cur_1.append(board[row][column + i])
                        if cur_1[-1] == "X":
                            pos_direct.remove(1)

                        elif cur_1[-1] == "S":
                            break

                    if 2 in pos_direct:
                        cur_2.append(board[row - i][column])
                        if cur_2[-1] == "X":
                            pos_direct.remove(2)

                        elif cur_2[-1] == "S":
                            break

                    if 3 in pos_direct:
                        cur_3.append(board[row + i][column])
                        if cur_3[-1] == "X":
                            pos_direct.remove(3)

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

        # self.root.mainloop()

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
                    if board[i][j] == "S":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="deeppink")
                    elif board[i][j] == "H":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="orange")
                    elif board[i][j] == "D":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="red")
                    else:
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="blue")
        else:
            for i in range(1, len(board)-1):
                for j in range(1, len(board)-1):
                    if board[i][j] == "S":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="deeppink")
                    elif board[i][j] == "H":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="orange")
                    elif board[i][j] == "D":
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="red")
                    else:
                        self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="blue")

def main():
    game = Battleship()
    gui = GUI(game)
    while True:
        row_1 = int(input("Guess row: "))
        col_1 = int(input("Guess column: "))
        game.guess_ship(row_1, col_1, game.board1)
        
        if game.num_ships_2 == 0:
        	print("Player 1 wins!")
        	break

        row_2 = int(input("Guess row:"))
        col_2 = int(input("Guess column: "))
        game.guess_ship(row_2, col_2, game.board2)
        
        if game.num_ships_1 == 0:
        	print("Player 2 wins!")
        	break

start = time.time()
main()
end = time.time() - start
print("\n" + str(end) + "s")
