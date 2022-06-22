from os import system
from tkinter import Tk, Canvas, Frame, BOTH

from game import SudokuApp


if __name__ == '__main__':
    game = SudokuApp(True)
    game.root.attributes('-type', 'dialog')
    
    game.run()
 