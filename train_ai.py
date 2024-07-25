import numpy as np
import torch
from game import Game
from ai import AI

# Parameters
BATCH_SIZE = 32
EPISODES = 1000

# Initialize game and AI
game = Game()
ai = AI(game, 'X')

# Train the AI model
ai.train_model(episodes=EPISODES, batch_size=BATCH_SIZE)

# Save the trained model
ai.save_model("super_tic_tac_toe_ai.pth")
