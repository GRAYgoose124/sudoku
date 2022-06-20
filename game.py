import math
import time

from tkinter import Tk, Canvas, Frame, BOTH, messagebox
from tkinter.font import Font

from copy import deepcopy

from board import SudokuBoard
from checker import SudokuChecker
from helpers import neighbors

class SudokuApp():
    def __init__(self, new_game=True, nhints=60, cell_size=50):
        self.current_pos = (None, None)
        self.last_move = None
        self.filled = (None, None, None)
        self.hover = (None, None, None)
        self.cages = [[None for _ in range(9)] for _ in range(9)]
        self.move_checking = True

        self.notetaking = False
        self.notes = [ [None for list in range(9)] for list in range(9) ]
        for i, r in enumerate(self.notes):
            for j, e in enumerate(r):
                self.notes[i][j] = {}
        
        self.root = Tk()
        self.cellfont = Font(family="Terminus", size=24, weight="bold")
        self.notefont = Font(family="Terminus", size=8)

        self.game = SudokuGame(new_game=new_game, nhints=nhints, cell_size=cell_size)
        self.canvas = Canvas(self.game)
        self.initUI(self.game)
        self.initKeybinds()

    def initUI(self, game):
        game.master.title("Sudoku Game")
        game.pack(fill=BOTH, expand=1)
        self.canvas.pack(fill=BOTH, expand=1)

        self.draw_grid()
 
    def initKeybinds(self):
        self.root.bind('<ButtonRelease-1>', self.on_click)
        self.root.bind('<Key>', self.on_key)
        self.root.bind('S', self.solve_game)
        self.root.bind('R', lambda e: setattr(self.game.board, 'board', deepcopy(self.game.board.starting)))
        self.root.bind('C', self.check_solution)
        self.root.bind('c', lambda e: setattr(self, 'move_checking', not self.move_checking))
        self.root.bind('N', lambda e: self.game.board.solver.generate())
        self.root.bind('n', lambda e: setattr(self, 'notetaking', not self.notetaking))
        self.root.bind('<Escape>', self.quit)

    def draw_grid(self):
        o = [self.game.pos[0], self.game.pos[1]]

        for _i, cell in enumerate(self.game.cells):
            i, j = _i // 9, _i % 9

            value = self.game.board[i][j]
            notes = self.notes[i][j]

            if value == 0:
                value = ' '
            center = (cell[2] + cell[0]) / 2 , (cell[3] + cell[1]) / 2

            # Color the cells based on the last move
            if self.current_pos is not None and self.current_pos[0] == i and self.current_pos[1] == j:
                self.hover = (i, j, 'grey')
                if self.last_move is not None:
                    if self.last_move:
                        self.filled = (i, j, 'green')
                    elif self.last_move == False:
                        self.filled = (i, j, 'red')

                    self.last_move = None

            # Create border and draw numbers:
            filled = self.filled
            if self.hover[0] == i and self.hover[1] == j:
                filled = self.hover

            self.canvas.create_rectangle(cell[0], cell[1], cell[2], cell[3], fill=filled[2] if filled[0] == i and filled[1] ==  j else '', outline='black')
            self.canvas.create_text(center[0], center[1], font=self.cellfont, text=value)

            # Draw notes
            for c in notes:
                addd = lambda x, y: (x[0] * y[0], x[1] * y[1])
                note_offset = addd(neighbors[int(c) - 1], (self.game.cell_size * .3, self.game.cell_size * .3))
                self.canvas.create_text(center[0]+note_offset[0], center[1]+note_offset[1], font=self.notefont, text=c, fill='darkblue')
                    
        self.canvas.create_rectangle((o[0]-self.game.cell_size*4.2) , o[1] - self.game.cell_size*4.2, self.game.cells[-1][0]+self.game.cell_size*1.1, self.game.cells[-1][1]+self.game.cell_size*1.1)
     
    def run(self):
        self.root.geometry("550x550+500+500")
        self.update()
        self.root.mainloop()
        
    def update(self):
        self.canvas.delete('all')
        self.draw_grid()
        self.root.after(13, self.update)

    def quit(self, event):
        self.root.quit()

    def on_click(self, event):
        self.current_pos = self.game.get_closest_cell((event.x, event.y))

    def on_key(self, event): 
        if self.current_pos is not None:
            if not self.notetaking:
                if event.char == "\x08":
                    self.game.board[self.current_pos[0]][self.current_pos[1]] = 0
                elif event.char.isdigit():
                    self.game.board[self.current_pos[0]][self.current_pos[1]] = int(event.char)

                    if self.move_checking:
                        if self.game.board.check_move(self.current_pos, int(event.char)):
                            self.last_move = True
                        else:
                            self.last_move = False
            else:
                if event.char.isdigit():
                    if event.char not in self.notes[self.current_pos[0]][self.current_pos[1]]:
                        self.notes[self.current_pos[0]][self.current_pos[1]][event.char] = True
                    else:
                        del(self.notes[self.current_pos[0]][self.current_pos[1]][event.char])

    def solve_game(self, event):
        self.game.board.solver.solve(self.game.board.board, generate=True)
        # done = True
        # for i, r in enumerate(self.game.board.board):
        #     try:
        #         j = r.index(0)
        #         self.game.board.board[i][j] = self.game.board.solution[i][j]
        #         done = False
        #         break
        #     except ValueError:
        #         done = True

        # if not done:
        #     self.root.after(int((1/3)*100), lambda: self.solve_game(event))

    def check_solution(self, event):
        if self.game.board.check():
            messagebox.showinfo(title="You win!", message="Congratulations!")
        else:
            messagebox.showinfo(title="Sorry!", message="Not correct!")           


class SudokuGame(Frame):
    def __init__(self, new_game=True, nhints=60, cell_size=50):        
        super().__init__()

        self.cell_size = cell_size
        self.pos = (self.cell_size*5, self.cell_size*5)

        self.board = SudokuBoard(new_game=new_game, nhints=nhints)
        self.cells = self.get_cell_offsets(self.pos)

    def get_closest_cell(self, pos):
        current = None
        closest = 1000
        distance = lambda a, b: math.sqrt( ((a[0] - b[0])**2 - self.cell_size / 2) + ((a[1] - b[1])**2 - self.cell_size / 2) )

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
        o = [pos[0], pos[1]]

        offsets = []
        for i in neighbors:
            off = o[0] + ((i[0]*self.cell_size*3.1)), o[1] + ((i[1]*self.cell_size*3.1))
            for j in neighbors:
                off2 = off[0] + (j[0]*self.cell_size), off[1] + (j[1]*self.cell_size)
                cell = off2[0], off2[1], off2[0]+self.cell_size, off2[1]+self.cell_size
                offsets.append(cell)
        return offsets
