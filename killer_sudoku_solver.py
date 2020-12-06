import time


def get_possible_combinations(length: int, min_value: int, max_value: int) -> list:
    """To construct the map from sum to possible values

    Args:
        length (int): max length of int list, usually N-1
        min_value (int): start value, usually 1 for the first call
        max_value (int): end value for generation, usually N+1 

    Yields:
        list of int: generated value list
    """

    for i in range(min_value, max_value):
        if i + 1 < max_value and length != 1:
            for v in get_possible_combinations(length - 1, i + 1, max_value):
                yield [i] + v
        yield [i]


class Cell:
    
    def __init__(self, value, is_fixed=False):
        self.value = value
        self.is_fixed = is_fixed
        self.tested_values = []
        self.candidates = set()

    def get_next_candidate(self) -> int:
        """Get the next available candidate from set, order not guaranteed

        Returns:
            int: next available candidate
        """

        if not self.is_fixed and len(self.candidates) > 0:
            for e in self.candidates:
                return e

        return -1

    def reset_values(self):
        """Reset all the values to the initial state for backtracing
        """

        if self.is_fixed:
            return

        while len(self.tested_values) > 0:
            self.candidates.add(self.tested_values.pop())

        self.value = 0

    def unset_value(self) -> bool:
        """Reset the last candidate being tried

        Returns:
            bool: if the operation succeed
        """

        if self.is_fixed:
            return False

        if self.value == 0:
            return True

        self.tested_values.pop()
        self.candidates.add(self.value)

        if len(self.tested_values) == 0:
            self.value = 0
        else: 
            self.value = self.tested_values[-1]
        return True

    def set_value(self, value: int) -> bool:
        """Set the cell to a certain value.

        If the cell is initialized, it would always return False
        If the value is not a valid candidate, it would return False
        It would only succeed when the value is in the candidate list

        Args:
            value (int): The number to be filled

        Returns:
            bool: if the operation succeed
        """
        
        if self.is_fixed or value not in self.candidates:
            return False
        
        self.value = value
        self.tested_values.append(value)
        self.candidates.remove(value)
        return True

class Board:

    def __init__(self, N: int, matrix: list, cage_constraints: list):

        # list all possible combinations for certain length and sum
        self.length_sum_candidates_map = dict([(l, {}) for l in range(2, N)])
        for v in get_possible_combinations(N - 1, 1, N + 1):
            l = len(v)
            s = sum(v)

            if l == 1:
                continue

            if s not in self.length_sum_candidates_map[l].keys():
                self.length_sum_candidates_map[l][s] = []

            self.length_sum_candidates_map[l][s].append(v)

        # initialize board with given matrix
        self._board = [[Cell(value, value != 0) for value in row] for row in matrix]

        # initialize cell candidates with cage constraints
        self.cell_cage_map = {}
        for s, cells in cage_constraints:
            l = len(cells)
            for cell in cells:
                if not self.__getitem__(cell).is_fixed:
                    self.__getitem__(cell).candidates = set(sum(self.length_sum_candidates_map[l][s], []))
                    self.cell_cage_map[cell] = (s, cells)

        # trim candidates based on given row, column and nonet constraints
        for row in range(1, N + 1):
            for col in range(1, N + 1):
                cell = self.__getitem__((row, col))
                if cell.is_fixed:
                    value = cell.value
                    for i in range(1, N  + 1):
                        # neighbour in the same column
                        neighbour = self.__getitem__((i, col))
                        if value in neighbour.candidates:
                            neighbour.candidates.remove(value)

                        # neighbour in the same row
                        neighbour = self.__getitem__((row, i))
                        if value in neighbour.candidates:
                            neighbour.candidates.remove(value)

                    nonet_row = int((row - 1) / 3) * 3 + 1
                    nonet_col = int((col - 1) / 3) * 3 + 1
                    for r in range(nonet_row, nonet_row + 3):
                        for c in range(nonet_col, nonet_col + 3):
                            neighbour = self.__getitem__((r, c))
                            if value in neighbour.candidates:
                                neighbour.candidates.remove(value)

    def fill_cell(self, index: tuple, value: int) -> bool:
        """Fill the cell.

        The cell would only be filled if it does not violate existing constraints.

        Args:
            index (tuple): the index of the cell
            value (int): the number to fill

        Returns:
            bool: if the operation succeed
        """

        cell = self.__getitem__(index)
        row, col = index

        if not cell:
            return False

        status = cell.set_value(value)

        if not status:
            return status

        for i in range(1, N + 1):
            neighbour = self.__getitem__((i, col))
            if neighbour.value == cell.value and i != row:
                return False

            neighbour = self.__getitem__((row, i))
            if neighbour.value == cell.value and i != col:
                return False

            nonet_row = int((row - 1) / 3) * 3 + 1
            nonet_col = int((col - 1) / 3) * 3 + 1
            for r in range(nonet_row, nonet_row + 3):
                for c in range(nonet_col, nonet_col + 3):
                    neighbour = self.__getitem__((r, c))
                    if neighbour.value == cell.value and r != row and c != col:
                        return False

        target_sum, cells = self.cell_cage_map[index]

        # if all other cells in this cage are filled, check the sum constraints
        # otherwise, fill the cage
        current_sum = 0
        for cell in cells:
            value = self.__getitem__(cell).value

            if value == 0:
                current_sum = -1
                break

            current_sum += value

        if current_sum < 0:
            return status
        
        if current_sum != target_sum:
            return False

        return True

    def __getitem__(self, index: int) -> Cell:
        """Get the cell by index. Return None if the index is not valid

        Args:
            index (int): index of the cell

        Returns:
            Cell: The cell
        """

        if index[0] <= N and index[1] <= N:
            return self._board[index[0] - 1][index[1] - 1]
        return None

    def print(self):
        """Helper function for printing the current value of the matrix
        """
        
        for row in self._board:
            for cell in row:
                print(cell.value, end="\t")
            print()


