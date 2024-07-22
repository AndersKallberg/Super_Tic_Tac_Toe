class Cell:
    """Represents a single cell in a Tic Tac Toe grid."""
    
    def __init__(self):
        self.value = None  # None, 'X', or 'O'

    def is_empty(self):
        """Check if the cell is empty."""
        return self.value is None

    def set_value(self, value):
        """Set the value of the cell."""
        if self.is_empty():
            self.value = value
