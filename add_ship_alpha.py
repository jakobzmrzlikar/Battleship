from random import randint

size = []

def make_board(a):
	board = []

	rows = columns = a

	if rows < 5:
		rows = 5
	if columns < 5:
		columns = 5

	size.append(rows + 2)
	size.append(columns + 2)

	board.append(["X"] * (columns))
	for i in range(rows):
		board.append(["O"] * columns)
		board[i].insert(0, "X")
		board[i].append("X")
	board[rows].insert(0, "X")
	board[rows].append("X")
	board.append(["X"] * (columns + 2))

	return board

def add_ship(n, board):

	rows = size[0]
	columns = size[1]

	dic = [[0, -1], [0, 1], [-1, 0], [1, 0]]

	
	exit = False

	while not exit:
		space = 0
		no_space = False
		bound = False

		ship_row = randint(0, rows - 1)
		ship_col = randint(0, columns - 1)
		ship_direction = randint(0,3)

		if board[ship_row][ship_col] == "O":
			for i in range(1, n):
				if board[ship_row + i * dic[ship_direction][0]][ship_col + i * dic[ship_direction][1]] == "X":
					space += (i - 1)
					bound = True
					for j in range(n - 1 - space):
						if board[ship_row - j * dic[ship_direction][0]][ship_col - j * dic[ship_direction][1]] == "X":
							no_space = True
							break

					if no_space:
						break

					for k in range(n):
						# ko je smer 3, začne risat navzdol in se teleportira čez rob
						board[ship_row + (space - k) * dic[ship_direction][0]] \
						[ship_col + (space - k) * dic[ship_direction][1]] = "S"

						board[ship_row + (space - k) * dic[ship_direction][0] + dic[ship_direction][1]] \
						[ship_col + (space - k) * dic[ship_direction][1] + dic[ship_direction][0]] = "X"

						board[ship_row + (space - k) * dic[ship_direction][0] - dic[ship_direction][1]] \
						[ship_col + (space - k) * dic[ship_direction][1] - dic[ship_direction][0]] = "X"

					# ne izriše X v kotih ladje	
					board[ship_row + (space + 1) * dic[ship_direction][0]] \
					[ship_col + (space + 1) * dic[ship_direction][1]] = "X"

					board[ship_row + (space - n) * dic[ship_direction][0]] \
					[ship_col + (space - n) * dic[ship_direction][1]] = "X"

					exit = True
					break

			if not bound:
				for k in range(n):
					# tu dobi out of range, če je smer 2 in ne najde X
					board[ship_row - (k * dic[ship_direction][0])] \
					[ship_col + (k * dic[ship_direction][1])] = "S"

					board[ship_row - (k * dic[ship_direction][0]) + dic[ship_direction][1]] \
					[ship_col + (k * dic[ship_direction][1]) + dic[ship_direction][0]] = "X"

					board[ship_row - (k * dic[ship_direction][0]) - dic[ship_direction][1]] \
					[ship_col + (k * dic[ship_direction][1]) - dic[ship_direction][0]] = "X"

				# včasih napiše X na sredino ladje, ker ne gledava dolžine
				board[ship_row + dic[ship_direction][0]] \
				[ship_col + dic[ship_direction][1]] = "X"

				board[ship_row - dic[ship_direction][0]] \
				[ship_col - dic[ship_direction][1]] = "X"

				# ne izriše X v kotih ladje
				exit = True
