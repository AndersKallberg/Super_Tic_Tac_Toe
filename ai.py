import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque

class AI:
    """AI player for Super Tic Tac Toe using a neural network for reinforcement learning."""

    def __init__(self, game, player, model=None, device='cpu'):
        self.game = game
        self.player = player
        self.device = device

        # Define the model
        self.model = model if model else self.create_model()
        self.model.to(self.device)

        # Define the optimizer
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.loss_fn = nn.MSELoss()

        # Replay memory for experience replay
        self.memory = deque(maxlen=10000)

    def create_model(self):
        """Define the neural network model."""
        model = nn.Sequential(
            nn.Flatten(),
            nn.Linear(9*9*2 + 3*3*2 + 3, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 9*9)  # Output 81 values representing the Q-values for each cell
        )
        return model

    def get_board_state(self):
        """Get the board state features."""
        return self.game.get_board_state()

    def get_state_tensor(self):
        """Get the board state as a tensor."""
        state = self.get_board_state()
        state_tensor = torch.tensor(state, dtype=torch.float32).to(self.device)
        print(f"State tensor: {state_tensor[:10]}...")  # Print only the first 10 values for readability
        return state_tensor

    def predict_move(self):
        """Predict the best move given the current board state."""
        self.model.eval()
        state_tensor = self.get_state_tensor().unsqueeze(0)  # Add batch dimension
        with torch.no_grad():
            q_values = self.model(state_tensor)
        q_values = q_values.cpu().numpy().flatten()
        print(f"Q-values before masking: {q_values[:10]}...")  # Print only the first 10 values for readability

        # Mask invalid moves
        mask = np.ones(q_values.shape, dtype=bool)
        for gr in range(3):
            for gc in range(3):
                for cr in range(3):
                    for cc in range(3):
                        if not self.game.validate_move(gr, gc, cr, cc):
                            mask[gr * 27 + gc * 9 + cr * 3 + cc] = False
        q_values[~mask] = -np.inf  # Set invalid moves to negative infinity
        print(f"Q-values after masking: {q_values[:10]}...")  # Print only the first 10 values for readability

        # Convert Q-values to a move (grid_row, grid_col, cell_row, cell_col)
        move = np.unravel_index(np.argmax(q_values), (9, 9))
        grid_row, cell_row = divmod(move[0], 3)
        grid_col, cell_col = divmod(move[1], 3)
        print(f"Predicted move: {grid_row, grid_col, cell_row, cell_col}")
        return grid_row, grid_col, cell_row, cell_col

    def make_move(self):
        """Make a move based on the predicted best move."""
        move = self.predict_move()
        if self.game.validate_move(*move):
            print(f"Making move: {move}")
            self.game.play_turn(*move)
        else:
            print(f"Invalid move predicted: {move}")
            print(f"Reason: Grid ({move[0]}, {move[1]}) - Cell ({move[2]}, {move[3]}) validation failed.")
            if self.game.super_grid.overall_winner is not None:
                print(f"Game already won by {self.game.super_grid.overall_winner}")
            elif self.game.next_grid is not None:
                next_grid_row, next_grid_col = self.game.next_grid
                if (move[0], move[1]) != (next_grid_row, next_grid_col):
                    if not self.game.super_grid.mini_grids[next_grid_row][next_grid_col].is_finished():
                        print(f"Move must be in grid ({next_grid_row}, {next_grid_col}), but got grid ({move[0]}, {move[1]})")
                    else:
                        print(f"Mini-grid ({next_grid_row}, {next_grid_col}) is finished, move should be allowed anywhere.")
            if self.game.super_grid.mini_grids[move[0]][move[1]].winner is not None:
                print(f"Mini-grid ({move[0]}, {move[1]}) is already won by {self.game.super_grid.mini_grids[move[0]][move[1]].winner}")
            if not self.game.super_grid.mini_grids[move[0]][move[1]].cells[move[2]][move[3]].is_empty():
                print(f"Cell ({move[2]}, {move[3]}) in mini-grid ({move[0]}, {move[1]}) is already taken")

    def remember(self, state, action, reward, next_state, done):
        """Store experience tuple in replay memory."""
        print(f"Remembering state: {state[:10]}..., action: {action}, reward: {reward}, next_state: {next_state[:10]}..., done: {done}")  # Print only the first 10 values for readability
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        """Train the model using experience replay."""
        if len(self.memory) < batch_size:
            print("Not enough memory to replay")
            return

        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            self.train(state, next_state, action, reward, done)

    def train(self, state, next_state, action, reward, done):
        """Train the model with a single step of gameplay data."""
        self.model.train()

        # Convert inputs to tensors
        state_tensor = torch.tensor(state, dtype=torch.float32).to(self.device)
        next_state_tensor = torch.tensor(next_state, dtype=torch.float32).to(self.device)
        action_tensor = torch.tensor(action, dtype=torch.long).to(self.device)
        reward_tensor = torch.tensor(reward, dtype=torch.float32).to(self.device)
        done_tensor = torch.tensor(done, dtype=torch.float32).to(self.device)

        # Get Q-values for the current state
        q_values = self.model(state_tensor.unsqueeze(0)).squeeze(0)
        print(f"Q-values for current state: {q_values[:10]}...")  # Print only the first 10 values for readability

        # Compute target Q-values for the next state
        with torch.no_grad():
            next_q_values = self.model(next_state_tensor.unsqueeze(0)).squeeze(0)
            max_next_q_value = torch.max(next_q_values)
            target_q_value = reward_tensor + (1 - done_tensor) * 0.99 * max_next_q_value
        print(f"Target Q-value: {target_q_value}")

        # Update the Q-value for the action taken
        q_values[action_tensor] = target_q_value

        # Compute the loss
        loss = self.loss_fn(q_values, self.model(state_tensor.unsqueeze(0)).squeeze(0))
        print(f"Loss: {loss.item()}")

        # Backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def save_model(self, path):
        """Save the model to a file."""
        print(f"Saving model to {path}")
        torch.save(self.model.state_dict(), path)

    def load_model(self, path):
        """Load the model from a file."""
        print(f"Loading model from {path}")
        self.model.load_state_dict(torch.load(path, map_location=self.device))
        self.model.to(self.device)

    def train_model(self, episodes, batch_size):
        """Train the model through multiple episodes of self-play."""
        for episode in range(episodes):
            print(f"Episode {episode + 1}/{episodes}")
            self.game.reset_game()
            state = self.get_state_tensor().cpu().numpy()
            done = False

            i = 0
            while not done:
                i+= 1
                if i == 10:
                    import time
                    time.sleep(10)
                print(f"Player {self.game.current_player}'s turn.")
                action = self.predict_move()
                grid_row, grid_col, cell_row, cell_col = action

                # Make the move
                current_player = self.game.current_player
                valid_move = self.game.play_turn(grid_row, grid_col, cell_row, cell_col)

                if valid_move:
                    print(f"Valid move made by Player {current_player}: {action}")
                    next_state = self.get_state_tensor().cpu().numpy()
                    reward = self.compute_reward()
                    done = self.game.super_grid.overall_winner is not None or self.game.is_draw()
                    self.remember(state, action, reward, next_state, done)
                    state = next_state

                    if not done:
                        self.make_move()
                        print(f"Player {self.game.current_player} tried making a move (unknown if success or fail)")
                        #state = self.get_state_tensor().cpu().numpy()
                else:
                    print(f"Invalid move attempted by Player {self.game.current_player}: {action}")

            self.replay(batch_size)

    def compute_reward(self):
        """Compute the reward based on the current game state."""
        if self.game.super_grid.overall_winner == self.player:
            return 1  # AI wins
        elif self.game.super_grid.overall_winner is not None:
            return -1  # AI loses
        elif self.game.is_draw():
            return 0.5  # Draw
        else:
            return 0  # Game continues