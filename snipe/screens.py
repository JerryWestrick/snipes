"""Title screen and game over screen."""

from __future__ import annotations

import pygame
from snipe.settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BG, COLOR_HUD_TEXT, LEVELS


def draw_title_screen(screen: pygame.Surface) -> None:
    """Draw the title screen."""
    screen.fill(COLOR_BG)
    title_font = pygame.font.SysFont("monospace", 48, bold=True)
    sub_font = pygame.font.SysFont("monospace", 20)

    title = title_font.render("S N I P E S", True, (50, 255, 80))
    subtitle = sub_font.render("A recreation of the 1983 Novell classic", True, COLOR_HUD_TEXT)
    controls1 = sub_font.render("Arrow keys = Move    WASD = Shoot", True, COLOR_HUD_TEXT)
    controls2 = sub_font.render("Combine keys for diagonal shots", True, COLOR_HUD_TEXT)
    controls3 = sub_font.render("Diagonal shots bounce off walls!", True, (255, 255, 50))
    start = sub_font.render("Press ENTER to start    ESC to quit", True, (200, 200, 200))

    cx = SCREEN_WIDTH // 2
    screen.blit(title, (cx - title.get_width() // 2, 150))
    screen.blit(subtitle, (cx - subtitle.get_width() // 2, 220))
    screen.blit(controls1, (cx - controls1.get_width() // 2, 300))
    screen.blit(controls2, (cx - controls2.get_width() // 2, 330))
    screen.blit(controls3, (cx - controls3.get_width() // 2, 370))
    screen.blit(start, (cx - start.get_width() // 2, 450))


def draw_game_over_screen(screen: pygame.Surface, victory: bool, score: int) -> None:
    """Draw the game over screen."""
    screen.fill(COLOR_BG)
    title_font = pygame.font.SysFont("monospace", 48, bold=True)
    sub_font = pygame.font.SysFont("monospace", 24)

    if victory:
        title = title_font.render("VICTORY!", True, (50, 255, 80))
    else:
        title = title_font.render("GAME OVER", True, (255, 60, 60))

    score_text = sub_font.render(f"Score: {score}", True, COLOR_HUD_TEXT)
    prompt = sub_font.render("R = Play Again    ESC = Quit", True, (200, 200, 200))

    cx = SCREEN_WIDTH // 2
    screen.blit(title, (cx - title.get_width() // 2, 200))
    screen.blit(score_text, (cx - score_text.get_width() // 2, 300))
    screen.blit(prompt, (cx - prompt.get_width() // 2, 380))


def draw_level_screen(screen: pygame.Surface, level_num: int) -> None:
    """Draw the level intro screen."""
    screen.fill(COLOR_BG)
    title_font = pygame.font.SysFont("monospace", 48, bold=True)
    sub_font = pygame.font.SysFont("monospace", 20)

    title = title_font.render(f"Level {level_num}", True, (50, 255, 80))

    level = LEVELS[level_num - 1]
    info = sub_font.render(
        f"Maze: {level['rooms_x']}x{level['rooms_y']}   "
        f"Hives: {level['hives']}   "
        f"Max Snipes: {level['max_snipes']}",
        True, COLOR_HUD_TEXT
    )
    prompt = sub_font.render("Press any key to start", True, (150, 150, 150))

    cx = SCREEN_WIDTH // 2
    screen.blit(title, (cx - title.get_width() // 2, 220))
    screen.blit(info, (cx - info.get_width() // 2, 300))
    screen.blit(prompt, (cx - prompt.get_width() // 2, 380))
