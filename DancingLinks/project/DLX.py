import numpy as np
from .Node import Node

class DLX:
    def __init__(self):
        self.head = Node(None,0)
        # lambda functions that define the constraints on the sudoku
        # value is the value passed to the function and itemIndex is the unique value index in the 81 boxes
        self.row_constraint = lambda itemIndex, value: 81 + (itemIndex // 9) * 9 + value
        self.col_constraint = lambda itemIndex, value: 162 + (itemIndex % 9) * 9 + value
        self.box_constraint = lambda itemIndex, value: 243 + (itemIndex // 27) * 27 + (itemIndex % 9) // 3 * 9 + value

    # creates an exact cover matrix of a sudoku grid
    def create_matrix(self, sudokArr):
        head = self.head
        cols = [head] # store the column headers in a list for easier access
        # Construct column headers as a doubly circular linked list
        for i in range(324): # the number of columns for a 9x9 matrix given the 4 constraints (4*9*9)
            current = Node(i+1, None)
            current.right = head # re-do the new column loop back to the head column
            current.left = head.left
            head.left.right = current
            head.left = current
            cols.append(current)

        # iterates through each value in the sudoku
        for row in range(len(sudokArr)):
            for chr in range(9):
                # takes the unique positional id of the value in the sudoku
                chrID = row*9 + chr
                # if the value is 0 then there is no given value and links for the possibilities at that position are created.
                if sudokArr[row][chr] == 0:
                    for j in range(9):
                        self.createNodeLinks(chrID, j+1, cols)
                else:
                    self.createNodeLinks(chrID, sudokArr[row][chr], cols)

    # for each possible value of the sudoku that is not yet found, createLinks creates links based on the sudoku constraints for each value
    # and then adds the links to the DLX structure re-assigning links so that the structure is maintained.
    def createNodeLinks(self, index, value, cols):
        # Node(col, row)
        cellNode = Node(cols[index + 1], index*9 + value)
        rowNode = Node(cols[self.row_constraint(index, value)], index*9 + value)
        colNode = Node(cols[self.col_constraint(index, value)], index*9 + value)
        areaNode = Node(cols[self.box_constraint(index, value)], index*9 + value)

        # Link all the nodes into a single row in the form of a doubly linked list
        cellNode.right, cellNode.left = rowNode, areaNode
        rowNode.right, rowNode.left = colNode, cellNode
        colNode.right, colNode.left = areaNode, rowNode
        areaNode.right, areaNode.left = cellNode, colNode

        # for each node, appends the node to the end of the right column and deals with re-assigning the pointers so
        # that the quadruple linked list structure is maintained
        for i in [cellNode, rowNode, colNode, areaNode]:
            i.column.rowCount +=1
            i.down = i.column
            i.up = i.column.up
            i.column.up.down = i
            i.column.up = i

    #   x.left.right = x.right;
    #   x.right.left = x.left;
    # the cover method removes a column, as well as all the rows that intersect with the column
    # the removal of the column leaves the removed columns pointers untouched such that the column can then be
    # re-added or "uncovered"
    def cover(self, column):
        # assigns the column node to the left to point to the column node to the right of the current column and vica versa
        column.right.left = column.left
        column.left.right = column.right
        currentColNode = column.down # take the first non column head node in the column
        # iterate through each node in the covered column
        while currentColNode != column:
            # iterate through all nodes on the current row and unlink them
            currentRowNode = currentColNode.right
            while currentRowNode != currentColNode:
                # the item on the row is unlinked from its owning column with its own pointers unaffected
                currentRowNode.down.up = currentRowNode.up
                currentRowNode.up.down = currentRowNode.down
                currentRowNode.column.rowCount -= 1 # reduce row count
                currentRowNode = currentRowNode.right
            currentColNode = currentColNode.down # take next node in column

    # essentially the inverse of the cover method
    def uncover(self, column):
        currentColNode = column.up # get the last item of column backward from the head
        # iterate through each node in the column from bottom to head
        while currentColNode != column:
            currentRowNode = currentColNode.left
            # iterate through each node row, re-joining the links that were previously removed.
            while currentRowNode != currentColNode:
                currentRowNode.down.up = currentRowNode
                currentRowNode.up.down = currentRowNode
                currentRowNode.column.rowCount += 1
                currentRowNode = currentRowNode.left
            currentColNode = currentColNode.up
        column.right.left = column
        column.left.right = column

    # search for a solution with DLX-style search - this is essentially donald knuths recursive algorithm X
    def search(self, solution = []):
        # If the root node loops to itself then all columns have been removed and a solution has been found
        if self.head == self.head.right:
            return (solution, True)
        # chooses the linked list column with the least number of members (knuth calls it the s heuristic)
        leastCol = None
        currentColNode = self.head.right
        s = 99999 # starting value for the s heuristic is high to find min
        # iterate through the column head nodes until return back to the start head node
        while currentColNode != self.head:
            if currentColNode.rowCount < s:
                leastCol = currentColNode
                s = currentColNode.rowCount
            currentColNode = currentColNode.right
        # cover the column with the least number of nodes below
        self.cover(leastCol)
        # iterate through each column value in the column with the least members
        curNodeDown = leastCol.down
        while curNodeDown != leastCol: # while the current down node hasnt looped back to the starting node in the col
            solution.append(curNodeDown) # add the current column node to the solution
            # curNodeLat = current lateral node (either left or right dependant on cover or uncover)
            curNodeLat = curNodeDown.right # get the node to the right side of the current column node
            while curNodeLat != curNodeDown: # while the lateral node hasnt returned back to the column node
                # cover the column and intersections for the current lateral node.
                self.cover(curNodeLat.column)
                curNodeLat = curNodeLat.right
            # Algorithm x baseline recursive call on current solution
            solution, found = self.search(solution)
            if found:
                return (solution, True)
            # backtracking and uncover if solution is not found - pop from current solution
            curNodeDown = solution.pop()
            leastCol = curNodeDown.column
            curNodeLat = curNodeDown.left
            # uncover in order to backtrack and try different solution route
            while curNodeLat != curNodeDown: # while the lateral node hasnt returned back to the column node
                self.uncover(curNodeLat.column)
                curNodeLat = curNodeLat.left
            curNodeDown = curNodeDown.down
        # uncover the column
        self.uncover(leastCol)
        return (solution, False)

