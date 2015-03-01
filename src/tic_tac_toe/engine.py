import decorator
import enum
import numpy as np
import sys
import traceback


class Team(enum.Enum):
    X = -1
    O = 1


@decorator.decorator
def soft_error(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except:
        _error()


class TicTacToe(object):

    def __init__(self):
        self.board = np.zeros((3, 3), dtype=np.int)
        self.turn = Team.O
        self.winning_team = None

    def game_over(self):
        return self.winning_team is not None

    @soft_error
    def mark_o(self, r, c):
        assert self.turn == Team.O and self.board[r, c] == 0 and not self.game_over()
        self.board[r, c] = Team.O.value
        self.turn = Team.X
        print(self.board)
        self._check_win()

    @soft_error
    def mark_x(self, r, c):
        assert self.turn == Team.X and self.board[r, c] == 0 and not self.game_over()
        self.board[r, c] = Team.X.value
        self.turn = Team.O
        print(self.board)
        self._check_win()

    @soft_error
    def _check_win(self):
        for team in Team:
            for i in range(3):
                if (self.board[i, :] == team.value).all() or (self.board[:, i] == team.value).all():
                    self._win(team)
            if all([mark == team.value for mark in (self.board[0, 0], self.board[1, 1], self.board[2, 2])]):
                self._win(team)
            if all([mark == team.value for mark in (self.board[0, 2], self.board[1, 1], self.board[2, 0])]):
                self._win(team)

    def _win(self, team):
        self.winning_team = team.name


def _error():
    traceback.print_exc(file=sys.stderr)
