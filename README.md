# Sudoku 
Features:
* Solver-Generator
* Tkinter GUI (Overly simplistic at the moment.)


## Solver
Currently uses a simple backtracking algorithm that just checks if a value has been used in the rows, columns, and nonets.

## Interface
No keybinds yet, here's the code:

    self.root.bind('<ButtonRelease-1>', self.on_click)
    self.root.bind('<Key>', self.on_key)
    self.root.bind('S', self.solve_game)
    self.root.bind('R', lambda e: setattr(self.game.board, 'board', deepcopy(self.game.board.starting)))
    self.root.bind('C', self.check_solution)
    self.root.bind('N', lambda e: self.game.board.new_game(nhints=17))
    self.root.bind('<Escape>', self.quit)

![Sudoku TkGUI](screenshots/board.png)