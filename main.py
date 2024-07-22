import os
from cli import CLI
from game import Game
from gui import GUI
from ai import AI
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    game = Game()
    gui = GUI(game)
    
    # Game loop
    starting = True
    while gui.running or starting:
        starting = False 
        # Main menu loop
        while gui.mode is None and gui.running:
            gui.update()
        
        clear_screen()
        game.reset_game()  # Reset the game state

        # Set player types based on selected mode
        if gui.mode == 'PvP':
            game.set_player_type('X', 'human')
            game.set_player_type('O', 'human')
        elif gui.mode == 'PvE':
            ai_player = AI(game, 'O')  # Initialize AI player
            game.set_player_type('O', 'ai')
        elif gui.mode == 'EvE':
            ai_player_x = AI(game, 'X')  # Initialize AI player for X
            ai_player_o = AI(game, 'O')  # Initialize AI player for O
            game.set_player_type('X', 'ai')
            game.set_player_type('O', 'ai')

        while not game.super_grid.overall_winner and not game.is_draw() and gui.running:
            gui.update()  # Handle GUI updates

            if game.is_player_human(game.current_player):
                # Wait for human input via GUI
                continue
                
            
            # AI's turn
            if gui.mode == 'PvE' and not game.is_player_human(game.current_player):
                print("AI is making a move...")
                ai_player.make_move()
            elif gui.mode == 'EvE' and not game.is_player_human(game.current_player):
                print(f"AI {game.current_player} is making a move...")
                if game.current_player == 'X':
                    ai_player_x.make_move()
                else:
                    ai_player_o.make_move()

        if game.super_grid.overall_winner or game.is_draw():
            print(game.get_game_state())
            gui.update()  # To show the final state
            gui.draw_end_screen()
        # No explicit 'Play Again' prompt needed as it's handled by GUI
        # The GUI handles play again through button click

    pygame.quit()  # Quit pygame when exiting the game loop

if __name__ == "__main__":
    main()