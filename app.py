from tkinter import Tk, Canvas, BOTH, messagebox
from tkinter.font import Font
from copy import deepcopy

from helpers import neighbors

from game import SudokuGame


class SudokuApp():
    def __init__(self, new_game=True, cell_size=50):
        self.current_pos = (None, None)
        self.last_move = None
        self.filled = (None, None, None)
        self.hover = (None, None, None)
        self.cages = [[None for _ in range(9)] for _ in range(9)]
        self.move_checking = True

        self.selecting = False
        self.selection = []
        self.selection_last = None

        self.notetaking = False
        self.notes = None
        self.init_notes()

        self.root = Tk()
        self.cellfont = Font(family="Terminus", size=24, weight="bold")
        self.notefont = Font(family="Terminus", size=8)

        self.game = SudokuGame(new_game=new_game, cell_size=cell_size)
        self.canvas = Canvas(self.game)
        self.initUI(self.game)
        self.initKeybinds()

    def initUI(self, game):
        game.master.title("Sudoku Game")
        game.pack(fill=BOTH, expand=1)
        self.canvas.pack(fill=BOTH, expand=1)

        self.draw_grid()
 
    def initKeybinds(self):
        self.root.bind('<Button-1>', self.on_press)
        self.root.bind('<ButtonRelease-3>', self.on_release_right)
        self.root.bind('<ButtonRelease-1>', self.on_release)
        self.root.bind('<Key>', self.on_key)
        self.root.bind('S', lambda e: self.game.solver.solve(self.game.board.board, generate=True))
        self.root.bind('s', lambda e: setattr(self, 'selection', list()))
        self.root.bind('R', self.restart_game)
        self.root.bind('C', self.check_solution)
        self.root.bind('c', lambda e: setattr(self, 'move_checking', not self.move_checking))
        self.root.bind('N', lambda e: self.game.solver.generate())
        self.root.bind('n', lambda e: setattr(self, 'notetaking', not self.notetaking))
        self.root.bind('<Escape>', self.quit)
        self.root.bind('<Motion>', self.motion)

    def init_notes(self):
        self.notes = [ [None for list in range(9)] for list in range(9) ]

        for i, r in enumerate(self.notes):
            for j, e in enumerate(r):
                self.notes[i][j] = {}
        
    def run(self):
        self.root.geometry("550x550+500+500")
        self.update()
        self.root.mainloop()

    def update(self):
        self.canvas.delete('all')
        self.draw_grid()

        if self.selecting and self.selection_last != self.current_pos:
            if self.current_pos not in self.selection:
                self.selection_last = self.current_pos
                self.selection.append(self.current_pos)
            else:
                self.selection_last = self.current_pos
                self.selection.remove(self.current_pos)

        self.root.after(13, self.update)

    def quit(self, event):
        self.root.quit()

    def draw_grid(self):
        o = [self.game.pos[0], self.game.pos[1]]

        for _i, c in enumerate(self.game.cells):
            i, j = _i // 9, _i % 9

            cell = list(c)
            value = self.game.board[i][j]
            notes = self.notes[i][j]
            
            # get cell center
            if value == 0:
                value = ' '
            center = [(cell[2] + cell[0]) / 2 , (cell[3] + cell[1]) / 2]

            # Color the cells based on the last move
            if self.current_pos is not None and self.current_pos[0] == i and self.current_pos[1] == j:
                self.hover = (i, j, 'grey')
                if self.last_move is not None:
                    if self.last_move:
                        self.filled = (i, j, 'green')
                    elif self.last_move == False:
                        self.filled = (i, j, 'red')

                    self.last_move = None

            # hover color
            filled = self.filled
            if self.hover[0] == i and self.hover[1] == j:
                filled = self.hover

            # draw selection
            for s in self.selection:
                if s[0] == i and s[1] == j:
                    filled = (i, j,'lightblue')
            
            # grid cell and value
            self.canvas.create_rectangle(cell[0], cell[1], cell[2], cell[3], fill=filled[2] if filled[0] == i and filled[1] ==  j else '', outline='black')
            self.canvas.create_text(center[0], center[1], font=self.cellfont, text=value)

            # self.canvas.create_text(center[0], center[1], font=self.notefont, text=f'{_i}:{i}, {j}')

            # notes
            for c in notes:
                addd = lambda x, y: (x[0] * y[0], x[1] * y[1])
                note_offset = addd(neighbors[int(c) - 1], (self.game.cell_size * .3, self.game.cell_size * .3))
                self.canvas.create_text(center[0]+note_offset[0], center[1]+note_offset[1], font=self.notefont, text=c, fill='darkblue')


        # Outlining square         
        self.canvas.create_rectangle((o[0]-self.game.cell_size*4.2), o[1] - self.game.cell_size*4.2, self.game.cells[-1][0]+self.game.cell_size*1.2, self.game.cells[-1][1]+self.game.cell_size*1.2)
 
    def restart_game(self, event):
        self.game.board.board = deepcopy(self.game.board.starting)
        self.init_notes()

    def motion(self, event):
        self.current_pos = self.game.get_closest_cell((event.x, event.y))

    def on_release(self, event):
        self.selecting = False
        self.current_pos = self.game.get_closest_cell((event.x, event.y))

    def on_release_right(self, event):
        self.selection = []

    def on_press(self, event):
        self.selecting = True

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
                    if len(self.selection) != 0:
                        for cell in self.selection:
                            if event.char not in self.notes[cell[0]][cell[1]]:
                                self.notes[cell[0]][cell[1]][event.char] = True
                            else:
                                del(self.notes[cell[0]][cell[1]][event.char])        
                    else:
                        if event.char not in self.notes[self.current_pos[0]][self.current_pos[1]]:
                            self.notes[self.current_pos[0]][self.current_pos[1]][event.char] = True
                        else:
                            del(self.notes[self.current_pos[0]][self.current_pos[1]][event.char])        

    def check_solution(self, event):
        for r1,r2 in zip(self.game.board.board, self.game.board.solution):
            for e, e2 in zip(r1, r2):
                if e != e2:
                    messagebox.showinfo(title="Sorry!", message="Not correct!")   
                    return        
        messagebox.showinfo(title="You win!", message="Congratulations!")