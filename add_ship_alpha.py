from random import randint

size = []

def make_board(a):
	board = []

	rows = columns = a

	size.append(rows)
	size.append(columns)

	if rows < 5:
		rows = 5
	if columns < 5:
		columns = 5

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

	dic = {
	0: [0, -1],
	1: [0, 1],
	2: [-1, 0],
	3: [1, 0]
	}

	space = 0
	exit = False

	while not exit:
		ship_beg_row = ship_row = randint(0, rows - 1)
		ship_beg_col = ship_col = randint(0, columns - 1)
		ship_beg_direction = ship_direction = randint(0,3)

		if board[ship_row][ship_col] == "O":
			for i in range(1, n):
				if board[ship_row + i * dic[ship_direction][0]][ship_col + i * dic[ship_direction][1]] == "X":
					space += i
					for j in range(n - 1 - space):
						if board[ship_row - j * dic[ship_direction][0]][ship_col - j * dic[ship_direction][1]] == "X":
							'''
							FIX HERE!
											    ____________________________
							   _____                          ,\\    ___________________    \
							  |     `------------------------'  ||  (___________________)   `|
							  |_____.------------------------._ ||  ____________________     |
							                                  `//__(____________________)___/

							'''
							break

					for k in range(n):
						board[ship_row + (space - k) * dic[ship_direction][0]] \
						[ship_col + (space - k) * dic[ship_direction][1]] = "S"

						board[ship_row + (space - k) * dic[ship_direction][0] + dic[ship_direction][1]] \
						[ship_col + (space - k) * dic[ship_direction][1] + dic[ship_direction][0]] = "X"

						board[ship_row + (space - k) * dic[ship_direction][0] - dic[ship_direction][1]] \
						[ship_col + (space - k) * dic[ship_direction][1] - dic[ship_direction][0]] = "X"

					board[ship_row + (space + 1) * dic[ship_direction][0]] \
					[ship_col + (space + 1) * dic[ship_direction][1]] = "X"

					board[ship_row + (space - n) * dic[ship_direction][0]] \
					[ship_col + (space - n) * dic[ship_direction][1]] = "X"

					exit = True
					break
					
			for k in range(n):
				board[ship_row - k * dic[ship_direction][0]] \
				[ship_col - k * dic[ship_direction][1]] = "S"

				board[ship_row - k * dic[ship_direction][0] + dic[ship_direction][1]] \
				[ship_col - k * dic[ship_direction][1] + dic[ship_direction][0]] = "X"

				board[ship_row - k * dic[ship_direction][0] - dic[ship_direction][1]] \
				[ship_col - k * dic[ship_direction][1] - dic[ship_direction][0]] = "X"

			board[ship_row + dic[ship_direction][0]] \
			[ship_col + dic[ship_direction][1]] = "X"

			board[ship_row - n * dic[ship_direction][0]] \
			[ship_col - n * dic[ship_direction][1]] = "X"

			exit = True
