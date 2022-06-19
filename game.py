from tkinter import Tk, Canvas, Frame, BOTH

from board import SudokuBoard


class SudokuApp():
    def __init__(self, new_game=True, nhints=60, cell_size=50):
        self.root = Tk()
        self.game = SudokuGame(new_game=True, nhints=60, cell_size=50)

    def run(self):
        self.root.geometry("550x550+500+500")
        self.root.mainloop()


class SudokuGame(Frame):
    def __init__(self, new_game=True, nhints=60, cell_size=50):        
        super().__init__()

        self.board = SudokuBoard(new_game=new_game, nhints=nhints,)
        self.cell_size = cell_size
        self.pos = (self.cell_size*5, self.cell_size*5)
        self.cells = self.get_cell_offsets()

        self.initUI()

    def initUI(self):
        self.master.title("Sudoku Game")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        self.draw_grid(canvas)

        canvas.pack(fill=BOTH, expand=1)

    def draw_grid(self, canvas):
        o = [self.pos[0], self.pos[1]]

        for i, cell in enumerate(self.cells):
            value = self.board[i // 9][i % 9]
            if value == 0:
                value = ' '
                
            center = (cell[2] + cell[0]) / 2, (cell[3] + cell[1]) / 2
            canvas.create_rectangle(cell[0], cell[1], cell[2], cell[3], fill='', outline='black')
            canvas.create_text(center[0], center[1], font="Calibri 40 bold", text=value)
        canvas.create_rectangle((o[0]-self.cell_size*4.2) , o[1] - self.cell_size*4.2, self.cells[-1][0]+self.cell_size*1.1, self.cells[-1][1]+self.cell_size*1.1)

    def get_cell_offsets(self):
        o = [self.pos[0], self.pos[1]]

        offsets = []
        for i in self.board.neighbors:
            off = o[0] + ((i[0]*self.cell_size*3.1)), o[1] + ((i[1]*self.cell_size*3.1))
            for j in self.board.neighbors:
                off2 = off[0] + (j[0]*self.cell_size), off[1] + (j[1]*self.cell_size)
                cell = off2[0], off2[1], off2[0]+self.cell_size, off2[1]+self.cell_size
                offsets.append(cell)
        return offsets


