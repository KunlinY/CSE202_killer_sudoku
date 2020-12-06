import time

from cell import Cell
from board import Board


class KillerSudoku:

    N = 9
    
    def __init__(self, N, initial_matrix, cage_constraints):
        assert (len(initial_matrix) == N and all(len(row) == N for row in initial_matrix)), "Initial matrix size is invalid!"
        assert all(0 <= cell <= N for row in initial_matrix for cell in row), "Initial matrix value is invalid"
        
        KillerSudoku.N = N
        self.board = Board(N, initial_matrix, cage_constraints)
        self.back_track_count = 0

    def solve(self):
        start = time.process_time()
        result = self.solve_index((1, 1))
        t = time.process_time() - start
        self.board.print()

        if result:
            print("Solution found!")
        else:
            print("No solution!")
        print("Time elapse: ", t)

    def solve_index(self, index):
        cell = self.board[index]
        next_index = (index[0], index[1] + 1) if index[1] != self.N else (index[0] + 1, 1)
        while True:
            
            if cell == None:
                return True

            if cell.is_fixed:
                if self.board[next_index]:
                    return self.solve_index(next_index)
                else:
                    return True

            else:
                candidate = cell.get_next_candidate()

                if candidate < 0:
                    break

                status = self.board.fill_cell(index, candidate)
                if status:
                    # print("Set value at index ", index, candidate)
                    # print("Starting next index ", next_index)
                    # self.board.print()
                    if self.solve_index(next_index):
                        return True

        self.back_track_count += 1
        cell.reset_values()
        return False
