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

class AI:
    def __init__(self, game):
        self.game = game
        self.mode = self.game.style


    def statistical_guess(self, n):
        

        if self.mode == "hit":
            #če je prej zadel(je na pravi premici)
            if self.game.hit > 2:
                #če je v tej smeri še prostor
                if not self.game.wrong_dir:
                    for i in range(2, 5):
                    #če naslednje polje ni prosto:
                        if self.game.board_com[self.guess_coords[0]+compass[0]*i, self.guess_coords[1]+compass[1]*i] in ["G", "H", "D"]:
                            self.game.wrong_dir = True
                            break
                        #če je naslednje polje prosto
                        else:
                            self.game.guess_ship(self.guess_coords[0]+compass[0]*i, self.guess_coords[1]+compass[1]*i, self.game.board_com)
                #če v tej smeri ni več prostora (ampak je na pravi premici) gre v nasprotno smer
                elif wrong_dir:
                    for i in range(2, 5):
                        self.game.guess_ship(self.guess_coords[0]-compass[0]*i, self.guess_coords[1]-compass[1]*i, self.game.board_com)
            #če prej v tej smeri ni zadel            
            else:
                compass_array = [[0, 1], [0, -1], [1, 0], [-1, 0]]
                for i in compass_array:
                    if self.game.board_com[self.guess_coords[0]+compass_array[i][0], self.guess_coords[1]+compass_array[i][1]] in ["G", "H", "D"]:
                        del(compass_array[i])    
                compass = compass_array[randint(0, len(compass_array)-1)]
                while len(compass_array) > 0:
                    self.game.guess_ship(self.guess_coords[0]+compass[0], self.guess_coords[1]+compass[1], self.game.board_com)



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

        else:
            pass

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


class Battleship:
    def __init__(self):
        # makes both boards, adds ships and sets some variables
        self.window = tk.Tk()
        self.game_end = False

        self.player = 1
        self.board_player = make_board(10)
        self.board_com = make_board(10)
        for i in range(2, 6):
            add_ship(i, self.board_player)
            add_ship(i, self.board_com)
        add_ship(3, self.board_player)
        add_ship(3, self.board_com)

        self.player_ships = [2,3,3,4,5]
        self.com_ships = [2,3,3,4,5]

        self.num_ships_player = len(self.player_ships)
        self.num_ships_com = len(self.com_ships)

        self.repeat_player = True
        self.repeat_com = True

        self.hit = 0
        self.wrong_dir = False
        self.style = "statistical"

    def restart_game(self):
        # it restarts the game
        self.end_screen.destroy()
        self.window.destroy()
        main()

    def quit_game(self):
        # it destroys both screens
        self.end_screen.destroy()
        self.window.destroy()

    def game_over(self, winner):
        # makes the end screen and all the text + buttons
        self.end_screen = tk.Tk()
        game_end = True
        self.repeat_com = False

        if winner:
            end_text = tk.Label(self.end_screen, text="Player 1 wins!", font=("Helvetica", 16))
        else:
            end_text = tk.Label(self.end_screen, text="The computer wins!", font=("Helvetica", 16))

        restart = tk.Button(self.end_screen, text="Yes!", command=self.restart_game)
        quit = tk.Button(self.end_screen, text="No!", command=self.quit_game)
        text = tk.Label(self.end_screen, text="Do you want to play again?")

        end_text.pack()
        text.pack(side=tk.LEFT)
        restart.pack(side=tk.LEFT)
        quit.pack(side=tk.LEFT)

    def guess_player(self, row, column):
        # calls guess_ship for the player and checks the victory condition
        self.guess_ship(int(row), int(column), self.board_player)
        if self.num_ships_com == 0:
            self.game_over(1)

    def guess_ship(self, row, column, board):
        # checks if the guessed tile is inside the board
        if not(row > 10 or column > 10):

            # it finds an S tile and you have another turn after this one
            if board[row][column] == "S":

                pos_direct = [0,1,2,3]
                cur_0 = []
                cur_1 = []
                cur_2 = []
                cur_3 = []
                count = 0
                ship_len = 0

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
                        #self.style = "random"

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
                                board[row - 1][column + i] = "G"
                                board[row][column + i] = "D"
                                board[row + 1][column + i] = "G"                         

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

                        # it decreases the number of ships on the board and removes the ship from the list of ships
                        if board == self.board_player:
                            len_ship = 1 + (len(cur_0) - 1) + (len(cur_1) - 1) + (len(cur_2) - 1) + (len(cur_3) - 1)
                            self.num_ships_com -= 1
                            self.com_ships.remove(len_ship)
                        else:
                            len_ship = 1 + (len(cur_0) - 1) + (len(cur_1) - 1) + (len(cur_2) - 1) + (len(cur_3) - 1)
                            self.num_ships_player -= 1
                            self.player_ships.remove(len_ship)

                        break

                # if it found another S tile, than the guessed tile becomes an H tile
                if len(pos_direct) > 0:
                    board[row][column] = "H"
                    #self.style = "ship"
                    self.style = "hit"
                    self.hit += 1

            # if the guessed tile was not a ship, it changes it into a G tile and it's the opponent's turn
            elif board[row][column] in ["O", "X"]:
                board[row][column] = "G"
                self.repeat_player = False
                self.repeat_com = False

                if self.hit > 2:
                    self.wrong_dir = True
                self.hit = 0

            # if the guessed tile was previously guessed, it warns the player
            elif board[row][column] in ["H", "D", "G"]:
                pass


