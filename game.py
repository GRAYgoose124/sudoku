import time

from tkinter import Frame
from copy import deepcopy

from board import SudokuBoard
from generator import SudokuGenerator


class SudokuGame(Frame):
    def __init__(self, new_game=True, cell_size=50):        
        super().__init__()

        self.cell_size = cell_size
        self.pos = (self.cell_size*5, self.cell_size*5)

        self.board = SudokuBoard()
        self.cells = self.get_cell_offsets(self.pos)

        self.solver = SudokuGenerator(self.board)
        self.solver.generate()

    def get_closest_cell(self, pos):
        current = None
        closest = 1000
        distance = lambda a, b: ((a[0] - b[0])**2 - self.cell_size / 2) + ((a[1] - b[1])**2 - self.cell_size / 2)**0.5

        for i, cell in enumerate(self.cells):
            center = (cell[2] + cell[0]) / 2 , (cell[3] + cell[1]) / 2

            
            dist = None
            try:
                dist = distance(pos, center)
            except ValueError:
                dist = distance(pos, cell)

            if dist < closest:
                closest = dist
                current = i // 9, i % 9
        
        return current

    def get_cell_offsets(self, pos):
        o = (self.cell_size, self.cell_size)

        offsets = []
        for j in range(9):
            for i in range (9):
                cell = o[0]+i*self.cell_size, o[1]+j*self.cell_size, o[0]+i*self.cell_size+self.cell_size, o[1]+j*self.cell_size+self.cell_size
                offsets.append(cell)
        return offsets
