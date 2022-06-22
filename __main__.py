from os import system
from tkinter import Tk, Canvas, Frame, BOTH

from app import SudokuApp


if __name__ == '__main__':
    app = SudokuApp(True)
    app.root.attributes('-type', 'dialog')
    
    app.run()
 