class SudokuChecker:
    nonets = [(1,1),(1,4),(1,7),(4,1),(4,4),(4,7),(7,1),(7,4),(7,7)]
    full_bucket = [1,2,3,4,5,6,7,8,9]

    @staticmethod
    def check_row(board, row):
        s = 0
        bucket = []
        for e in board[row]:
            if e not in bucket or e == 0:
                bucket.append(e)
                s += e

        if s != 45:
            return set(SudokuChecker.full_bucket) - set(bucket)

    @staticmethod
    def check_col(board, col):
        s = 0
        bucket = []
        for r in board:
            if r[col] not in bucket or r[col] == 0:
                bucket.append(r[col])
                s += r[col]

        if s != 45:
            return set(SudokuChecker.full_bucket) - set(bucket)

    @staticmethod
    def check_nonet(board, i):
        s = 0
        bucket = []
        nonets = [(1,1),(1,4),(1,7),(4,1),(4,4),(4,7),(7,1),(7,4),(7,7)]
        neighbors = [(-1, -1),  (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for n in neighbors:
            cell = board[nonets[i][0] + n[0]][nonets[i][1] + n[1]]
            if cell not in bucket or cell == 0:
                bucket.append(cell)
                s += cell
 
        print(s)
        if s != 45:
            return set(SudokuChecker.full_bucket) - set(bucket)

    @staticmethod
    def check(board, pos):
        row = SudokuChecker.check_row(board, pos[0])
        col = SudokuChecker.check_col(board, pos[1])
        
        idxs = list(map(lambda n: (n[0]-pos[0])**2 + (n[1]-pos[1])**2, SudokuChecker.nonets))
        n = idxs.index(min(idxs))
        non = SudokuChecker.check_nonet(board, n)

        return list(row & col & non)

    @staticmethod
    def check_board(board):
        board = board
        for i in range(9):
            if not SudokuChecker.check_nonet(board, i):
                return False

        return True

    @staticmethod
    def is_filled(board, self):
        for r in board:
            if 0 in r:
                return False
        
        return True