class SudokuPuzzle:

    N = 9
    
    def __init__(self, N, initial_matrix, cage_constraints):
        assert (len(initial_matrix) == N and all(len(row) == N for row in initial_matrix)), "Initial matrix size is invalid!"
        assert all(0 <= cell <= N for row in initial_matrix for cell in row), "Initial matrix value is invalid"
        
        SudokuPuzzle.N = N
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


if __name__ == "__main__":
    N = 9
    initial_matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    cage_constraints = [
        (3, [(1, 1), (1, 2)]),
        (15, [(1, 3), (1, 4), (1, 5)]),
        (22, [(1, 6), (2, 5), (2, 6), (3, 5)]),
        (4, [(1, 7), (2, 7)]),
        (16, [(1, 8), (2, 8)]),
        (15, [(1, 9), (2, 9), (3, 9), (4, 9)]),
        (25, [(2, 1), (2, 2), (3, 1), (3, 2)]),
        (17, [(2, 3), (2, 4)]),
        (9, [(3, 3), (3, 4), (4, 4)]),
        (8, [(3, 6), (4, 6), (5, 6)]),
        (20, [(3, 7), (3, 8), (4, 7)]),
        (6, [(4, 1), (5, 1)]),
        (14, [(4, 2), (4, 3)]),
        (17, [(4, 5), (5, 5), (6, 5)]),
        (17, [(4, 8), (5, 7), (5, 8)]),
        (13, [(5, 2), (5, 3), (6, 2)]),
        (20, [(5, 4), (6, 4), (7, 4)]),
        (12, [(5, 9), (6, 9)]),
        (27, [(6, 1), (7, 1), (8, 1), (9, 1)]),
        (6, [(6, 3), (7, 2), (7, 3)]),
        (20, [(6, 6), (7, 6), (7, 7)]),
        (6, [(6, 7), (6, 8)]),
        (10, [(7, 5), (8, 4), (8, 5), (9, 4)]),
        (14, [(7, 8), (7, 9), (8, 8), (8, 9)]),
        (8, [(8, 2), (9, 2)]),
        (16, [(8, 3), (9, 3)]),
        (15, [(8, 6), (8, 7)]),
        (13, [(9, 5), (9, 6), (9, 7)]),
        (17, [(9, 8), (9, 9)]),
    ]

    sudoku = SudokuPuzzle(N, initial_matrix, cage_constraints)
    sudoku.solve()
