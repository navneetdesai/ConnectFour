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


class Board:
    def __init__(self, default_token, rows, columns):
        self.board = [[default_token for _ in range(columns)] for _ in range(rows)]
        self.top_filled_rows = [rows - 1 for _ in range(columns)]

    def __str__(self):
        # To-do: store and replace instead of creating every time?
        repr_ = []
        for row in self.board:
            repr_.extend(f'{str(token)} ' for token in row)
            repr_.append('\n')
        return ''.join(repr_)

    def get(self, row, column):
        return self.board[row][column]

    def is_winning_move(self, row, column, token) -> bool:
        # check horizontal
        # col from column -3 to column + 3
        board = self.board
        for c in range(column - 3, column + 1):
            count = sum(0 <= c + d < Constants.COLUMNS and board[row][c + d] == token for d in range(4))
            if count == 4:
                return True

        # check vertical
        for r in range(row - 3, row + 1):
            count = sum(0 <= r + d < Constants.ROWS and board[r + d][column] == token for d in range(4))
            if count == 4:
                return True

        # check negative diagonal
        count = 0
        for r, c in zip(range(row - 3, row + 1), range(column - 3, column + 1)):
            for d in range(4):
                # r - 3, c - 3 | r -2 , c - 2, | r - 1, c - 1 | r, c
                # r -2 , c - 2, | r - 1, c - 1 | r, c | r + 1, c + 1
                # r - 1, c - 1 | r, c | r + 1, c + 1 | r + 2, c + 2 ...
                if 0 <= r + d < Constants.ROWS and 0 <= c + d < Constants.ROWS \
                        and board[r + d][c + d] == token:
                    count += 1
            if count == 4:
                return True

        # check positive diagonal
        for r, c in zip(range(row + 3, row - 1, -1), range(column - 3, column + 1)):
            for d in range(4):
                # r + 3, c - 3 | r + 2 , c - 2, | r + 1, c - 1 | r, c
                # r + 2 , c - 2, | r + 1, c - 1 | r, c | r - 1, c + 1
                # r + 1, c - 1 | r, c | r - 1, c + 1 | r - 2, c + 2 ...
                if 0 <= r + d < Constants.ROWS and 0 <= c + d < Constants.ROWS \
                        and board[r - d][c + d] == token:
                    count += 1
            if count == 4:
                return True


    def drop_token(self, column, token) -> bool:
        row = self.top_filled_rows[column]
        self.board[row][column] = token
        self.top_filled_rows[column] -= 1
        return self.is_winning_move(row, column, token)


class ConnectFour:
    def __init__(self, rows=Constants.ROWS, columns=Constants.COLUMNS):
        self.board = Board(Tokens.WHITE, rows, columns)
        self.players = [None] * 2
        self.tokens = [Tokens.RED, Tokens.BLACK]
        self.turn = 0
        self.game_over = False

    def add_players(self, player_one, player_two):
        self.players[0], self.players[1] = player_one, player_two

    def is_valid_choice(self, column):
        is_on_board = 1 <= column <= 7
        is_valid_column = self.board.get(0, column) == Tokens.WHITE
        return is_on_board and is_valid_column

    def drop_token(self, column, token):
        self.board.drop_token(column, token)

    def start_game(self):
        while not self.game_over:
            print(self.board)
            column = int(input(f'{self.players[self.turn]}\'s turn (1 - 7): '))
            if column == -1:
                break
            if self.is_valid_choice(column):
                self.drop_token(column, self.tokens[self.turn])
            self.turn = (self.turn + 1) % 2


def main():
    game = ConnectFour()
    game.start_game()


if __name__ == '__main__':
    main()
