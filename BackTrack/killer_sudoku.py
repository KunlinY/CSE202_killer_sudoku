import time

from cell import Cell
from board import Board


class KillerSudoku:

    N = 9
    
    def __init__(self, N, initial_matrix, cage_constraints, pre_sum=True):
        assert (len(initial_matrix) == N and all(len(row) == N for row in initial_matrix)), "Initial matrix size is invalid!"
        assert all(0 <= cell <= N for row in initial_matrix for cell in row), "Initial matrix value is invalid"
        
        KillerSudoku.N = N
        self.board: Board = Board(N, initial_matrix, cage_constraints, pre_sum)
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
        print("Back track count ", self.back_track_count)
        return t

    def solve_index(self, index):
        cell = self.board[index]
            
        # The end of the search
        if cell == None:
            return True

        next_index = (index[0], index[1] + 1) if index[1] < self.N else (index[0] + 1, 1)
        while True:

            if cell.is_fixed:
                # If the cell is initialized, move to next cell
                return self.solve_index(next_index)
            else:
                candidate = cell.get_next_candidate()

                if candidate < 0:
                    # No available candidates, break to back track
                    break

                status = self.board.fill_cell(index, candidate)
                if status and self.solve_index(next_index):
                    return True

        self.back_track_count += 1
        cell.reset_values()

        if self.back_track_count % 500000 == 0:
            print("back tracking", self.back_track_count)
            self.board.print()

        if self.back_track_count >= 10000000:
            return False

        return False
