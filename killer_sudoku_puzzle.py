from sudoku_puzzle import SudokuPuzzle
import cage_member_calculator


class KillerSudokuPuzzle(SudokuPuzzle):
    class KillerRelation:
        def __init__(self, total_value, cells):
            self.total_value = total_value
            self.relatives = cells
            #self.set_cage_member_values()

        def set_cage_member_values(self):
            available_values = cage_member_calculator.get_cage_members(len(self.relatives), self.total_value)
            for cell in self.relatives:
                cell.available_values = available_values

        def have_relation(self, cell):
            return cell in self.relatives

        def check_relations(self, cell, solver):
            if self.have_relation(cell):
                assigned_relatives = [c for c in self.relatives if c.current_value != 0]
                if len(self.relatives) == len(assigned_relatives):
                    if sum([v.current_value for v in self.relatives]) != self.total_value:
                        return False
                    else:
                        return True
                if len(self.relatives) > len(assigned_relatives):
                    if sum([v.current_value for v in self.relatives]) >= self.total_value:
                        return False
            return True

    def __init__(self, initial_values):
        self.killer_relations = []
        SudokuPuzzle.__init__(self, initial_values)

    def parse_puzzle(self, (initial_values, killer_relations)):
        SudokuPuzzle.parse_puzzle(self, initial_values)
        for killer_relation in killer_relations:
            total_value, relatives = killer_relation
            self.killer_relations.append(
                KillerSudokuPuzzle.KillerRelation(total_value, [self.cells.get(c_id) for c_id in relatives]))

    def check_relatives(self, cell, solver):
        if cell.current_value:
            if SudokuPuzzle.check_relatives(self, cell, solver):
                for killer_relation in self.killer_relations:
                    if not killer_relation.check_relations(cell, solver):
                        return False
                return True
        return False

    def verify_relatives(self):
        all = set([])
        for killer_relation in self.killer_relations:
            for relative in killer_relation.relatives:
                all.add(relative)
        print(len(all))
        assert len(all) == 81
