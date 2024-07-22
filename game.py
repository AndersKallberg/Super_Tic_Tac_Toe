import json
from super_grid import SuperGrid

class Game:
    """Manages the game logic and flow for Super Tic Tac Toe."""

    def __init__(self):
        self.super_grid = SuperGrid()
        self.current_player = 'X'
        self.next_grid = None  # This will hold the index of the next mini-grid
        self.highlight_super_grid = False
        self.players = {'X': 'human', 'O': 'human'}  # Default to human players

    def set_player_type(self, player, player_type):
        """Set the type of player (human or ai)."""
        if player in self.players:
            self.players[player] = player_type

    def is_player_human(self, player):
        """Check if the specified player is human."""
        return self.players.get(player, 'human') == 'human'

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def validate_move(self, grid_row, grid_col, cell_row, cell_col):
        """Validate a move."""
        if self.super_grid.overall_winner is not None:
            return False  # Game already won
        if self.next_grid:
            # If next_grid is set, ensure the move is in the correct mini-grid or allow free placement if the mini-grid is finished
            next_grid_row, next_grid_col = self.next_grid
            if (grid_row, grid_col) != (next_grid_row, next_grid_col):
                if self.super_grid.mini_grids[next_grid_row][next_grid_col].is_finished():
                    # Allow free placement if the mini-grid is finished
                    return True
                else:
                    return False  # Not the correct mini-grid
        if self.super_grid.mini_grids[grid_row][grid_col].winner is not None:
            return False  # Mini-grid already won
        if not self.super_grid.mini_grids[grid_row][grid_col].cells[cell_row][cell_col].is_empty():
            return False  # Cell already taken
        return True

    def play_turn(self, grid_row, grid_col, cell_row, cell_col):
        """Play a turn."""
        if self.validate_move(grid_row, grid_col, cell_row, cell_col):
            if self.super_grid.make_move(grid_row, grid_col, cell_row, cell_col, self.current_player):
                if self.super_grid.overall_winner is None:
                    # Check if the mini-grid is finished
                    if self.super_grid.mini_grids[cell_row][cell_col].is_finished():
                        self.next_grid = None  # Allow free placement
                    else:
                        self.next_grid = (cell_row, cell_col)
                    self.switch_player()
                return True
        return False

    def is_draw(self):
        """Check if the game is a draw."""
        if self.super_grid.overall_winner is not None:
            return False
        return all(
            mini_grid.is_full() or mini_grid.winner is not None
            for row in self.super_grid.mini_grids
            for mini_grid in row
        )
    
    def get_winner(self):
        """Return the winner of the game ('X' or 'O') if there is one, otherwise None."""
        if self.super_grid.overall_winner:
            return self.super_grid.overall_winner
        return None
    
    def get_game_state(self):
        """Get the current state of the game."""
        if self.super_grid.overall_winner:
            return f"Player {self.super_grid.overall_winner} wins!"
        elif self.is_draw():
            return "The game is a draw!"
        else:
            return f"Player {self.current_player}'s turn."

    def save_game(self, filename):
        """Save the game state to a file."""
        game_state = {
            'super_grid': []
        }
        
        for row in self.super_grid.mini_grids:
            grid_row = []
            for mini_grid in row:
                grid_cells = []
                for cell_row in mini_grid.cells:
                    row_cells = [cell.value for cell in cell_row]
                    grid_cells.append(row_cells)
                grid_row.append({
                    'cells': grid_cells,
                    'winner': mini_grid.winner
                })
            game_state['super_grid'].append(grid_row)
        
        game_state['current_player'] = self.current_player
        game_state['next_grid'] = self.next_grid
        
        with open(filename, 'w') as f:
            json.dump(game_state, f)

    def load_game(self, filename):
        """Load the game state from a file."""
        with open(filename, 'r') as f:
            game_state = json.load(f)
        for gr in range(3):
            for gc in range(3):
                mini_grid_state = game_state['super_grid'][gr][gc]
                for row in range(3):
                    for col in range(3):
                        cell_value = mini_grid_state['cells'][row][col]
                        self.super_grid.mini_grids[gr][gc].cells[row][col].value = cell_value
                self.super_grid.mini_grids[gr][gc].winner = mini_grid_state['winner']
        self.current_player = game_state['current_player']
        self.next_grid = game_state['next_grid']

    def reset_game(self):
        """Reset the game state."""
        self.super_grid = SuperGrid()
        self.current_player = 'X'
        self.next_grid = None  # This will hold the index of the next mini-grid
        self.highlight_super_grid = False