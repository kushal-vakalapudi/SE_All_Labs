import unittest

import pygame

from game.maze import CELL
from game.player import Player


class PressedKeys:
    def __init__(self, *pressed):
        self.pressed = set(pressed)

    def __getitem__(self, key):
        return key in self.pressed


class PlayerTests(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_player_cannot_cross_a_closed_wall(self):
        walls = [[[True, True, True, True], [True, True, True, True]]]
        player = Player(0, 0)

        for _ in range(20):
            player.move(PressedKeys(pygame.K_RIGHT), walls, 1, 2)

        self.assertEqual(player.c, 0)
        self.assertLessEqual(player.rect.right, CELL)

    def test_player_can_cross_an_open_passage(self):
        walls = [[[True, True, False, True], [True, True, True, False]]]
        player = Player(0, 0)

        for _ in range(10):
            player.move(PressedKeys(pygame.K_RIGHT), walls, 1, 2)

        self.assertEqual(player.c, 1)

    def test_player_cannot_leave_the_maze(self):
        walls = [[[True, True, True, True]]]
        player = Player(0, 0)

        for _ in range(10):
            player.move(PressedKeys(pygame.K_LEFT), walls, 1, 1)

        self.assertGreaterEqual(player.rect.left, 0)


if __name__ == "__main__":
    unittest.main()
