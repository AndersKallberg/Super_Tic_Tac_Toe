import random
import math

class AI:
    """AI player for Super Tic Tac Toe."""
    
    def __init__(self, game, player):
        self.game = game
        self.player = player

    def get_board_state(self):
        cell_features = self.game.get_cell_features()
        minigrid_features = self.game.get_minigrid_features()
        game_state_features = self.game.get_game_state_features()
        return cell_features, minigrid_features, game_state_features

    def make_move(self):
        # Get the board state features
        cell_features, minigrid_features, game_state_features = self.get_board_state()
        
        # For now, we can print the features for debugging
        print("Cell Features:\n", cell_features)
        print("MiniGrid Features:\n", minigrid_features)
        print("Game State Features:\n", game_state_features)

        # You can implement your AI logic here using these features
        move = self.random_move()  # Placeholder for AI logic
        
        if move:
            self.game.play_turn(*move)

    def random_move(self):
        """Make a random valid move."""
        possible_moves = []
        for gr in range(3):
            for gc in range(3):
                for cr in range(3):
                    for cc in range(3):
                        if self.game.validate_move(gr, gc, cr, cc):
                            possible_moves.append((gr, gc, cr, cc))
        
        if possible_moves:
            return random.choice(possible_moves)
        return None