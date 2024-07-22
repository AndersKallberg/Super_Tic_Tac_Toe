from mini_grid import MiniGrid

class SuperGrid:
    """Represents the main 3x3 grid of mini-grids in Super Tic Tac Toe."""
    
    def __init__(self):
        self.mini_grids = [[MiniGrid() for _ in range(3)] for _ in range(3)]
        self.overall_winner = None
        self.winning_line = None

    def check_overall_winner(self):
        """Check if there is an overall winner in the Super Grid."""
        for i in range(3):
            if self.mini_grids[i][0].winner == self.mini_grids[i][1].winner == self.mini_grids[i][2].winner and self.mini_grids[i][0].winner is not None:
                self.overall_winner = self.mini_grids[i][0].winner
                self.winning_line = ('row', i)
                return
            if self.mini_grids[0][i].winner == self.mini_grids[1][i].winner == self.mini_grids[2][i].winner and self.mini_grids[0][i].winner is not None:
                self.overall_winner = self.mini_grids[0][i].winner
                self.winning_line = ('col', i)
                return

        if self.mini_grids[0][0].winner == self.mini_grids[1][1].winner == self.mini_grids[2][2].winner and self.mini_grids[0][0].winner is not None:
            self.overall_winner = self.mini_grids[0][0].winner
            self.winning_line = ('diag', 1)
            return
        if self.mini_grids[0][2].winner == self.mini_grids[1][1].winner == self.mini_grids[2][0].winner and self.mini_grids[0][2].winner is not None:
            self.overall_winner = self.mini_grids[0][2].winner
            self.winning_line = ('diag', 2)
            return

    def make_move(self, grid_row, grid_col, cell_row, cell_col, player):
        """Make a move in the Super Grid."""
        if self.mini_grids[grid_row][grid_col].make_move(cell_row, cell_col, player):
            self.check_overall_winner()
            return True
        return False
