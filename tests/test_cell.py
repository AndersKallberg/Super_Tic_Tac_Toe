import unittest
import sys
import os

# Add the base directory to sys.path if it's not already there
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from cell import Cell

class TestCell(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nRunning tests in test_cell.py")

    def setUp(self):
        self.cell = Cell()

    def test_initial_state(self):
        self.assertIsNone(self.cell.value)

    def test_is_empty(self):
        self.assertTrue(self.cell.is_empty())
        self.cell.set_value('X')
        self.assertFalse(self.cell.is_empty())

    def test_set_value(self):
        self.cell.set_value('X')
        self.assertEqual(self.cell.value, 'X')
        self.cell.set_value('O')
        self.assertEqual(self.cell.value, 'X')  # Value should not change

if __name__ == '__main__':
    unittest.main()