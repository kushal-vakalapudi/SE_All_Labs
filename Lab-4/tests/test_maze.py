import unittest

from game.maze import find_path, generate_maze


class MazeTests(unittest.TestCase):
    def test_generated_maze_has_a_valid_start_to_exit_path(self):
        walls = generate_maze(10, 8)
        path = find_path(walls)

        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (7, 9))
        self.assertEqual(len(path), len(set(path)))

        for (row, col), (next_row, next_col) in zip(path, path[1:]):
            delta = (next_row - row, next_col - col)
            wall_direction = {
                (-1, 0): 0,
                (1, 0): 1,
                (0, 1): 2,
                (0, -1): 3,
            }[delta]
            self.assertFalse(walls[row][col][wall_direction])

    def test_find_path_returns_shortest_route(self):
        walls = [[[True, True, False, True] for _ in range(3)]]
        walls[0][1][3] = False

        self.assertEqual(find_path(walls), [(0, 0), (0, 1), (0, 2)])

    def test_generation_rejects_non_positive_dimensions(self):
        for dimensions in ((0, 1), (1, 0), (-1, 2)):
            with self.subTest(dimensions=dimensions):
                with self.assertRaises(ValueError):
                    generate_maze(*dimensions)


if __name__ == "__main__":
    unittest.main()
