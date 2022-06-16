import numpy as np


class Constants:
    ROWS = 6
    COLUMNS = 7


class ConnectFour:
    def __init__(self, rows=Constants.ROWS, columns=Constants.COLUMNS):
        self.board = np.zeros((rows, columns))
        self.players = [None] * 2
        self.turn = 0
        self.top_filled_rows = [Constants.ROWS - 1] * Constants.COLUMNS
        self.game_over = False

    def add_players(self, player_one, player_two):
        self.players[0], self.players[1] = player_one, player_two

    def is_valid_choice(self, column):
        is_on_board = 1 <= column <= 7
        is_valid_column = not self.board[0][column]
        return is_on_board and is_valid_column

    def start_game(self):
        while not self.game_over:
            column = int(input(f'{self.players[self.turn]}\'s turn (1 - 7): '))
            self.turn = (self.turn + 1) % 2


def main():
    game = ConnectFour()
    game.start_game()


if __name__ == '__main__':
    main()
