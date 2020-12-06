from cell import Cell

class Board:

    def __init__(self, N: int, matrix: list, cage_constraints: list):

        self.N = N

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

        for i in range(1, self.N + 1):
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

        if index[0] <= self.N and index[1] <= self.N:
            return self._board[index[0] - 1][index[1] - 1]
        return None

    def print(self):
        """Helper function for printing the current value of the matrix
        """

        for row in self._board:
            for cell in row:
                print(cell.value, end="\t")
            print()


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
