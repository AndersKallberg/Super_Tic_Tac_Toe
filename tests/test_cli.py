import unittest
try:
    from unittest import mock
except ImportError:
    import mock
from game import Game
from cli import CLI
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestCLI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nRunning tests in test_cli.py")

    def setUp(self):
        self.game = Game()
        self.cli = CLI(self.game)

    def test_display_grid_initial_state(self):
        self.cli.display_grid()  # Should print the initial empty grid

    def test_get_input_valid(self):
        with mock.patch('builtins.input', return_value='0 0 0 0'):
            grid_row, grid_col, cell_row, cell_col = self.cli.get_input()
            self.assertEqual((grid_row, grid_col, cell_row, cell_col), (0, 0, 0, 0))

    def test_get_input_invalid(self):
        # Mock input with invalid values
        with mock.patch('builtins.input', side_effect=['0 0 0', '0 0 0']) as mocked_input:
            with self.assertRaises(ValueError) as context:
                self.cli.get_input(max_retries=2)  # Set max_retries to test retry behavior
            print(f"Invalid input error message: {context.exception}")

            # Mock input with valid values for subsequent tests
            mocked_input.side_effect = ['0 0 0 0']
            grid_row, grid_col, cell_row, cell_col = self.cli.get_input(max_retries=1)
            self.assertEqual((grid_row, grid_col, cell_row, cell_col), (0, 0, 0, 0))

    def test_update(self):
        self.cli.update()  # Should print the initial game state

if __name__ == '__main__':
    unittest.main()