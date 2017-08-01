import tkinter as tk
import time

class GUI:
    def __init__(self, game, AI):
        self.game = game
        self.AI = AI

        # sets the window and tile size
        self.height, self.width = 396, 396
        self.grid = self.height / 12
        self.root = self.game.window

        # makes a canvas for each board and loads the board
        self.make_canvas()

        # makes 2 boxes for the remaining ships
        self.make_listbox()

        self.root.mainloop()

    def make_canvas(self):
        self.map_player = tk.Canvas(self.root, height=self.height, width=self.width)
        self.map_player.bind('<Button-1>', self.mouse_guess)
        self.map_player.grid(row=0, column=0)

        self.map_com = tk.Canvas(self.root, height=self.height, width=self.width)
        self.map_com.grid(row=1, column=0)

        self.load_map(self.game.board_player, self.map_player)
        self.load_map(self.game.board_com, self.map_com)

    def make_listbox(self):
        frame = tk.Frame(self.root)
        frame.grid(row=0, column=1)

        player_text = tk.Label(frame, text='Player\'s remaining ships:')
        com_text = tk.Label(frame, text='Opponent\'s remaining ships:')
        self.player_list = tk.Listbox(frame)
        self.com_list = tk.Listbox(frame)
        
        player_text.pack()
        self.player_list.pack()

        com_text.pack()
        self.com_list.pack()

        self.update_list(self.game.player_ships, self.game.com_ships)

    def update_list(self, player_ships, computer_ships):
        # updates the remaining ships
        self.player_list.delete(0, tk.END)
        self.com_list.delete(0, tk.END)

        for i in player_ships:
            self.player_list.insert(tk.END, i)

        for i in computer_ships:
            self.com_list.insert(tk.END, i)        

    def mouse_guess(self, event):
        if not self.game.game_end:
            mouse_row = int(event.y // self.grid) 
            mouse_col = int(event.x // self.grid)

            # it calls the game's guess function with the row and column based on the position of the mouse click
            self.game.guess_ship(mouse_row, mouse_col, self.game.board_player)
            self.update_list(self.game.player_ships, self.game.com_ships)         

            # if it's your turn, the computer can't guess
            if not self.game.repeat_player:
                self.game.repeat_com = True

                # the computer guesses until it's no longer his turn
                while self.game.repeat_com:
                    self.AI.guess()
                self.update_list(self.game.player_ships, self.game.com_ships)    
                self.game.repeat_player = True

            # it reloads both boards
            self.load_map(self.game.board_player, self.map_player)
            self.load_map(self.game.board_com, self.map_com)

    def load_map(self, board, map):
        # it deletes the entire map
        self.map = map
        self.map.delete('all')

        #it draws the background
        self.map.create_rectangle(0, 0, len(board) * self.grid, len(board) * self.grid, fill='blue')

        # it draws the tile grid
        for i in range(len(board)):
            self.map.create_line(0, i * self.grid, len(board) * self.grid, i * self.grid)
            self.map.create_line(i * self.grid, 0, i * self.grid, len(board) * self.grid)

        # it draws the border
        self.map.create_rectangle(0, 0, len(board) * self.grid, self.grid, fill='black')
        self.map.create_rectangle(0, 0, self.grid, len(board) * self.grid, fill='black')

        self.map.create_rectangle(0, (len(board) - 1) * self.grid,
                                  len(board) * self.grid, len(board) * self.grid, fill='black')

        self.map.create_rectangle((len(board) - 1) * self.grid, 0,
                                   len(board) * self.grid, len(board) * self.grid, fill='black')

        # it doesn't draw the S tiles on the computer's board, so that the player can't cheat
        if self.map == self.map_player:
            for i in range(1, len(board)-1):
                for j in range(1, len(board)-1):
                    if board[j][i] == 'G':
                        self.map.create_line(i * self.grid, j * self.grid,
                                            (i + 1) * self.grid, (j + 1) * self.grid, width=2)

                        self.map.create_line((i + 1) * self.grid, j * self.grid,
                                              i * self.grid, (j + 1) * self.grid, width=2)
                        continue

                    elif board[j][i] == 'H': colour = 'orange'
                    elif board[j][i] == 'D': colour = 'red'
                    else: continue

                    self.map.create_rectangle(i * self.grid, j * self.grid,
                                             (i + 1) * self.grid, (j + 1) * self.grid, fill=colour)

        else:
            for i in range(1, len(board)-1):
                for j in range(1, len(board)-1):
                    if board[j][i] == 'G':
                        self.map.create_line(i * self.grid, j * self.grid,
                                            (i + 1) * self.grid, (j + 1) * self.grid, width=2)

                        self.map.create_line((i + 1) * self.grid, j * self.grid,
                                              i * self.grid, (j + 1) * self.grid, width=2)
                        continue

                    if board[j][i] == 'S': colour = 'deeppink'
                    elif board[j][i] == 'H': colour = 'orange'
                    elif board[j][i] == 'D': colour = 'red'
                    else: continue

                    self.map.create_rectangle(i * self.grid, j * self.grid,
                                             (i + 1) * self.grid, (j + 1) * self.grid, fill=colour)