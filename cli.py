import time

class CLI:
    """Manages the command-line interface for Super Tic Tac Toe."""
    
    def __init__(self, game):
        self.game = game

    def display_grid(self):
        """Display the Super Grid in the CLI."""
        super_grid = self.game.super_grid
        for gr in range(3):
            for row in range(3):
                row_cells = []
                for gc in range(3):
                    for col in range(3):
                        cell_value = super_grid.mini_grids[gr][gc].cells[row][col].value
                        row_cells.append(cell_value if cell_value is not None else '.')
                    if gc < 2:  # Add space between mini-grids, but not after the last one
                        row_cells.append(' ')
                print(' '.join(row_cells))
            if gr < 2:  # Add a newline between super grid rows, but not after the last one
                print()

    """def get_input_prev(self):
        "Get user input for a move."
        attempts = 0
        while attempts < 3:  # Limit attempts to avoid infinite loop in tests
            try:
                if self.game.next_grid:
                    prompt = f"Enter your move in grid {self.game.next_grid} (cell_row cell_col): "
                else:
                    prompt = "Enter your move (grid_row grid_col cell_row cell_col): "
                move = input(prompt).strip().split()
                if self.game.next_grid and len(move) == 2:
                    grid_row, grid_col = self.game.next_grid
                    cell_row, cell_col = map(int, move)
                elif len(move) == 4:
                    grid_row, grid_col, cell_row, cell_col = map(int, move)
                else:
                    raise ValueError("Invalid input. Please enter the correct number of integers.")
                if not (0 <= grid_row < 3 and 0 <= grid_col < 3 and 0 <= cell_row < 3 and 0 <= cell_col < 3):
                    raise ValueError("Input values must be between 0 and 2.")
                return grid_row, grid_col, cell_row, cell_col
            except ValueError as e:
                print(f"Error: {e}. Please try again.")
                attempts += 1
        return None, None, None, None"""
    
    def get_input(self, max_retries=5):
        retries = 0
        while retries < max_retries:
            try:
                move = input("Enter your move (grid_row grid_col cell_row cell_col): ").strip().split()
                if len(move) != 4:
                    raise ValueError("Invalid input. Please enter exactly four integers.")
                grid_row, grid_col, cell_row, cell_col = map(int, move)
                if not (0 <= grid_row < 3 and 0 <= grid_col < 3 and 0 <= cell_row < 3 and 0 <= cell_col < 3):
                    raise ValueError("Input values must be between 0 and 2.")
                return grid_row, grid_col, cell_row, cell_col
            except ValueError as e:
                print(f"Error: {e}. Please try again.")
                retries += 1
                if retries >= max_retries:
                    raise ValueError("Maximum retries exceeded. Please restart the input process.")
            time.sleep(0.1)

    def update(self):
        """Update the CLI display and show the current game state."""
        self.display_grid()
        print(self.game.get_game_state())

    def play(self):
        """Main loop for playing the game in the CLI."""
        while not self.game.super_grid.overall_winner and not self.game.is_draw():
            self.update()
            grid_row, grid_col, cell_row, cell_col = self.get_input()
            if grid_row is None:  # Handle break condition from get_input
                break
            self.game.play_turn(grid_row, grid_col, cell_row, cell_col)
            self.update()
        print(self.game.get_game_state())
        if input("Play again? (y/n): ").lower() == 'y':
            self.game.reset_game()
            self.play()
