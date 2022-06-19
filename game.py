from tkinter import Tk, Canvas, Frame, BOTH
import math

from board import SudokuBoard


class SudokuApp():
    def __init__(self, new_game=True, nhints=60, cell_size=50):
        self.root = Tk()
        self.game = SudokuGame(new_game=new_game, nhints=nhints, cell_size=cell_size)
        self.canvas = self.initUI(self.game, Canvas(self.game))

        self.root.bind('<ButtonRelease-1>', self.on_click)
        self.root.bind('<Key>', self.on_key)

        self.current_pos = None


    def initUI(self, game, canvas):
        game.master.title("Sudoku Game")
        game.pack(fill=BOTH, expand=1)

        canvas = Canvas(game)
        self.draw_grid(canvas)

        canvas.pack(fill=BOTH, expand=1)

        return canvas
     
    def draw_grid(self, canvas):
        o = [self.game.pos[0], self.game.pos[1]]

        for i, cell in enumerate(self.game.cells):
            value = self.game.board[i // 9][i % 9]
            if value == 0:
                value = ' '
                
            center = (cell[2] + cell[0]) / 2 , (cell[3] + cell[1]) / 2
            canvas.create_rectangle(cell[0], cell[1], cell[2], cell[3], fill='', outline='black')
            canvas.create_text(center[0], center[1], font="Calibri 40 bold", text=value)
        canvas.create_rectangle((o[0]-self.game.cell_size*4.2) , o[1] - self.game.cell_size*4.2, self.game.cells[-1][0]+self.game.cell_size*1.1, self.game.cells[-1][1]+self.game.cell_size*1.1)
     
    def run(self):
        self.root.geometry("550x550+500+500")
        self.update()
        self.root.mainloop()

    def update(self):
        self.draw_grid(self.canvas)
        self.root.after(16, self.update)

    def on_click(self, event):
        closest = 1000
        for i, cell in enumerate(self.game.cells):
            center = (cell[2] + cell[0]) / 2 , (cell[3] + cell[1]) / 2

            distance = lambda a, b: math.sqrt( ((a.x - b[0])**2 - self.game.cell_size / 2) + ((a.y - b[1])**2 - self.game.cell_size / 2) )
            
            dist = None
            try:
                dist = distance(event, center)
            except ValueError:
                dist = distance(event, cell)

            if dist < closest:
                closest = dist
                self.current_pos = i // 9, i % 9
        
        print(self.current_pos)

    def on_key(self, event):
        if event.char.isdigit() and self.current_pos is not None:
            self.game.board[self.current_pos[0]][self.current_pos[1]] = event.char

            print(event.char)
    


class SudokuGame(Frame):
    def __init__(self, new_game=True, nhints=60, cell_size=50):        
        super().__init__()

        self.board = SudokuBoard(new_game=new_game, nhints=nhints)
        self.cell_size = cell_size
        self.pos = (self.cell_size*5, self.cell_size*5)
        self.cells = self.get_cell_offsets()

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


