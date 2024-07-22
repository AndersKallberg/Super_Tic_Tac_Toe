import unittest
from mini_grid import MiniGrid
from cell import Cell
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestMiniGrid(unittest.TestCase):
    def setUp(self):
        self.mini_grid = MiniGrid()

    @classmethod
    def setUpClass(cls):
        print("\nRunning tests in test_mini_grid.py")

    def test_initial_state(self):
        for row in self.mini_grid.cells:
            for cell in row:
                self.assertIsNone(cell.value)
        self.assertIsNone(self.mini_grid.winner)

    def test_is_full(self):
        self.assertFalse(self.mini_grid.is_full())
        for row in self.mini_grid.cells:
            for cell in row:
                cell.set_value('X')
        self.assertTrue(self.mini_grid.is_full())

    def test_check_winner(self):
        self.mini_grid.cells[0][0].set_value('X')
        self.mini_grid.cells[0][1].set_value('X')
        self.mini_grid.cells[0][2].set_value('X')
        self.mini_grid.check_winner()
        self.assertEqual(self.mini_grid.winner, 'X')

    def test_make_move(self):
        self.assertTrue(self.mini_grid.make_move(0, 0, 'X'))
        self.assertEqual(self.mini_grid.cells[0][0].value, 'X')
        self.assertFalse(self.mini_grid.make_move(0, 0, 'O'))  # Cell already taken

if __name__ == '__main__':
    unittest.main()
