import numpy as np
from enum import Enum


class Constants:
    ROWS = 6
    COLUMNS = 7


class Tokens(Enum):
    RED = '🔴'
    BLACK = '⚫'
    WHITE = '⚪'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class ConnectFour:
    def __init__(self, rows=Constants.ROWS, columns=Constants.COLUMNS):
        self.board = [[Tokens.WHITE] * Constants.COLUMNS] * Constants.ROWS
        self.players = [None] * 2
        self.tokens = [Tokens.RED, Tokens.BLACK]
        self.turn = 0
        self.top_filled_rows = [Constants.ROWS - 1] * Constants.COLUMNS
        self.game_over = False

    def add_players(self, player_one, player_two):
        self.players[0], self.players[1] = player_one, player_two

    def is_valid_choice(self, column):
        is_on_board = 1 <= column <= 7
        is_valid_column = not self.board[0][column]
        return is_on_board and is_valid_column

    def drop_token(self, column, piece):
        row = self.top_filled_rows[column]
        print(row)
        self.board[row][column] = piece

    def start_game(self):
        while not self.game_over:
            print(self.board)
            column = int(input(f'{self.players[self.turn]}\'s turn (1 - 7): '))
            if column == -1:
                break
            if self.is_valid_choice(column):
                print('here')
                self.drop_token(column, self.tokens[self.turn])
            self.turn = (self.turn + 1) % 2


def main():
    game = ConnectFour()
    game.start_game()


if __name__ == '__main__':
    main()
