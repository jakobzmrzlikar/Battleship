import time

from AI import AI
from GUI import GUI
from Game import Game


def main():

    game = Game()
    ai = AI(game)
    gui = GUI(game, ai)


start = time.time()

if __name__ == '__main__':
    main()

end = time.time() - start
print('\n' + str(end) + 's')
