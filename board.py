import random
from itertools import permutations
from copy import deepcopy

from generator import SudokuGenerator
from checker import SudokuChecker
from helpers import is_filled


class SudokuBoard: 
    def __init__(self, new_game=False, nhints=17):
        self.board = None
        self.starting = None
        self.solution = None

        self.solver = SudokuGenerator(self)
        self.solver.generate()

    def check(self, full=True):
        if not full or is_filled(self.board):
            return SudokuChecker.check_board(self.board)
        else:
            return False

    def check_move(self, pos, value):
        temp = self.board[pos[0]][pos[1]]
        self.board[pos[0]][pos[1]] = value

        if SudokuChecker.check_move(self, pos):
            self.board[pos[0]][pos[1]] = temp
            return True
        else: 
            self.board[pos[0]][pos[1]] = temp
            return False
    
    def __len__(self):
        return len(self.board)

    def move(self, pos, value):
        self[pos[0]][pos[1]] = value

    def __getitem__(self, key):
        return self.board[key]

    def pretty(self, array):
        s = ""
        for i, r in enumerate(array):
            if i % 3 == 0:
                s += '█'*23 + "\n"

            for j, e in enumerate(r):
                if j != 0 and j % 3 == 0:
                    s += "|█"
                s += f"|{e if e != 0 else ' '}"
            s += "|\n"

        s += '█'*23 + "\n"
        
        return s

    def __str__(self):
        return self.pretty(self.board)