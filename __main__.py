from board import SudokuBoard
from generator import SudokuGenerator
from checker import SudokuChecker


if __name__ == '__main__':
    b = SudokuBoard()

    print(b)
    
    # b[3] = [1, 2 ,3 ,4, 5, 6, 7, 8, 9] 
    print(SudokuChecker().check_row(b, 1), " == False") 
    print(SudokuChecker().check_col(b, 1), " == False")
    print(SudokuChecker().check_nonet(b, 1)  , " == False")

    b.generate()

    print(SudokuChecker().check_row(b, 1), " == True") 
    print(SudokuChecker().check_col(b, 1), " == True")
    print(SudokuChecker().check_nonet(b, 1)  , " == True")

    print(b)
    