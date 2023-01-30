from typing import Callable
import time

START_TIME = '180'  # in sec


class GameChar:
    def __init__(self, digit, coord):
        self._digit = digit
        self._coord = coord

    @property
    def digit(self):
        return self._digit

    @property
    def coord(self):
        return self._coord


class GameTime:

    def __init__(self, h, m, s):
        self._hours
        self._minutes = m
        self._seconds = s


class GameModel:
    _time: str
    _current_word: list
    _path: list
    _game_is_running: bool
    _last_char_preesed: GameChar
    _score: str

    def __init__(self):
        self.reset_game()

    def del_last_char(self):
        self._current_word.pop()

    def add_char_to_word(self, c):
        # if not self._current_word[-1].coord() == c.coord():
        self._current_word.append(c)

    @property
    def score(self):
        return self._score

    def update_score(self):
        self._score += len(self.path) ** 2
        self.taken_words.append(self.current_word())
        self.reset_word()

    def set_time(self, t):
        self._time = t

    def set_game_is_running(self, run):
        self._game_is_running = run

    def current_word(self):
        x = ''.join(self._current_word)
        return x

    def reset_word(self):
        self._current_word = []
        self._path = []

    def game_is_running(self):
        return self._game_is_running

    @property
    def path(self):
        return self._path

    def add_coor_to_path(self, coor: tuple):
        self._path.append(coor)

    def reset_game(self):
        self._time = START_TIME
        self._current_word = []
        self._path = []
        self._game_is_running = False
        self._score = 0
        self.taken_words = []


"""
functions:
1. check if press is legal
2. function calculate score
3. reset word button
4. resize the label
5. save words user got scores for
6. fix timer
7. add score label
8. finish game button
9. time end function
"""
