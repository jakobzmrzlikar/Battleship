# Legacy tests:

#---------------------------------------------------------
# from add_ship_alpha import make_board, add_ship
# import time

# start = time.time()
# board = make_board(10)
# add_ship(2, board)
# add_ship(3, board)
# add_ship(3, board)
# add_ship(3, board)
# add_ship(4, board)
# add_ship(4, board)
# add_ship(5, board)

# for row in board:
# 		print(" ".join(row))

# end = time.time()-start
# print("\n" + str(end) + "s")
#-------------------------------------------------------


from main import AI, Battleship
import time

start = time.time()
game = Battleship()
ai = AI(game)

end = time.time()-start
print("\n" + str(end) + "s")