import random
from itertools import permutations

from checker import SudokuChecker


class SudokuBoard: 
    nonets = [(1,1),(1,4),(1,7),(4,1),(4,4),(4,7),(7,1),(7,4),(7,7)]

    def __init__(self):
        self.board = [ [0 for list in range(9)] for list in range(9) ]
        self.solution = None

    def generate(self):
        not_visited = [(i, j) for i in range(9) for j in range(9)]
        pos = random.randint(0, 8), random.randint(0, 8)

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        move = random.choice(moves)

        i = 0  
        limit = 0
        while i < 81:
            if self.board[pos[0]][pos[1]] != 0:
                if len(not_visited) == 0:
                    return True
                i = i - 1
                pos = random.choice(not_visited)
                continue 

            choices = SudokuChecker.check(self.board, pos) 
            try: 
                choice = random.choice(choices)
            except IndexError:
                pass

            self.board[pos[0]][pos[1]] = choice

            not_visited.remove(pos)
            pos = (pos[0] + move[0]) % 9, (pos[1] + move[1]) % 9
            if not (0 <= pos[0] + move[0] and pos[0] + move[0] <= 8 and 0 <= pos[1] + move[1] and pos[1] + move[1] <= 8):
                move = random.choice(moves)
                
            i = i + 1

    

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