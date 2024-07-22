import unittest
from game import Game
from gui import GUI
import os
import sys
import pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.gui = GUI(self.game)
        pygame.display.set_mode = lambda *args, **kwargs: None  # Mock display mode to avoid opening a window

    @classmethod
    def setUpClass(cls):
        print("\nRunning tests in test_gui.py")

    def test_initial_state(self):
        self.assertEqual(self.gui.game.current_player, 'X')
        self.assertIsNone(self.gui.game.super_grid.overall_winner)

    def test_draw_grid(self):
        self.gui.draw_grid()  # Should draw the initial empty grid

    def test_handle_click_valid(self):
        self.gui.handle_click((10, 10))  # Mock click on the top-left cell

    def test_handle_click_invalid(self):
        self.game.play_turn(0, 0, 0, 0)  # Occupy the top-left cell
        self.gui.handle_click((10, 10))  # Mock click
