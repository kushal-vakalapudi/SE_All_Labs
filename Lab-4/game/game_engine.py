import time

import pygame

from game.leaderboard import load_leaderboard, record_time
from game.maze import CELL, find_path, generate_maze
from game.player import Player

FPS = 60
BG = (240, 235, 220)
WALL_COLOR = (40, 40, 60)
EXIT_COLOR = (80, 200, 80)
HUD_HEIGHT = 64
FOG_RADIUS = 3 * CELL
DIFFICULTIES = {
    "Easy": (10, 8),
    "Medium": (15, 13),
    "Hard": (20, 18),
}
MENU_SIZE = (800, 560)


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(MENU_SIZE)
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 20)
        self.small_font = pygame.font.SysFont("monospace", 12)
        self.big_font = pygame.font.SysFont("monospace", 36, bold=True)
        self.mode = "select"
        self.difficulty = None
        self.walls = []
        self.player = None
        self.path = []
        self.show_hint = False
        self.won = False
        self.elapsed = 0.0
        self.start_time = 0.0
        self.leaderboard = load_leaderboard()

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.cols, self.rows = DIFFICULTIES[difficulty]
        self.width = self.cols * CELL
        self.play_height = self.rows * CELL
        self.screen = pygame.display.set_mode((self.width, self.play_height + HUD_HEIGHT))
        self.reset()
        self.mode = "game"

    def reset(self):
        self.walls = generate_maze(self.cols, self.rows)
        self.player = Player(0, 0)
        self.exit_rect = pygame.Rect(
            (self.cols - 1) * CELL + 5,
            (self.rows - 1) * CELL + 5,
            CELL - 10,
            CELL - 10,
        )
        self.path = find_path(self.walls)
        self.show_hint = False
        self.start_time = time.perf_counter()
        self.elapsed = 0.0
        self.won = False
        self.leaderboard = load_leaderboard()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.mode == "select":
                if event.type == pygame.KEYDOWN:
                    choices = (pygame.K_1, pygame.K_2, pygame.K_3)
                    for key, difficulty in zip(choices, DIFFICULTIES):
                        if event.key == key:
                            self.start_game(difficulty)
                            break
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button, difficulty in self._difficulty_buttons():
                        if button.collidepoint(event.pos):
                            self.start_game(difficulty)
                            break
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_h and not self.won:
                    self.show_hint = not self.show_hint
                elif event.key == pygame.K_ESCAPE:
                    self.mode = "select"
                    self.screen = pygame.display.set_mode(MENU_SIZE)

        return True

    def update(self):
        if self.mode != "game" or self.won:
            return

        keys = pygame.key.get_pressed()
        self.player.move(keys, self.walls, self.rows, self.cols)
        self.elapsed = time.perf_counter() - self.start_time
        if self.player.rect.colliderect(self.exit_rect):
            self.won = True
            self.leaderboard = record_time(self.elapsed, self.difficulty)

    def _difficulty_buttons(self):
        button_width, button_height, gap = 180, 66, 22
        total_width = len(DIFFICULTIES) * button_width + (len(DIFFICULTIES) - 1) * gap
        left = (MENU_SIZE[0] - total_width) // 2
        top = 280
        return [
            (
                pygame.Rect(left + index * (button_width + gap), top, button_width, button_height),
                difficulty,
            )
            for index, difficulty in enumerate(DIFFICULTIES)
        ]

    def draw_maze(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x, y = col * CELL, row * CELL
                if self.show_hint and (row, col) in self.path:
                    highlight = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
                    highlight.fill((40, 170, 230, 105))
                    self.screen.blit(highlight, (x, y))

                north, south, east, west = self.walls[row][col]
                if north:
                    pygame.draw.line(self.screen, WALL_COLOR, (x, y), (x + CELL, y), 3)
                if south:
                    pygame.draw.line(
                        self.screen, WALL_COLOR, (x, y + CELL), (x + CELL, y + CELL), 3
                    )
                if east:
                    pygame.draw.line(
                        self.screen, WALL_COLOR, (x + CELL, y), (x + CELL, y + CELL), 3
                    )
                if west:
                    pygame.draw.line(self.screen, WALL_COLOR, (x, y), (x, y + CELL), 3)

    def draw_fog(self):
        fog = pygame.Surface((self.width, self.play_height), pygame.SRCALPHA)
        fog.fill((0, 0, 0, 235))
        pygame.draw.circle(
            fog,
            (0, 0, 0, 0),
            self.player.rect.center,
            FOG_RADIUS,
        )
        self.screen.blit(fog, (0, 0))

    def _draw_hud(self):
        hud = pygame.Rect(0, self.play_height, self.width, HUD_HEIGHT)
        pygame.draw.rect(self.screen, (30, 30, 50), hud)
        label = self.font.render(
            f"{self.difficulty}  Time: {self.elapsed:.1f}s  H: Hint  R: New maze",
            True,
            (230, 230, 230),
        )
        self.screen.blit(label, (10, self.play_height + 21))

    def _draw_win_overlay(self):
        overlay = pygame.Surface((self.width, self.play_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        center_x = self.width // 2
        center_y = self.play_height // 2
        title = self.big_font.render("Maze solved!", True, (110, 255, 130))
        result = self.font.render(f"Time: {self.elapsed:.2f}s", True, (245, 245, 245))
        heading = self.font.render("BEST TIMES", True, (255, 220, 100))
        self.screen.blit(title, title.get_rect(center=(center_x, center_y - 125)))
        self.screen.blit(result, result.get_rect(center=(center_x, center_y - 82)))
        self.screen.blit(heading, heading.get_rect(center=(center_x, center_y - 42)))

        for index, entry in enumerate(self.leaderboard):
            text = self.font.render(
                f"{index + 1}. {entry['difficulty']}  {entry['time']:.2f}s",
                True,
                (230, 230, 230),
            )
            self.screen.blit(
                text,
                text.get_rect(center=(center_x, center_y - 10 + index * 27)),
            )

        prompt = self.small_font.render(
            "R: play again     Esc: choose difficulty",
            True,
            (205, 205, 205),
        )
        self.screen.blit(prompt, prompt.get_rect(center=(center_x, center_y + 145)))

    def _draw_selection(self):
        self.screen.fill((24, 28, 48))
        title = self.big_font.render("MAZE RUNNER", True, (245, 245, 245))
        subtitle = self.font.render("Choose your difficulty", True, (190, 205, 225))
        self.screen.blit(title, title.get_rect(center=(MENU_SIZE[0] // 2, 150)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(MENU_SIZE[0] // 2, 215)))

        colors = ((70, 145, 95), (65, 110, 180), (175, 85, 75))
        for (button, difficulty), color in zip(self._difficulty_buttons(), colors):
            pygame.draw.rect(self.screen, color, button, border_radius=8)
            label = self.font.render(f"{difficulty} ({DIFFICULTIES[difficulty][0]}x{DIFFICULTIES[difficulty][1]})", True, (255, 255, 255))
            self.screen.blit(label, label.get_rect(center=button.center))

        instructions = self.small_font.render(
            "Click a size or press 1, 2, or 3",
            True,
            (190, 205, 225),
        )
        self.screen.blit(instructions, instructions.get_rect(center=(MENU_SIZE[0] // 2, 385)))

    def draw(self):
        if self.mode == "select":
            self._draw_selection()
        else:
            self.screen.fill(BG)
            self.draw_maze()
            pygame.draw.rect(self.screen, EXIT_COLOR, self.exit_rect, border_radius=4)
            exit_label = self.small_font.render("EXIT", True, (20, 80, 20))
            self.screen.blit(exit_label, exit_label.get_rect(center=self.exit_rect.center))
            self.player.draw(self.screen)
            self.draw_fog()
            self._draw_hud()
            if self.won:
                self._draw_win_overlay()

        pygame.display.flip()

    def run(self):
        running = True
        try:
            while running:
                running = self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(FPS)
        finally:
            pygame.quit()
