import tkinter as tk
from add_ship_alpha import make_board, add_ship
import time

start = time.time()

class Battleship:

	def __init__(self):
		self.board1 = make_board(10)
		self.board2 = make_board(10)
		for i in range(2, 6):
			add_ship(i, self.board1)
			add_ship(i, self.board2)
		add_ship(3, self.board1)
		add_ship(4, self.board1)
		add_ship(3, self.board2)
		add_ship(4, self.board2)

class GUI:

	def __init__(self, game):
		self.root = tk.Tk()
		self.height = 480
		self.width = 480
		self.grid = 40
		self.game = game

		self.map1 = tk.Canvas(self.root, height=self.height, width=self.width)
		self.map1.pack()

		self.map2 = tk.Canvas(self.root, height=self.height, width=self.width)
		self.map2.pack()

		self.load(self.game.board1, self.map1)
		self.load(self.game.board2, self.map2)

		self.root.mainloop()

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
					else:
						self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="blue")
		else:
			for i in range(1, len(board)-1):
				for j in range(1, len(board)-1):
					if board[i][j] == "S":
						self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="deeppink")
					else:
						self.map.create_rectangle(i * self.grid, j * self.grid, (i + 1) * self.grid, (j + 1) * self.grid, fill="blue")


if __name__ == "__main__":
	game = Battleship()
	gui = GUI(game)
	end = time.time() - start
	print("\n" + str(end) + "s")