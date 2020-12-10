import numpy as np

class Node:
    def __init__(self, column = None, row = None):
        if row is None:
            self.column = column
            self.row = self
            self.rowCount = 0
        else:
            self.column = column
        self.row = row
        self.up = self
        self.down = self
        self.left = self
        self.right = self
