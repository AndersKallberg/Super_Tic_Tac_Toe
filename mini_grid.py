from cell import Cell

class MiniGrid:
    """Represents a 3x3 mini-grid in Super Tic Tac Toe."""
    
    def __init__(self):
        self.cells = [[Cell() for _ in range(3)] for _ in range(3)]
        self.winner = None

    def is_finished(self):
        return self.winner is not None or self.is_full()

    def is_full(self):
        """Check if the mini-grid is full."""
        return all(cell.value is not None for row in self.cells for cell in row)

    def get_winner(self):
        return self.winner

    def check_winner(self):
        """Check if there is a winner in the mini-grid."""
        for i in range(3):
            if self.cells[i][0].value == self.cells[i][1].value == self.cells[i][2].value and self.cells[i][0].value is not None:
                self.winner = self.cells[i][0].value
                return
            if self.cells[0][i].value == self.cells[1][i].value == self.cells[2][i].value and self.cells[0][i].value is not None:
                self.winner = self.cells[0][i].value
                return

        if self.cells[0][0].value == self.cells[1][1].value == self.cells[2][2].value and self.cells[0][0].value is not None:
            self.winner = self.cells[0][0].value
            return
        if self.cells[0][2].value == self.cells[1][1].value == self.cells[2][0].value and self.cells[0][2].value is not None:
            self.winner = self.cells[0][2].value
            return

    def make_move(self, row, col, player):
        """Make a move in the mini-grid."""
        if self.cells[row][col].is_empty():
            self.cells[row][col].set_value(player)
            self.check_winner()
            return True
        return False
