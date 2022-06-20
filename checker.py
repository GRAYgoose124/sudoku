from helpers import neighbors, nonets


class SudokuChecker:
    BadMove = -1 # Sentinel indicating a bad position has occured.
    full_bucket = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    @staticmethod
    def check_row(board, row):
        s = 0
        bucket = []
        for e in board[row]:
            if e not in bucket or e == 0:
                bucket.append(e)
                s += e
            else:
                return set([SudokuChecker.BadMove])

        if s != 45:
            return set(range(9)) - set(bucket)
        else:
            return set()

    @staticmethod
    def check_col(board, col):
        s = 0
        bucket = []
        for r in board:
            if r[col] not in bucket or r[col] == 0:
                bucket.append(r[col])
                s += r[col]
            else:
                return set([SudokuChecker.BadMove])

        if s != 45:
            return set(SudokuChecker.full_bucket) - set(bucket)
        else:
            return set()

    @staticmethod
    def check_non(board, i):
        s = 0
        bucket = []
        
        for n in SudokuChecker.neighbors:
            cell = board[SudokuChecker.nonets[i][0] + n[0]][SudokuChecker.nonets[i][1] + n[1]]
            if cell not in bucket or cell == 0:
                bucket.append(cell)
                s += cell
            else:
                return set([SudokuChecker.BadMove])
 
        if s != 45:
            return set(SudokuChecker.full_bucket) - set(bucket)
        else:
            return set()

    @staticmethod
    def check(board, i):
        j, k, l = i, i, i
        if isinstance(i, tuple):
            j, k, l = i

        row = SudokuChecker.check_row(board, j)
        col = SudokuChecker.check_col(board, k)
        non = SudokuChecker.check_non(board, l)
        if (SudokuChecker.BadMove in row or 
            SudokuChecker.BadMove in col or 
            SudokuChecker.BadMove in non):
            return False
        return row & col & non

    @staticmethod
    def check_board(board):
        for i in range(9):
            valid = SudokuChecker.check(board, i)

        if valid == set():
            return True
   
    @staticmethod
    def check_move(board, pos):
        valid = SudokuChecker.check(board, pos[0])
        if valid == set():
            return True

    @staticmethod 
    def valid_moves(board, pos):
        return list((SudokuChecker.check_col(board, pos[0]) &
                     SudokuChecker.check_row(board, pos[1]) &
                     SudokuChecker.check_non(board, pos   )) - set([-1])) 