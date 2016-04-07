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
	exit = NoPlaceHere = False

	while not exit:

		# Izbere random začetno polje in smer ladje

		ship_beg_row = ship_row = randint(1, rows - 2)
		ship_beg_col = ship_col = randint(1, columns - 2)
		ship_beg_direction = ship_direction = randint(0,3)


		# Debug test code

		#ship_row = 
		#ship_col = 
		#ship_direction = 

		# Če je izbrano polje še prosto
		if board[ship_row][ship_col] == "O":
			# Preveri vsa polja v dani smeri
			for i in range(1, n):
				# Če je polje zasedeno, si zapomni, koliko prostora je v tisti smeri. 	
				if board[ship_row - i * dic[ship_direction][0]][ship_col - i * dic[ship_direction][1]] == "X":
					space += (i-1)
					print ("Debug: upper limit, space :" + str(space))
					# Nato preveri še minimalno število polj v nasprotni smeri, ki je potrebno za to, da se ladjo nariše sem vmes.
					for j in range(1, (n - 1 - space)):
						# Če ni dovolj prostora niti v tej smeri, si to zapomni in gre nazaj na izbiro začetnega polja.
						if board[ship_row + j * dic[ship_direction][0]][ship_col + j * dic[ship_direction][1]] == "X":
							NoPlaceHere = True
							print ("Debug: lower limit")
							break
					# Če je dovolj prostora za  v obeh smereh za eno ladjo, jo nariše in gre ven iz vseh zank:		
					else:
						for k in range(n):
							board[ship_row - (space - k) * dic[ship_direction][0]] \
							[ship_col - (space - k) * dic[ship_direction][1]] = "S"

							board[ship_row - (space - k) * dic[ship_direction][0] - dic[ship_direction][1]] \
							[ship_col - (space - k) * dic[ship_direction][1] - dic[ship_direction][0]] = "X"

							board[ship_row - (space - k) * dic[ship_direction][0] + dic[ship_direction][1]] \
							[ship_col - (space - k) * dic[ship_direction][1] + dic[ship_direction][0]] = "X"

						board[ship_row - (space + 1) * dic[ship_direction][0]] \
						[ship_col - (space + 1) * dic[ship_direction][1]] = "X"

						board[ship_row - (space - n) * dic[ship_direction][0]] \
						[ship_col - (space - n) * dic[ship_direction][1]] = "X"

						exit = True
						break
			if NoPlaceHere or exit:
				pass
			else:
				# Če je prostor v izbrani smeri, nariše ladjo tja.
				print("Debug: no limit")
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
