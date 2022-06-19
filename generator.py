import random


class SudokuGenerator:
    @staticmethod
    def solve(board):
        for i in range(81):
            row, col = i // 9, i % 9

            if board[row][col] == 0:
                # bucket = list(range(1, 10))
                # random.shuffle(bucket)
                for value in range(1, 10):
                    if value not in board[row]:
                        if value not in [board[i][col] for i in range(9)]:
                            if value not in board.get_nonet((row, col)):
                                board[row][col] = value
                                
                                if board.is_filled():
                                    return True
                                elif SudokuGenerator.solve(board):
                                        return True
                break
        board[row][col] = 0