class GUI:
    def __init__(self, game, AI):
        # sets the window and tile size
        self.height, self.width = 360, 360
        self.grid = self.height / 12
        self.game = game
        self.root = self.game.window
        self.AI = AI

        # makes a canvas for each board and loads the board
        self.map_player = tk.Canvas(self.root, height=self.height, width=self.width)
        self.map_player.bind("<Button-1>", self.mouse_guess)
        self.map_player.grid(row=0, column=0)

        self.map_com = tk.Canvas(self.root, height=self.height, width=self.width)
        self.map_com.grid(row=1, column=0)

        self.load_map(self.game.board_player, self.map_player)
        self.load_map(self.game.board_com, self.map_com)

        # makes 2 boxes for the remaining ships
        frame = tk.Frame(self.root)
        player_text = tk.Label(frame, text="Player's remaining ships:")
        self.player_list = tk.Listbox(frame)
        com_text = tk.Label(frame, text="Opponent's remaining ships:")
        self.com_list = tk.Listbox(frame)

        frame.grid(row=0, column=1)
        player_text.pack()
        self.player_list.pack()
        com_text.pack()
        self.com_list.pack()

        self.update_list(self.game.player_ships, self.game.com_ships)

        self.root.mainloop()

    def update_list(self, player, computer):
        # updates the remaining ships
        self.player_list.delete(0, tk.END)
        self.com_list.delete(0, tk.END)

        for i in player:
            self.player_list.insert(tk.END, i)

        for i in computer:
            self.com_list.insert(tk.END, i)        

    def mouse_guess(self, event):
        if not self.game.game_end:
            mouse_row = int(event.y / self.grid) 
            mouse_col = int(event.x / self.grid)

            # it calls the game's guess function with the row and column based on the position of the mouse click
            self.game.guess_player(mouse_row, mouse_col)
            self.update_list(self.game.player_ships, self.game.com_ships)         

            # if it's your turn, the computer can't guess
            if not self.game.repeat_player:
                self.game.repeat_com = True

                # the computer guesses until it's no longer his turn
                while self.game.repeat_com:
                    self.AI.guess(self.game.board_com)
                    self.AI.mode = self.game.style
                    time.sleep(0.05)

                self.update_list(self.game.player_ships, self.game.com_ships)    
                self.game.repeat_player = True

            # it reloads both boards
            self.load_map(self.game.board_player, self.map_player)
            self.load_map(self.game.board_com, self.map_com)

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
        if self.map == self.map_player:
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


def main():
    # it initiates the game
    game = Battleship()
    ai = AI(game)
    gui = GUI(game, ai)


start = time.time()  

main()

end = time.time() - start
print("\n" + str(end) + "s")
