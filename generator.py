import random
from copy import deepcopy

from helpers import get_nonet, is_filled


class SudokuGenerator:
    def __init__(self, board):
        self.board = board
        self.counter = 0

    def solve(self, board, generate=False):
        if is_filled(board):
            return

        for i in range(81):
            row, col = i // 9, i % 9

            if board[row][col] == 0:
                bucket = list(range(1, 10))
                if generate: 
                    random.shuffle(bucket)

                for value in bucket:
                    if value not in board[row]:
                        if value not in [board[i][col] for i in range(9)]:
                            if value not in get_nonet(board, (row, col)):
                                board[row][col] = value
                                
                                if is_filled(board):
                                    if generate: 
                                        return True
                                    else:
                                        self.counter += 1
                                        break
                                elif self.solve(board, generate):
                                        return True
                break
        board[row][col] = 0

    def generate(self, attempts=3):
        self.board.board = [ [0 for e in range(9)] for e2 in range(9) ]
        self.board.starting = [ [0 for e in range(9)] for e2 in range(9) ]
        self.board.solution = [ [0 for e in range(9)] for e2 in range(9) ]
        temp_board = None

        self.solve(self.board.board, generate=True)

        while attempts > 0:
            i, j = 0, 0
            while self.board.board[i][j] == 0:
                i, j = random.randint(0,8), random.randint(0,8)

            back = self.board.board[i][j]
            self.board.board[i][j] = 0

            temp_board = deepcopy(self.board.board)

            self.counter = 0
            self.solve(temp_board)
            if self.counter != 1:
                self.board.board[i][j] = back
                attempts -= 1

        self.board.starting = deepcopy(self.board.board)
        self.board.solution = deepcopy(self.board.board)
        self.solve(self.board.solution, generate=True)

    def add_killer_rules(self):
        pass