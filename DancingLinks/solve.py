import numpy as np
import pandas as pd
import sys
from project.Sudoku import Sudoku


def sudoku_solver(sudoku):
    sudoku = np.array(sudoku)
    s = Sudoku()
    solExample, fExample, t = s.solve(sudoku.astype(int))
    # x = s.returnSol(solExample, fExample)
    return t

if __name__ == "__main__":

    normal_log = []
    for N in [4, 9, 16]:
        for p in range(5, 100, 5):
            p = float(p / 100.0)
            matrix = eval(open(f"../sudokus/{N}_{p:.2f}_normal.txt").read())

            print(N, p)

            for i in range(5):
                t = sudoku_solver(np.array(matrix))
                normal_log.append((N, p, t))

    log = pd.DataFrame(normal_log, columns=["N", "Non-Empty cell percentage", "Time"])
    log.to_csv("normal_dlx.csv")

    # args = sys.argv[1:]

    # if len(args) < 1:
    #     print("Please provide a sudoku as a file or plain text...")
    # else:
    #     for arg in args:
    #         if arg[-4:] == ".txt":
    #             s = []
    #             with open(arg, "r") as f:
    #                 for line in f.readlines():
    #                     s.append([int(d) for d in [c for c in line] if d.isdigit()])
    #             print(sudoku_solver(np.array(s)))
    #         else:
    #             print(sudoku_solver(np.reshape(np.array([int(c) for c in arg if c.isdigit()]), (-1, 9))))
    #         print()

