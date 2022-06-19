import random
from itertools import permutations
from copy import deepcopy

from generator import SudokuGenerator
from checker import SudokuChecker


class SudokuBoard: 
    bucket = [1,2,3,4,5,6,7,8,9]
    nonets = [(1,1),(1,4),(1,7),(4,1),(4,4),(4,7),(7,1),(7,4),(7,7)]
    neighbors = [(-1, -1),  (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, new_game=False, nhints=60):
        self.board = [ [0 for list in range(9)] for list in range(9) ]
        self.starting = [ [0 for list in range(9)] for list in range(9) ]
        self.solution = [ [0 for list in range(9)] for list in range(9) ]

        if new_game:
            self.new_game(nhints)

    def new_game(self, nhints=60):
        b = random.sample(self.bucket, 9)

        # for i in range(9):
            
        for x in map(lambda x: (x[0][0] + x[1][0], x[0][1] + x[1][1]), zip(random.sample(self.nonets, 9), random.sample(self.neighbors, 9))):
            self.board[x[0]][x[1]] = random.choice(b)
            b.remove(self.board[x[0]][x[1]])


        SudokuGenerator.solve(self)
        self.solution = deepcopy(self.board)
        
        if nhints != 0:
            for _ in range(min(81-nhints, 64)):
                self.board[random.randint(0,8)][random.randint(0,8)] = 0

        return self

    def is_filled(self):
        for r in self.board:
            if 0 in r:
                return False
        
        return True

    def check(self, partial=True):
        print(self)
        if partial or self.is_filled():
            return SudokuChecker.check_board(self.board)
        else:
            return False

    # def check_solution(self, partial=True):
    #     self.starting = deepcopy(self.board)
    #     self.board = self.solution
    #     result = self.check(partial)
    #     self.board = self.starting
    #     return result

    def check_move(self, pos, value):
        temp = self.board[pos[0]][pos[1]]
        self.board[pos[0]][pos[1]] = value

        if SudokuChecker.check_move(self, pos):
            self.board[pos[0]][pos[1]] = temp
            return True
        else: 
            self.board[pos[0]][pos[1]] = temp
            return False

    def get_nonet_idx(self, pos):
        idxs = list(map(lambda n: (n[0]-pos[0])**2 + (n[1]-pos[1])**2, SudokuBoard.nonets))
        return idxs.index(min(idxs))

    def get_nonet(self, pos):
        bucket = []
        idx = self.get_nonet_idx(pos)
        for n in self.neighbors:
            k = self.nonets[idx] 
            bucket.append(self.board[n[0] + k[0]][n[1] + k[1]])

        return bucket
    
    def __len__(self):
        return len(self.board)

    def move(self, pos, value):
        self[pos[0]][pos[1]] = value

    def __getitem__(self, key):
        return self.board[key]

    def __setitem__(self, key, value):
        self.board[key] = value

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