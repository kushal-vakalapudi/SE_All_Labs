import unittest
from unittest.mock import patch

import pygame

from game.game_engine import BG, DIFFICULTIES, GameEngine


class GameEngineTests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.engine = GameEngine()

    def tearDown(self):
        pygame.quit()

    def test_each_difficulty_starts_a_fresh_game_at_the_requested_size(self):
        for difficulty, (cols, rows) in DIFFICULTIES.items():
            with self.subTest(difficulty=difficulty):
                self.engine.start_game(difficulty)
                self.assertEqual((self.engine.cols, self.engine.rows), (cols, rows))
                self.assertEqual(self.engine.mode, "game")
                self.assertEqual(self.engine.path[0], (0, 0))
                self.assertEqual(self.engine.path[-1], (rows - 1, cols - 1))
                self.engine.draw()

    def test_hint_key_toggles_the_shortest_path(self):
        self.engine.start_game("Easy")
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_h))
        self.engine.handle_events()
        self.assertTrue(self.engine.show_hint)

        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_h))
        self.engine.handle_events()
        self.assertFalse(self.engine.show_hint)

    def test_fog_reveals_nearby_cells_and_darkens_distant_cells(self):
        self.engine.start_game("Easy")
        self.engine.screen.fill(BG)
        self.engine.draw_fog()

        self.assertEqual(self.engine.screen.get_at(self.engine.player.rect.center)[:3], BG)
        self.assertLess(self.engine.screen.get_at((self.engine.width - 1, self.engine.play_height - 1)).r, 50)

    def test_completing_a_maze_records_and_displays_the_run(self):
        self.engine.start_game("Easy")
        scores = [{"time": 1.25, "difficulty": "Easy"}]
        self.engine.player.rect.center = self.engine.exit_rect.center

        with patch("game.game_engine.record_time", return_value=scores) as record:
            self.engine.update()
            self.engine.draw()

        self.assertTrue(self.engine.won)
        self.assertGreaterEqual(record.call_args.args[0], 0)
        self.assertEqual(record.call_args.args[1], "Easy")
        self.assertEqual(self.engine.leaderboard, scores)


if __name__ == "__main__":
    unittest.main()
