"""
Author: Navneet Desai
ConnectFour Game
"""
import math
import sys
from enum import Enum
import pygame


class Constants:
    """
    Defines constant dimensions and color codes
    """
    ROWS = 6
    COLUMNS = 7
    SIZE = 150
    BLUE = 0, 0, 255
    BLACK = 0, 0, 0
    RED = 255, 0, 0
    WHITE = 255, 255, 255
    RADIUS = 45
    WAIT = 10000


class Tokens(Enum):
    """
    Defines game tokens
    """
    RED = '🔴'
    BLACK = '⚫'
    WHITE = '⚪'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class Pygame:
    """
    Class that handles Pygame specific functionality
    """
    @staticmethod
    def init_pygame():
        """
        Setup the pygame screen dimensions and font
        :return:
        """
        pygame.init()
        font = pygame.font.SysFont("Corbel", 75)
        unit_size = 100
        width = Constants.COLUMNS * unit_size
        height = (1 + Constants.ROWS) * unit_size
        size = width, height
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Connect Four')
        return screen, font

    @staticmethod
    def draw_circle(screen, color, row, column, radius):
        """
        Draws a circle of standard dimensions on a board with 'row' rows
        and 'column' columns
        """
        pygame.draw.circle(screen, color, (column * 100 + 50, row * 100 + 100 + 50),radius)

    @staticmethod
    def draw_rectangle(screen, color, row, column):
        """
        Draws a rectangle of standard dimensions on a board with 'row' rows
        and 'column' columns
        """
        pygame.draw.rect(screen, color, (column * 100, row * 100 + 100, 100, 100))


class Board:
    """
    Represents the board used in the game
    """
    def __init__(self, default_token, rows, columns):
        """
        Creates the board
        :param default_token: default token the board should be filled with
        :param rows: number of rows in the board
        :param columns: number of columns in the board
        """
        self.board = [[default_token for _ in range(columns)] for _ in range(rows)]
        self.top_filled_rows = [rows - 1 for _ in range(columns)]

    def __str__(self):
        """
        Representation of the board
        :return:
        """
        repr_ = []
        for row in self.board:
            repr_.extend(f'{str(token)} ' for token in row)
            repr_.append('\n')
        return ''.join(repr_)

    def get(self, row, column):
        """
        Returns the token at (row, column) position
        """
        return self.board[row][column]

    def is_winning_move(self, row, column, token) -> bool:
        """
        Returns true if the current move is a winning move
        :return:
        """
        board = self.board
        for col in range(column - 3, column + 1):
            count = sum(0 <= col + d < Constants.COLUMNS and board[row][col + d] == token \
                        for d in range(4))
            if count == 4:
                return True

        for row_ in range(row - 3, row + 1):
            count = sum(0 <= row_ + d < Constants.ROWS and board[row_ + d][column] == token \
                        for d in range(4))
            if count == 4:
                return True

        for row_, col in zip(range(row - 3, row + 1), range(column - 3, column + 1)):
            count = 0
            for dist in range(4):
                if 0 <= row_ + dist < Constants.ROWS and 0 <= col + dist < Constants.ROWS \
                        and board[row_ + dist][col + dist] == token:
                    count += 1
                if count == 4:
                    return True

        for row_, col in zip(range(row + 3, row - 1, -1), range(column - 3, column + 1)):
            count = 0
            for dist in range(4):
                if 0 <= row_ - dist < Constants.ROWS and 0 <= col + dist < Constants.ROWS \
                        and board[row_ - dist][col + dist] == token:
                    count += 1
                if count == 4:
                    return True
        return False

    def drop_token(self, column, token) -> bool:
        """
        Drops a token in a particular column on
        the board
        Returns true if the move is a winning move
        :param column: target column for the token
        :param token: token to be dropped
        :return: True if the move ends the game
        """
        row = self.top_filled_rows[column]
        self.board[row][column] = token
        self.top_filled_rows[column] -= 1
        return self.is_winning_move(row, column, token)


class ConnectFour:
    """
    Represents the ConnectFour game
    """
    def __init__(self, rows=Constants.ROWS, columns=Constants.COLUMNS):
        """
        Inits the game
        :param rows: number of rows on the board
        :param columns: number of columns on the board
        """
        self.board = Board(Tokens.BLACK, rows, columns)
        self.players = [None] * 2
        self.tokens = [Tokens.RED, Tokens.WHITE]
        self.turn = 0
        self.game_over = False

    def add_players(self, player_one, player_two):
        """
        Adds players to the game
        :param player_one:
        :param player_two:
        :return:
        """
        self.players[0], self.players[1] = player_one, player_two

    def is_valid_choice(self, column):
        """
        Validates whether the choice of column
        is valid
        :param column: target column
        :return: True if the move is valid
        """
        is_on_board = 1 <= column <= 7
        is_valid_column = self.board.get(0, column) == Tokens.BLACK
        return is_on_board and is_valid_column

    def drop_token(self, column, token):
        """
        Drops a token in the column
        """
        return self.board.drop_token(column, token)

    def draw_graphic_board(self, screen):
        """
        Draws the board on the screen
        :param screen: pygame object
        """
        for row in range(Constants.ROWS):
            for column in range(Constants.COLUMNS):
                Pygame.draw_rectangle(screen, Constants.BLUE, row, column)
                pygame.draw.rect(screen, Constants.BLUE, (column * 100, row * 100 + 100, 100, 100))
                if self.board.get(row, column) == Tokens.RED:
                    Pygame.draw_circle(screen, Constants.RED, row, column, Constants.RADIUS)
                elif self.board.get(row, column) == Tokens.WHITE:
                    Pygame.draw_circle(screen, Constants.WHITE, row, column, Constants.RADIUS)
                else:
                    Pygame.draw_circle(screen, Constants.BLACK, row, column, Constants.RADIUS)
        pygame.display.update()

    def start(self):
        """
        Starts the game and loops over the turns
        """
        player_one = input('Who\'s player one? - ')
        player_two = input('Who\'s player two? - ')
        self.add_players(player_one, player_two)
        screen, font = Pygame.init_pygame()
        self.draw_graphic_board(screen)
        pygame.display.update()
        while not self.game_over:
            self.run_game_loop(font, screen)
        pygame.time.wait(Constants.WAIT)

    def run_game_loop(self, font, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                column, _ = event.pos
                column = math.floor(column / 100)
                if self.is_valid_choice(column) and \
                        self.drop_token(column, self.tokens[self.turn]):
                    print(f'{self.players[self.turn]} has won! Congratulations!!!')
                    label = font.render(f"{self.players[self.turn]} wins!!!",
                                        True, Constants.WHITE)
                    screen.blit(label, (40, 10))
                    self.game_over = True
                self.turn = (self.turn + 1) % 2
            self.draw_graphic_board(screen)


def main():
    """
    Creates a ConnectFour instance and starts the game
    :return:
    """
    game = ConnectFour()
    game.start()


if __name__ == '__main__':
    main()
