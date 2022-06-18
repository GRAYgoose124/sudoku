import random

from checker import SudokuChecker


class SudokuBoard: 
    nonets = [(1,1),(1,4),(1,7),(4,1),(4,4),(4,7),(7,1),(7,4),(7,7)]

    def __init__(self):
        self.board = [ [0 for list in range(9)] for list in range(9) ]
        self.solution = None

    def generate(self):
        bucket = []
        pos = (random.randint(0, 8), random.randint(0, 8))
        moves = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        new_pos = (5, 5)

        
        for i in range(9):
            for j in range(9):
                choices = SudokuChecker.check(self.board, (i, j)) 
                try:
                    choice = random.choice(choices)
                except IndexError:
                    pass
                self.board[i][j] = choice
                
    

    def pretty(self):
        s = ""
        for i, r in enumerate(self.board):
            if i % 3 == 0:
                s += '█'*23 + "\n"

            for j, e in enumerate(r):
                if j != 0 and j % 3 == 0:
                    s += "|█"
                s += f"|{e if e != 0 else ' '}"
            s += "|\n"

        s += '█'*23 + "\n"
        
        return s

    def __getitem__(self, key):
        return self.board[key]

    def __setitem__(self, key, value):
        self.board[key] = value

    def __str__(self):
        return self.pretty()