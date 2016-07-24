from random import randint

def make_board(size):
    board = []
    rows = columns = size

    # it makes a board with a border of X tiles
    board.append(['X'] * columns)

    for i in range(rows):
        board.append(['O'] * columns)
        board[i].insert(0, 'X')
        board[i].append('X')

    board[rows].insert(0, 'X')
    board[rows].append('X')
    board.append(['X'] * (columns + 2))

    return board

def add_ship(size, board):
    rows = columns = len(board)

    li = [
    [0, -1], # Left
    [0, 1],  # Right
    [-1, 0], # Up
    [1, 0]   # Down
    ]

    while True:
        # it chooses a random tile and ship direction
        ship_row = randint(1, rows - 2)
        ship_col = randint(1, columns - 2)
        ship_direction = randint(0,3)

        # if the selected tile is empty
        if board[ship_row][ship_col] == 'O':

            # it checks all the tiles in the chosen direction
            for i in range(1, size):
                # If the ship can't fit in that direction, it restarts
                if board[ship_row + i * li[ship_direction][0]] \
                        [ship_col + i * li[ship_direction][1]] == 'X':
                    break

            # if it didn't find an obstacle it draws the ship and exits the loop
            else:
                for k in range(size):
                    board[ship_row + k * li[ship_direction][0]] \
                    [ship_col + k * li[ship_direction][1]] = 'S'

                    board[ship_row + k * li[ship_direction][0] + li[ship_direction][1]] \
                    [ship_col + k * li[ship_direction][1] + li[ship_direction][0]] = 'X'

                    board[ship_row + k * li[ship_direction][0] - li[ship_direction][1]] \
                    [ship_col + k * li[ship_direction][1] - li[ship_direction][0]] = 'X'

                if ship_direction == 0 or ship_direction == 1:
                    board[ship_row - 1][ship_col + size * li[ship_direction][1]] = 'X'
                    board[ship_row][ship_col + size * li[ship_direction][1]]     = 'X'
                    board[ship_row + 1][ship_col + size * li[ship_direction][1]] = 'X'

                    board[ship_row - 1][ship_col - li[ship_direction][1]] = 'X'
                    board[ship_row][ship_col - li[ship_direction][1]]     = 'X'
                    board[ship_row + 1][ship_col - li[ship_direction][1]] = 'X'
                
                else:
                    board[ship_row - li[ship_direction][0]][ship_col - 1] = 'X'
                    board[ship_row - li[ship_direction][0]][ship_col]     = 'X'
                    board[ship_row - li[ship_direction][0]][ship_col + 1] = 'X'

                    board[ship_row + size * li[ship_direction][0]][ship_col - 1] = 'X' 
                    board[ship_row + size * li[ship_direction][0]][ship_col]     = 'X'
                    board[ship_row + size * li[ship_direction][0]][ship_col + 1] = 'X'

                break