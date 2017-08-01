import tkinter as tk
from add_ship import add_ship, make_board

from GUI import GUI
from AI import AI

def lazy_main():
    game = Game()
    ai = AI(game)
    gui = GUI(game, ai)

class Game:
    def __init__(self):
        # makes both boards, adds ships and sets some variables
        self.window = tk.Tk()
        self.window.title("Battleship")
        self.game_end = False

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
        self.style = 'statistical'
        self.previous_miss = False

    def restart_game(self):
        # it restarts the game
        self.end_screen.destroy()
        self.window.destroy()
        lazy_main()

    def quit_game(self):
        # it destroys both screens
        self.end_screen.destroy()
        self.window.destroy()

    def game_over(self, winner):
        # makes the end screen and all the text + buttons
        self.end_screen = tk.Tk()
        self.game_end = True
        self.repeat_com = False

        if winner == 'player':
            end_text = tk.Label(self.end_screen, text='Player 1 wins!', font=('Helvetica', 16))
        else:
            end_text = tk.Label(self.end_screen, text='The computer wins!', font=('Helvetica', 16))

        text = tk.Label(self.end_screen, text='Do you want to play again?')
        restart = tk.Button(self.end_screen, text='Yes!', command=self.restart_game)
        quit = tk.Button(self.end_screen, text='No!', command=self.quit_game)

        end_text.pack()
        text.pack(side=tk.LEFT)
        restart.pack(side=tk.LEFT)
        quit.pack(side=tk.LEFT)

    def guess_ship(self, row, column, board):
        # checks if the guessed tile is inside the board
        if 11 > row > 0 or 11 > column > 0:

            # if the guessed tile was not a ship, it changes it into a G tile and it's the opponent's turn
            if board[row][column] in ['O', 'X']:
                board[row][column] = 'G'
                self.repeat_player = False
                self.repeat_com = False

                if board == self.board_com:
                    if self.hit >= 2:
                        self.wrong_dir = True
                        self.previous_miss = True

            # it finds an S tile and you have another turn after this one
            elif board[row][column] == 'S':

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
                        if cur_0[-1] in ['X', 'G']:
                            pos_direct.remove(0)

                        elif cur_0[-1] == 'S':
                            break

                    if 1 in pos_direct:
                        cur_1.append(board[row][column + count])
                        if cur_1[-1] in ['X', 'G']:
                            pos_direct.remove(1)

                        elif cur_1[-1] == 'S':
                            break

                    if 2 in pos_direct:
                        cur_2.append(board[row - count][column])
                        if cur_2[-1] in ['X', 'G']:
                            pos_direct.remove(2)

                        elif cur_2[-1] == 'S':
                            break

                    if 3 in pos_direct:
                        cur_3.append(board[row + count][column])
                        if cur_3[-1] in ['X', 'G']:
                            pos_direct.remove(3)

                        elif cur_3[-1] == 'S':
                            break

                    # if there is no connected S tiles, it goes and changes all the connected H tiles into D tiles and draws a border of G tiles
                    if len(pos_direct) == 0:
                        board[row - 1][column] = 'G'
                        board[row + 1][column] = 'G'
                        board[row][column - 1] = 'G'
                        board[row][column + 1] = 'G'

                        board[row][column] = 'D'

                        for i in range(1, len(cur_0)):
                            if cur_0[i - 1] == 'H':
                                board[row - 1][column - i] = 'G'
                                board[row][column - i] =     'D'
                                board[row + 1][column - i] = 'G'

                        for i in range(1, len(cur_1)):
                            if cur_1[i - 1] == 'H':
                                board[row - 1][column + i] = 'G'
                                board[row][column + i] =     'D'
                                board[row + 1][column + i] = 'G'

                        for i in range(1, len(cur_2)):
                            if cur_2[i - 1] == 'H':
                                board[row - i][column - 1] = 'G'
                                board[row - i][column] =     'D'
                                board[row - i][column + 1] = 'G'

                        for i in range(1, len(cur_3)):
                            if cur_3[i - 1] == 'H':
                                board[row + i][column - 1] = 'G'
                                board[row + i][column] =     'D'
                                board[row + i][column + 1] = 'G'

                        board[row - 1][column - len(cur_0)] = 'G'
                        board[row][column - len(cur_0)] =     'G'
                        board[row + 1][column - len(cur_0)] = 'G'

                        board[row - 1][column + len(cur_1)] = 'G'
                        board[row][column + len(cur_1)] =     'G'
                        board[row + 1][column + len(cur_1)] = 'G'

                        board[row - len(cur_2)][column - 1] = 'G'
                        board[row - len(cur_2)][column] =     'G'
                        board[row - len(cur_2)][column + 1] = 'G'

                        board[row + len(cur_3)][column - 1] = 'G'
                        board[row + len(cur_3)][column] =     'G'
                        board[row + len(cur_3)][column + 1] = 'G'

                        # it decreases the number of ships on the board and removes the ship from the list of ships
                        if board == self.board_player:
                            len_ship = 1 + len(cur_0) + len(cur_1) + len(cur_2) + len(cur_3) - 4
                            self.num_ships_com -= 1
                            self.com_ships.remove(len_ship)

                            if self.num_ships_com == 0:
                                self.game_over('player')
                        else:
                            len_ship = 1 + len(cur_0) + len(cur_1) + len(cur_2) + len(cur_3) - 4
                            self.num_ships_player -= 1
                            self.player_ships.remove(len_ship)

                            if self.num_ships_player == 0:
                                self.game_over('cpu')

                            self.hit = 0
                            self.wrong_dir = False
                            self.style = 'statistical'
                            self.previous_miss = False

                        break

                # if it found another S tile, than the guessed tile becomes an H tile
                if len(pos_direct) > 0:
                    board[row][column] = 'H'

                    if self.hit == 0 and not self.wrong_dir:
                        self.hit_coords = [row, column]
                    if board == self.board_com:
                        self.style = 'hit'
                        self.hit += 1
                        self.previous_miss = False
