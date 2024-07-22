import unittest
from super_grid import SuperGrid
from mini_grid import MiniGrid
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestSuperGrid(unittest.TestCase):
    def setUp(self):
        self.super_grid = SuperGrid()

    @classmethod
    def setUpClass(cls):
        print("\nRunning tests in test_super_grid.py")

    def test_initial_state(self):
        for row in self.super_grid.mini_grids:
            for mini_grid in row:
                for cell_row in mini_grid.cells:
                    for cell in cell_row:
                        self.assertIsNone(cell.value)
        self.assertIsNone(self.super_grid.overall_winner)

    def test_check_overall_winner(self):
        for i in range(3):
            self.super_grid.mini_grids[i][0].winner = 'X'
            self.super_grid.mini_grids[i][1].winner = 'X'
            self.super_grid.mini_grids[i][2].winner = 'X'
        self.super_grid.check_overall_winner()
        self.assertEqual(self.super_grid.overall_winner, 'X')

    def test_make_move(self):
        self.assertTrue(self.super_grid.make_move(0, 0, 0, 0, 'X'))
        self.assertEqual(self.super_grid.mini_grids[0][0].cells[0][0].value, 'X')
        self.assertFalse(self.super_grid.make_move(0, 0, 0, 0, 'O'))  # Cell already taken

if __name__ == '__main__':
    unittest.main()
