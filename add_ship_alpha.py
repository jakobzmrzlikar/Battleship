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

	dic = {
	# Desno
	0: [0, -1],
	# Levo
	1: [0, 1],
	# Dol
	2: [-1, 0],
	# Gor
	3: [1, 0]
	}

	space = 0
	no_space = False
	bound = False
	exit = False

	while not exit:

		# Izbere random začetno polje in smer ladje

		#ship_row = randint(1, rows - 2)
		#ship_col = randint(1, columns - 2)
		#ship_direction = randint(0,3)

		# Debug test code

		ship_row = 5
		ship_col = 5
		ship_direction = 2

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
						if board[ship_row - j * dic[ship_direction][0]][ship_col - j * dic[ship_direction][1]] == "X":
							no_space = True
							break
					# Če je dovolj prostora za  v obeh smereh za eno ladjo, jo nariše in gre ven iz vseh zank:
					else:
						for k in range(n):
							board[ship_row - (space - k) * dic[ship_direction][0]] \
							[ship_col - (space - k) * dic[ship_direction][1]] = "S"

							board[ship_row - (space - k) * dic[ship_direction][0] - dic[ship_direction][1]] \
							[ship_col - (space - k) * dic[ship_direction][1] - dic[ship_direction][0]] = "X"

					# ne izriše X v kotih ladje
					board[ship_row + (space + 1) * dic[ship_direction][0]] \
					[ship_col + (space + 1) * dic[ship_direction][1]] = "X"


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

				board[ship_row + dic[ship_direction][0]] \
				[ship_col + dic[ship_direction][1]] = "X"

				board[ship_row - n * dic[ship_direction][0]] \
				[ship_col - n * dic[ship_direction][1]] = "X"

				# ne izriše X v kotih ladje
				exit = True
