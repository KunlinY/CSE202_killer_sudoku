import numpy as np
from .DLX import DLX
from .Node import Node

class Sudoku:
    def solve(self, sudokArr):
        solver = DLX()
        solver.create_matrix(sudokArr)
        dlx_solution, found = solver.search()
        return dlx_solution, found

    # converts the quadruple linked list solution form back to numpy array
    def returnSol(self, solved, found, pretty = False, autoPrint = False):
        if not found:
            # if no solution is found then return a matrix consisting of entirely -1's
            # enforce -1.0 as otherwise returns an int numpy array for invalid solutions
            return np.full((9,9),-1.0)
        solution = [0] * 81
        for i in solved:
            solution[(i.row - 1) // 9] = i.row % 9 if i.row%9 != 0 else 9
        if pretty: # if the prettier view of the sudoku is required then pretty is set to true
            # disgusting list comprehension to print out the array in a more presentatble way. (converts to string, splits the string into rows, space seperated in 3's, then a new line on every third row)
            print("\n\n".join(["\n".join(["  ".join(" ".join([("".join(str(i) for i in solution))[i + j + k:i + j + k + 3] for i in range(0, 9, 3)])) for j in range(0, 27, 9)]) for k in range(0, 81, 27)]), end = "\n\n")
        # converts the 1d array solution to a 2d numpy array to be returned
        solNPA = np.asarray([[solution[i] for i in range(j,j+9)] for j in range(0,81,9)], dtype = np.float64)
        if autoPrint:
            print(solNPA)
        return solNPA

