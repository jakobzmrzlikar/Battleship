# coding=utf-8
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

	if n == 0:
		return False

	rows = size[0]
	columns = size[1]

	dic = {
	# Levo
	0: [0, -1],
	# Desno
	1: [0, 1],
	# Gor
	2: [-1, 0],
	# Dol
	3: [1, 0]
	}

	
	end = False

	while not end:
		space = 0
		no_space = False
		bound = False

		# Izbere random začetno polje in smer ladje
		ship_row = randint(1, rows - 2)
		ship_col = randint(1, columns - 2)
		ship_direction = randint(0,3)

		# Če je izbrano polje še prosto
		if board[ship_row][ship_col] == "O":

			# Preveri vsa polja v dani smeri
			for i in range(1, n):

				# Če je polje zasedeno, si zapomni, koliko prostora je v tisti smeri.
				if board[ship_row + i * dic[ship_direction][0]][ship_col + i * dic[ship_direction][1]] == "X":
					space += (i - 1)
					bound = True

					# Nato preveri še minimalno število polj v nasprotni smeri, ki je potrebno za to, da se ladjo nariše sem vmes.
					for j in range(n - 1 - space):

						# Če ni dovolj prostora niti v tej smeri, si to zapomni in gre nazaj na izbiro začetnega polja.
						if board[ship_row - (j + 1) * dic[ship_direction][0]][ship_col - (j + 1) * dic[ship_direction][1]] == "X":
							no_space = True
							break

					# Če je dovolj prostora v obeh smereh za eno ladjo, jo nariše in gre ven iz vseh zank:
					else:
						for k in range(n):
							board[ship_row + (space - k) * dic[ship_direction][0]] \
							[ship_col + (space - k) * dic[ship_direction][1]] = "S"

							board[ship_row + (space - k) * dic[ship_direction][0] - dic[ship_direction][1]] \
							[ship_col + (space - k) * dic[ship_direction][1] - dic[ship_direction][0]] = "X"

							board[ship_row + (space - k) * dic[ship_direction][0] + dic[ship_direction][1]] \
							[ship_col + (space - k) * dic[ship_direction][1] + dic[ship_direction][0]] = "X"

						if ship_direction == 0 or ship_direction == 1:
							board[ship_row - 1][ship_col - (n - space ) * dic[ship_direction][1]] = "X"
							board[ship_row][ship_col - (n - space ) * dic[ship_direction][1]] = "X"
							board[ship_row + 1][ship_col - (n - space ) * dic[ship_direction][1]] = "X"

						else:
							board[ship_row - (n - space) * dic[ship_direction][0]][ship_col - 1] = "X"
							board[ship_row - (n - space) * dic[ship_direction][0]][ship_col] = "X"
							board[ship_row - (n - space) * dic[ship_direction][0]][ship_col + 1] = "X"

						end = True
					break

			if not bound:
				for k in range(n):
					board[ship_row + (k * dic[ship_direction][0])] \
					[ship_col + (k * dic[ship_direction][1])] = "S"

					board[ship_row + (k * dic[ship_direction][0]) + dic[ship_direction][1]] \
					[ship_col + (k * dic[ship_direction][1]) + dic[ship_direction][0]] = "X"

					board[ship_row + (k * dic[ship_direction][0]) - dic[ship_direction][1]] \
					[ship_col + (k * dic[ship_direction][1]) - dic[ship_direction][0]] = "X"

				if ship_direction == 0 or ship_direction == 1:
					board[ship_row - 1][ship_col + n * dic[ship_direction][1]] = "X"
					board[ship_row][ship_col + n * dic[ship_direction][1]] = "X"
					board[ship_row + 1][ship_col + n * dic[ship_direction][1]] = "X"

					board[ship_row - 1][ship_col - dic[ship_direction][1]] = "X"
					board[ship_row][ship_col - dic[ship_direction][1]] = "X"
					board[ship_row + 1][ship_col - dic[ship_direction][1]] = "X"
				
				else:
					board[ship_row - dic[ship_direction][0]][ship_col - 1] = "X"
					board[ship_row - dic[ship_direction][0]][ship_col] = "X"
					board[ship_row - dic[ship_direction][0]][ship_col + 1] = "X"

					board[ship_row + n * dic[ship_direction][0]][ship_col - 1] = "X" 
					board[ship_row + n * dic[ship_direction][0]][ship_col] = "X"
					board[ship_row + n * dic[ship_direction][0]][ship_col + 1] = "X"

				end = True