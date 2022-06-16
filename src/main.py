import numpy as np


class ConnectFour:
    def __init__(self, rows=6, columns=7):
        self.board = np.zeros((rows, columns))
        self.game_over = False

    def start(self):
        while not self.game_over:
            pass


def main():
    game = ConnectFour()
    game.start()
    print(game.board)

if __name__ == '__main__':
    main()
