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

	for i in range(rows):
		board.append(["O"] * columns)

	return board


def add_ship(n, board):

	rows = size[0]
	columns = size[1]

	if n > rows and n > columns:
		return False

	ship_beg_row = ship_row = randint(0, rows - 1)
	ship_beg_col = ship_col = randint(0, columns - 1)

	ship_beg_direction = ship_direction = randint(0,3)

	'''
	0 = levo
	1 = desno
	2 = gor
	3 = dol
	'''
	print(ship_row + 1, ship_col + 1, ship_direction)

	board[ship_row][ship_col] = "S"

	if board[min(ship_row + 1, rows- 1)][min(ship_col + 1, columns - 1)] != "S":
				board[min(ship_row + 1, rows- 1)][min(ship_col + 1, columns - 1)] = "X"

	if board[min(ship_row + 1, rows - 1)][max(ship_col - 1, 0)] != "S":	
		board[min(ship_row + 1, rows - 1)][max(ship_col - 1, 0)] = "X"

	if board[max(ship_row - 1, 0)][min(ship_col + 1, columns - 1)] != "S":
		board[max(ship_row - 1, 0)][min(ship_col + 1, columns - 1)] = "X"

	if board[max(ship_row - 1, 0)][max(ship_col - 1, 0)] != "S":
		board[max(ship_row - 1, 0)][max(ship_col - 1, 0)] = "X"

	if n == 1:
		if board[ship_row][max(ship_col - 1, 0)] != "S":
			board[ship_row][max(ship_col - 1, 0)] = "X"

		if board[ship_row][min(ship_col + 1, columns - 1)] != "S":
			board[ship_row][min(ship_col + 1, columns - 1)] = "X"

		if board[max(ship_row - 1, 0)][ship_col] != "S":
			board[max(ship_row - 1, 0)][ship_col] = "X"

		if board[min(ship_row + 1, rows - 1)][ship_col] != "S":
			board[min(ship_row + 1, rows - 1)][ship_col] = "X"

		return True

	for i in range(1, n):
		if ship_direction == 0:
			ship_col -= 1

			if ship_col < 0:
				ship_col = i
				ship_direction = 1

			board[ship_row][ship_col] = "S"

			if board[min(ship_row + 1, rows- 1)][min(ship_col + 1, columns - 1)] != "S":
				board[min(ship_row + 1, rows- 1)][min(ship_col + 1, columns - 1)] = "X"

			if board[min(ship_row + 1, rows - 1)][max(ship_col - 1, 0)] != "S":	
				board[min(ship_row + 1, rows - 1)][max(ship_col - 1, 0)] = "X"

			if board[max(ship_row - 1, 0)][min(ship_col + 1, columns - 1)] != "S":
				board[max(ship_row - 1, 0)][min(ship_col + 1, columns - 1)] = "X"

			if board[max(ship_row - 1, 0)][max(ship_col - 1, 0)] != "S":
				board[max(ship_row - 1, 0)][max(ship_col - 1, 0)] = "X"


		elif ship_direction == 1:
			ship_col += 1
			if ship_col > columns - 1:
				ship_col = columns - 1 - i
				ship_direction = 0
			board[ship_row][ship_col] = "S"

			if board[min(ship_row + 1, rows- 1)][min(ship_col + 1, columns - 1)] != "S":
				board[min(ship_row + 1, rows- 1)][min(ship_col + 1, columns - 1)] = "X"

			if board[min(ship_row + 1, rows - 1)][max(ship_col - 1, 0)] != "S":	
				board[min(ship_row + 1, rows - 1)][max(ship_col - 1, 0)] = "X"

			if board[max(ship_row - 1, 0)][min(ship_col + 1, columns - 1)] != "S":
				board[max(ship_row - 1, 0)][min(ship_col + 1, columns - 1)] = "X"

			if board[max(ship_row - 1, 0)][max(ship_col - 1, 0)] != "S":
				board[max(ship_row - 1, 0)][max(ship_col - 1, 0)] = "X"


		elif ship_direction == 2:
			ship_row -= 1
			if ship_row < 0:
				ship_row = i 
				ship_direction = 3
			board[ship_row][ship_col] = "S"

			if board[min(ship_row + 1, rows- 1)][min(ship_col + 1, columns - 1)] != "S":
				board[min(ship_row + 1, rows- 1)][min(ship_col + 1, columns - 1)] = "X"

			if board[min(ship_row + 1, rows - 1)][max(ship_col - 1, 0)] != "S":	
				board[min(ship_row + 1, rows - 1)][max(ship_col - 1, 0)] = "X"

			if board[max(ship_row - 1, 0)][min(ship_col + 1, columns - 1)] != "S":
				board[max(ship_row - 1, 0)][min(ship_col + 1, columns - 1)] = "X"

			if board[max(ship_row - 1, 0)][max(ship_col - 1, 0)] != "S":
				board[max(ship_row - 1, 0)][max(ship_col - 1, 0)] = "X"


		else:
			ship_row += 1
			if ship_row > rows - 1:
				ship_row = rows - 1 - i
				ship_direction = 2
			board[ship_row][ship_col] = "S"

			if board[min(ship_row + 1, rows- 1)][min(ship_col + 1, columns - 1)] != "S":
				board[min(ship_row + 1, rows- 1)][min(ship_col + 1, columns - 1)] = "X"

			if board[min(ship_row + 1, rows - 1)][max(ship_col - 1, 0)] != "S":	
				board[min(ship_row + 1, rows - 1)][max(ship_col - 1, 0)] = "X"

			if board[max(ship_row - 1, 0)][min(ship_col + 1, columns - 1)] != "S":
				board[max(ship_row - 1, 0)][min(ship_col + 1, columns - 1)] = "X"

			if board[max(ship_row - 1, 0)][max(ship_col - 1, 0)] != "S":
				board[max(ship_row - 1, 0)][max(ship_col - 1, 0)] = "X"


	if ship_direction == 0:
		if board[ship_row][max(ship_col - 1, 0)] != "S":
			board[ship_row][max(ship_col - 1, 0)] = "X"

		if ship_beg_direction == 0:
			if board[ship_row][min(ship_beg_col + 1, columns - 1)] != "S":
				board[ship_row][min(ship_beg_col + 1, columns - 1)] = "X"
		

	if ship_direction == 1:
		if board[ship_row][min(ship_col + 1, columns - 1)] != "S":
			board[ship_row][min(ship_col + 1, columns - 1)] = "X"

		if ship_beg_direction == 1:
			if board[ship_row][max(ship_beg_col - 1, 0)] != "S":
				board[ship_row][max(ship_beg_col - 1, 0)] = "X"


	if ship_direction == 2:
		if board[max(ship_row - 1, 0)][ship_col] != "S":
			board[max(ship_row - 1, 0)][ship_col] = "X"

		if ship_beg_direction == 2:
			if board[min(ship_beg_row + 1, rows - 1)][ship_col] != "S":
				board[min(ship_beg_row + 1, rows - 1)][ship_col] = "X"


	if ship_direction == 3:
		if board[min(ship_row + 1, rows - 1)][ship_col] != "S":
			board[min(ship_row + 1, rows - 1)][ship_col] = "X"

		if ship_beg_direction == 3:
			if board[max(ship_beg_row - 1, 0)][ship_col] != "S":
				board[max(ship_beg_row - 1, 0)][ship_col] = "X"	

board = make_board(10)

add_ship(7, board)

'''
S = ship tile
X = tile next to a ship
O = empty tile
'''

for row in board:
		print(" ".join(row))