import numpy as np
import sys
from project.Sudoku import Sudoku


def sudoku_solver(sudoku):
    sudoku = np.array(sudoku)
    s = Sudoku()
    solExample, fExample = s.solve(sudoku.astype(int))
    x = s.returnSol(solExample, fExample)
    return x

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) < 1:
        print("Please provide a sudoku as a file or plain text...")
    else:
        for arg in args:
            if arg[-4:] == ".txt":
                s = []
                with open(arg, "r") as f:
                    for line in f.readlines():
                        s.append([int(d) for d in [c for c in line] if d.isdigit()])
                print(sudoku_solver(np.array(s)))
            else:
                print(sudoku_solver(np.reshape(np.array([int(c) for c in arg if c.isdigit()]), (-1, 9))))
            print()

