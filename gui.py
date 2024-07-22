import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.freetype  # For text rendering
import time

class GUI:
    """Manages the graphical user interface for Super Tic Tac Toe."""

    def __init__(self, game):
        self.game = game
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        self.font = pygame.freetype.SysFont(None, 36)
        self.info_font = pygame.freetype.SysFont(None, 48)
        self.large_symbol_alpha = 128  # Transparency level (0-255)
        self.mode = None  # Game mode (PvP, PvE, EvE)
        self.running = True
        
        # Button for the Play Again screen
        self.play_again_button = pygame.Rect(150, 350, 300, 100)  # Position and size of the button

    def create_buttons(self):
        """Create buttons for game mode selection."""
        return {
            'PvP': pygame.Rect(150, 50, 300, 100),
            'PvE': pygame.Rect(150, 200, 300, 100),
            'EvE': pygame.Rect(150, 350, 300, 100)
        }

    def draw_menu(self):
        """Draw the main menu with buttons for PvP and PvE."""
        self.screen.fill((255, 255, 255))  # Clear screen with white
        for label, rect in self.create_buttons().items():
            pygame.draw.rect(self.screen, (0, 0, 255), rect)
            text_surface, _ = self.font.render(label, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def handle_menu_click(self, pos):
        """Handle clicks on the menu to select game mode."""
        for label, rect in self.create_buttons().items():
            if rect.collidepoint(pos):
                self.mode = label
                return True
        return False

    def draw_grid(self):
        """Draw the Super Grid and current game state."""
        for grid_row in range(3):
            for grid_col in range(3):
                mini_grid = self.game.super_grid.mini_grids[grid_row][grid_col]
                self.draw_mini_grid(grid_row, grid_col, mini_grid)

        # Draw the large symbol after the cells to ensure it appears on top
        for grid_row in range(3):
            for grid_col in range(3):
                mini_grid = self.game.super_grid.mini_grids[grid_row][grid_col]
                if mini_grid.winner:
                    self.draw_large_symbol(grid_row, grid_col, mini_grid.winner)

        # Draw the large green outline if the player can pick any mini-grid
        if self.can_pick_any_mini_grid():
            self.draw_supergrid_outline()

        if self.game.super_grid.overall_winner:
            self.draw_winning_lines()

        if self.game.next_grid:
            grid_x = self.game.next_grid[1] * 200
            grid_y = self.game.next_grid[0] * 200
            pygame.draw.rect(self.screen, (0, 255, 0), (grid_x, grid_y, 200, 200), 3)

    def draw_mini_grid(self, grid_row, grid_col, mini_grid):
        """Draw individual mini-grid including cell contents and highlight."""
        for cell_row in range(3):
            for cell_col in range(3):
                x = grid_col * 200 + cell_col * 60 + 10
                y = grid_row * 200 + cell_row * 60 + 10
                rect = pygame.Rect(x, y, 60, 60)

                # Draw the cell with a solid color
                pygame.draw.rect(self.screen, (255, 255, 255), rect)  # Background for cells
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)    # Cell border
                
                # Draw the cell's content
                cell_value = mini_grid.cells[cell_row][cell_col].value
                if cell_value:
                    text_surface, _ = self.font.render(cell_value, (0, 0, 0))
                    self.screen.blit(text_surface, (x + 20, y + 10))

        # Draw the large symbol for the completed mini-grid
        if mini_grid.winner:
            self.draw_large_symbol(grid_row, grid_col, mini_grid.winner)
        
        # Highlight the mini-grid if it is finished
        if mini_grid.is_finished():
            self.highlight_mini_grid(grid_row, grid_col)

    def draw_large_symbol(self, grid_row, grid_col, symbol):
        """Draw a large symbol in the center of a completed mini-grid with transparency."""
        x = grid_col * 200
        y = grid_row * 200

        # Create a surface for the large symbol with transparency
        symbol_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        symbol_surface.fill((0, 0, 0, 0))  # Fully transparent background

        # Render the large symbol
        text_surface, _ = self.font.render(symbol, (255, 0, 0), size=100)
        text_surface.set_alpha(self.large_symbol_alpha)  # Set transparency
        text_rect = text_surface.get_rect(center=(100, 100))
        symbol_surface.blit(text_surface, text_rect.topleft)

        # Draw the symbol surface onto the main screen
        self.screen.blit(symbol_surface, (x, y))

    def draw_game_state(self):
        """Display the current game state at the bottom of the screen."""
        state_text = self.game.get_game_state()
        text_surface, _ = self.info_font.render(state_text, (0, 0, 0))
        self.screen.blit(text_surface, (10, 560))

    def draw_winning_lines(self):
        """Draw lines to indicate the winning condition."""
        winner_info = self.game.super_grid.winning_line
        if winner_info:
            line_type, index = winner_info
            if line_type == 'row':
                y = index * 200 + 100
                pygame.draw.line(self.screen, (255, 0, 0), (10, y), (590, y), 5)
            elif line_type == 'col':
                x = index * 200 + 100
                pygame.draw.line(self.screen, (255, 0, 0), (x, 10), (x, 590), 5)
            elif line_type == 'diag':
                if index == 1:
                    pygame.draw.line(self.screen, (255, 0, 0), (10, 10), (590, 590), 5)
                elif index == 2:
                    pygame.draw.line(self.screen, (255, 0, 0), (10, 590), (590, 10), 5)

    def draw_supergrid_outline(self):
        """Draw a large green outline around the supergrid."""
        pygame.draw.rect(self.screen, (0, 255, 0), (0, 0, 600, 600), 5)  # Green border

    def highlight_mini_grid(self, grid_row, grid_col):
        """Highlight a completed mini-grid with a border."""
        x = grid_col * 200
        y = grid_row * 200
        pygame.draw.rect(self.screen, (0, 0, 255), (x, y, 200, 200), 5)  # Blue border

    def can_pick_any_mini_grid(self):
        """Check if the player is allowed to pick any mini-grid."""
        # If next_grid is None, the player can pick any mini-grid
        return self.game.next_grid is None

    def handle_click(self, pos):
        """Handle mouse click events."""
        if self.mode is None:  # Menu screen
            if self.handle_menu_click(pos):
                return
        else:  # Game screen
            if self.game.is_player_human(self.game.current_player):
                grid_col = pos[0] // 200
                grid_row = pos[1] // 200
                cell_col = (pos[0] % 200) // 60
                cell_row = (pos[1] % 200) // 60
                if self.game.play_turn(grid_row, grid_col, cell_row, cell_col):
                    print(f"Move accepted: {grid_row} {grid_col} {cell_row} {cell_col}")
                else:
                    print(f"Invalid move: {grid_row} {grid_col} {cell_row} {cell_col}")
            else:
                print("It's not your turn!")

    def handle_play_again_click(self, pos):
        """Handle clicks on the Play Again button."""
        if self.play_again_button.collidepoint(pos):
            self.game.reset_game()  # Reset the game state
            self.mode = None  # Return to the mode selection screen
            return True
        return False

    def update(self):
        """Handle events and update the GUI."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.mode is None:  # Menu screen
                    self.handle_click(pos)
                elif self.game.super_grid.overall_winner or self.game.is_draw():
                    if self.game.is_player_human(self.game.current_player):
                        if self.handle_play_again_click(pos):
                            self.game.reset_game()  # Reset the game state
                            self.mode = None  # Go back to the menu
                else:  # Game screen
                    self.handle_click(pos)

        # Clear the screen and redraw based on the current mode
        if self.mode is None:
            self.draw_menu()
        else:
            self.screen.fill((255, 255, 255))  # Clear screen with white
            self.draw_grid()
            self.draw_game_state()

        pygame.display.flip()

    def draw_end_screen(self):
        """Draw the end screen with the result and a semi-transparent Play Again button."""
        # Draw the result text
        #if self.game.super_grid.overall_winner:
        #    result_text = f"Winner: {self.game.super_grid.overall_winner}"
        #else:
        #    result_text = "It's a draw!"
        
        #text_surface, _ = self.info_font.render(result_text, (255, 255, 255))
        #self.screen.blit(text_surface, (150, 200))

        # Create a surface for the "Play Again" button with transparency
        button_surface = pygame.Surface(self.play_again_button.size, pygame.SRCALPHA)
        button_surface.fill((0, 255, 0, 100))  # Semi-transparent green background
        button_text_surface, _ = self.font.render("Play Again", (255, 255, 255))
        button_text_rect = button_text_surface.get_rect(center=(self.play_again_button.width // 2, self.play_again_button.height // 2))
        button_surface.blit(button_text_surface, button_text_rect)

        # Draw the button surface onto the main screen at the button's position
        self.screen.blit(button_surface, self.play_again_button.topleft)
        
        # Make sure the screen updates to show the button
        pygame.display.flip()

        # Wait for a button click
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.handle_play_again_click(event.pos):
                        waiting_for_click = False
                        return  # Exit to allow the game to reset



    """def update(self):
        "Main loop for updating the GUI."
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            if self.mode is None:  # Menu screen
                self.draw_menu()
            else:  # Game screen
                self.screen.fill((255, 255, 255))
                self.draw_grid()
                self.draw_game_state()
                pygame.display.flip()

                if self.game.super_grid.overall_winner or self.game.is_draw():
                    print(self.game.get_game_state())
                    running = False

        pygame.quit()
        exit()  # Ensure the program exits when the GUI is closed"""

