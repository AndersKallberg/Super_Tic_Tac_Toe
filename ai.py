import random
import math

class AI:
    """AI player for Super Tic Tac Toe."""
    
    def __init__(self, game, player):
        self.game = game
        self.player = player

    def make_move(self):
        """Make a move based on the chosen strategy."""
        # You can choose different strategies here
        # For now, we'll implement a random move strategy and a simple minimax strategy
        move = self.random_move()
        
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