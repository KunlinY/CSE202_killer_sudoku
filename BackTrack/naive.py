from collections import defaultdict
import math
import time

'''
Usage: 
In any other file: 
    from naive import NaiveSolution
    
    S = NaiveSolution()
    S.solveSudoku(initial_matrix,cage_constraints)
'''


class NaiveSolution:
    def solveSudoku(self, board,cages):

        def createCageDict(cages):
            valueList = []
            res = {}
            for i in range(len(cages)):
                valueList.append(cages[i][0])
                for cage in cages[i][1]:
                    res[cage] = i
            return res,valueList
        def could_place(d, row, col):
            cageIndex = cages_constraints[(row+1, col+1)]
            return not (d in rows[row] or d in columns[col] or d in boxes[box_index(row, col)] or d in cages_new[cageIndex] or sum(cages_new[cageIndex])+d > cage_values[cageIndex] )

        def place_number(d, row, col):
            rows[row][d] += 1
            columns[col][d] += 1
            boxes[box_index(row, col)][d] += 1
            cageIndex = cages_constraints[(row+1, col+1)]
            cages_new[cageIndex][d]+=1
            board[row][col] = d

        def remove_number(d, row, col):
            del rows[row][d]
            del columns[col][d]
            del boxes[box_index(row, col)][d]
            cageIndex = cages_constraints[(row+1, col+1)]
            del cages_new[cageIndex][d]
            board[row][col] = 0

        def place_next_numbers(row, col):
            if col == N - 1 and row == N - 1:
                nonlocal sudoku_solved
                sudoku_solved = True
            else:
                if col == N - 1:
                    backtrack(row + 1, 0)
                else:
                    backtrack(row, col + 1)

        def backtrack(row=0, col=0):
            if board[row][col] == 0:
                for d in range(1, N+1):
                    if could_place(d, row, col):
                        place_number(d, row, col)
                        place_next_numbers(row, col)
                        if not sudoku_solved:
                            remove_number(d, row, col)
            else:
                place_next_numbers(row, col)

        starttime = time.time()

        # box size
        n = int(math.sqrt(len(board)))
        # row size
        N = n * n
        # lambda function to compute box index
        box_index = lambda row, col: (row // n) * n + col // n

        # init rows, columns and boxes
        rows = [defaultdict(int) for i in range(N)]
        columns = [defaultdict(int) for i in range(N)]
        boxes = [defaultdict(int) for i in range(N)]
        cages_new = [defaultdict(int) for i in range(len(cages))]
        cages_constraints, cage_values =  createCageDict(cages)


        for i in range(N):
            for j in range(N):
                if board[i][j] != 0:
                    d = int(board[i][j])
                    place_number(d, i, j)

        sudoku_solved = False
        backtrack()
        print("time(seconds):",time.time() - starttime)
        print("solution:", board)
