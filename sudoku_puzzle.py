class SudokuPuzzle:

    def __init__(self, initial_values):
        self.cells = {}
        self.parse_puzzle(initial_values)
        self.set_relatives()
        self.print_()

    def parse_puzzle(self, initial_values):
        cells = {}

        if initial_values is None:
            for r in range(1, 10):
                for c in range(1, 10):
                    cells.update({(r, c): Cell(r, c, 0)})
        else:
            initial_values = list(initial_values)
            assert len(initial_values) == 81
            for r in range(1, 10):
                for c in range(1, 10):
                    initial_val = initial_values[(((r - 1) * 9) + (c - 1))]
                    cells.update({(r, c): Cell(r, c, int(initial_val))})
        self.cells = cells

    def set_relatives(self):
        self.set_original_relations()

    def check_relatives(self, cell, solver):
        return cell.check_relatives(solver)

    def set_original_relations(self):
        for r in range(1, 10):
            for c in range(1, 10):
                cell = self.cells.get((r, c))
                for i in range(1, 10):
                    # belonging row
                    cell.relatives.add(self.cells.get((r, i)))
                    # belonging column
                    cell.relatives.add(self.cells.get((i, c)))

                # belonging 3x3
                belonging_3x3_r = int((r - 1) / 3)
                belonging_3x3_c = int((c - 1) / 3)
                for rr in range(belonging_3x3_r * 3 + 1, belonging_3x3_r * 3 + 4):
                    for cc in range(belonging_3x3_c * 3 + 1, belonging_3x3_c * 3 + 4):
                        cell.relatives.add(self.cells.get((rr, cc)))

                cell.relatives.remove(cell)

    def get_next_cell(self, cell):
        return self.cells.get((cell.row, cell.col + 1) if cell.col < 9 else (cell.row + 1, 1))

    def print_(self):
        for r in range(1, 10):
            for c in range(1, 10):
                print ("%s%s" % (self.cells.get((r, c)).current_value, " " if c % 3 == 0 else "")),
            if r % 3 == 0:
                print("")
            print("")
        print("-------------------")
        return self


class Cell:
    candidates = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, row, col, init_value):
        self.row = row
        self.col = col
        self.current_value = init_value
        self.tested_values = []
        self.available_values = [] if init_value != 0 else Cell.candidates
        self.relatives = set([])

    def get_index(self):
        return self.row, self.col

    def set_next_value(self):
        if len(self.available_values) > 0:
            self.tested_values.append(self.current_value)
            self.current_value = self.available_values.pop()
            return True
        return False

    def reset_values(self):
        for i in range(len(self.tested_values)):
            self.available_values.append(self.current_value)
            self.current_value = self.tested_values.pop()

    def check_relatives(self, solver):
        if self.current_value:
            for relative in self.relatives:
                solver.compare_count += 1
                if self.current_value == relative.current_value:
                    return False
                if len(relative.available_values) == 0 and self.current_value in relative.available_values:
                    return False
            return True
        return False

    def __str__(self):
        print_elems = [('row', self.row),
                       ('col', self.col),
                       ('current_value', self.current_value),
                       ('available_values', self.available_values),
                       ('tested_values', self.tested_values)]
        return ', '.join("%s: %s" % item for item in print_elems)

    def __repr__(self):
        return self.__str__()
