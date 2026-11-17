import tempfile
import unittest
from pathlib import Path

from game.leaderboard import load_leaderboard, record_time


class LeaderboardTests(unittest.TestCase):
    def test_keeps_only_the_five_fastest_scores(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "leaderboard.json"
            for value in (8, 2, 6, 1, 9, 3, 5):
                record_time(value, "Easy", path)

            entries = load_leaderboard(path)
            self.assertEqual([entry["time"] for entry in entries], [1, 2, 3, 5, 6])

    def test_missing_leaderboard_starts_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_leaderboard(Path(directory) / "scores.json"), [])

    def test_rejects_negative_completion_times(self):
        with self.assertRaises(ValueError):
            record_time(-1, "Easy", "unused.json")


if __name__ == "__main__":
    unittest.main()
