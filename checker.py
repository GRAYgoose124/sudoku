class SudokuChecker:
    BadMove = -1 # Sentinel indicating a bad position has occured.
    full_bucket = [1,2,3,4,5,6,7,8,9]

    nonets = [(1,1),(1,4),(1,7),(4,1),(4,4),(4,7),(7,1),(7,4),(7,7)]
    neighbors = [(-1, -1),  (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

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
            return set(SudokuChecker.full_bucket) - set(bucket)
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
    def check_nonet(board, i):
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
    def check_board(board):
        for i in range(9):
            if SudokuChecker.BadMove in SudokuChecker.check_row(board, i):
                return False
            if SudokuChecker.BadMove in SudokuChecker.check_col(board, i):
                return False
            if SudokuChecker.BadMove in SudokuChecker.check_nonet(board, i):
                return False

        return True
   
    @staticmethod
    def check_move(board, pos):
        b = board.board
        """Terrible method to get a list of valid moves"""
        if SudokuChecker.BadMove in SudokuChecker.check_row(b, pos[0]):
            return False
        if SudokuChecker.BadMove in SudokuChecker.check_col(b, pos[1]):
            return False
        if SudokuChecker.BadMove in SudokuChecker.check_nonet(b, board.get_nonet_idx(pos)):
            return False

        return True

    @staticmethod
    def valid_moves(board, pos):
        return list(SudokuChecker.all_moves(board, pos) - set([-1]))