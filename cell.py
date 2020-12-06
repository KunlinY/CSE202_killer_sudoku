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
