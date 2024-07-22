import unittest
from game import Game
from cell import Cell
from mini_grid import MiniGrid
from super_grid import SuperGrid
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    @classmethod
    def setUpClass(cls):
        print("\nRunning tests in test_game.py")

    def test_initial_state(self):
        self.assertEqual(self.game.current_player, 'X')
        self.assertIsNone(self.game.super_grid.overall_winner)
        self.assertIsNone(self.game.next_grid)

    def test_switch_player(self):
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 'O')
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 'X')

    def test_validate_move(self):
        self.assertTrue(self.game.validate_move(0, 0, 0, 0))
        self.game.play_turn(0, 0, 0, 0)
        self.assertFalse(self.game.validate_move(0, 0, 0, 0))  # Cell already taken

    def test_play_turn(self):
        self.assertTrue(self.game.play_turn(0, 0, 0, 0))
        self.assertEqual(self.game.current_player, 'O')
        self.assertFalse(self.game.play_turn(0, 0, 0, 0))  # Invalid move

    def test_is_draw(self):
        # Fill the board to make it a draw
        for gr in range(3):
            for gc in range(3):
                self.game.super_grid.mini_grids[gr][gc].winner = 'X'
        self.assertTrue(self.game.is_draw())

    def test_get_game_state(self):
        self.assertEqual(self.game.get_game_state(), "Player X's turn.")
        self.game.super_grid.overall_winner = 'X'
        self.assertEqual(self.game.get_game_state(), "Player X wins!")
        for gr in range(3):
            for gc in range(3):
                self.game.super_grid.mini_grids[gr][gc].winner = 'X'
        self.assertEqual(self.game.get_game_state(), "Player X wins!")
        self.game.super_grid.overall_winner = None
        for gr in range(3):
            for gc in range(3):
                self.game.super_grid.mini_grids[gr][gc].winner = 'X'
        self.assertTrue(self.game.is_draw())
        self.assertEqual(self.game.get_game_state(), "The game is a draw!")

    def test_save_and_load_game(self):
        self.game.play_turn(0, 0, 0, 0)
        self.game.save_game('test_save.json')
        new_game = Game()
        new_game.load_game('test_save.json')
        self.assertEqual(new_game.current_player, 'O')
        self.assertEqual(new_game.super_grid.mini_grids[0][0].cells[0][0].value, 'X')

    def test_reset_game(self):
        self.game.play_turn(0, 0, 0, 0)
        self.game.reset_game()
        self.assertEqual(self.game.current_player, 'X')
        self.assertIsNone(self.game.super_grid.overall_winner)
        self.assertIsNone(self.game.next_grid)
        for row in self.game.super_grid.mini_grids:
            for mini_grid in row:
                for cell_row in mini_grid.cells:
                    for cell in cell_row:
                        self.assertIsNone(cell.value)

if __name__ == '__main__':
    unittest.main()
