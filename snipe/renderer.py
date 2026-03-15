"""Draws everything to the screen."""

from __future__ import annotations

import pygame
from snipe.camera import Camera
from snipe.entities import Player, Snipe, Hive, Bullet
from snipe.maze import Maze
from snipe.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_BG, COLOR_WALL, COLOR_PLAYER, COLOR_PLAYER_INV,
    COLOR_SNIPE, COLOR_HIVE, COLOR_BULLET_PLAYER, COLOR_BULLET_SNIPE,
    COLOR_HUD_TEXT, COLOR_HUD_BG,
)


class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("monospace", 20)

    def draw(self, maze: Maze, player: Player, snipes: list[Snipe],
             hives: list[Hive], bullets: list[Bullet],
             camera: Camera, score: int, level: int = 1) -> None:
        """Draw one frame."""
        self.screen.fill(COLOR_BG)
        self._draw_walls(maze, camera)
        self._draw_hives(hives, camera)
        self._draw_snipes(snipes, camera)
        self._draw_bullets(bullets, camera)
        self._draw_player(player, camera)
        self._draw_hud(player, score, hives, level)

    def _draw_walls(self, maze: Maze, camera: Camera) -> None:
        for wall in maze.walls:
            sx, sy = camera.apply(wall.x, wall.y)
            screen_rect = pygame.Rect(sx, sy, wall.width, wall.height)
            # Only draw if on screen
            if screen_rect.right > 0 and screen_rect.left < SCREEN_WIDTH \
               and screen_rect.bottom > 0 and screen_rect.top < SCREEN_HEIGHT:
                pygame.draw.rect(self.screen, COLOR_WALL, screen_rect)

    def _draw_player(self, player: Player, camera: Camera) -> None:
        if not player.alive:
            return
        sx, sy = camera.apply(player.x, player.y)
        # Blink when invulnerable
        if player.is_invulnerable:
            if int(player.invulnerable * 8) % 2 == 0:
                color = COLOR_PLAYER_INV
            else:
                color = COLOR_PLAYER
        else:
            color = COLOR_PLAYER
        pygame.draw.circle(self.screen, color, (int(sx), int(sy)), player.radius)

    def _draw_snipes(self, snipes: list[Snipe], camera: Camera) -> None:
        for snipe in snipes:
            if not snipe.alive or not camera.is_visible(snipe.x, snipe.y):
                continue
            sx, sy = camera.apply(snipe.x, snipe.y)
            pygame.draw.circle(self.screen, COLOR_SNIPE, (int(sx), int(sy)), snipe.radius)

    def _draw_hives(self, hives: list[Hive], camera: Camera) -> None:
        for hive in hives:
            if not hive.alive or not camera.is_visible(hive.x, hive.y):
                continue
            sx, sy = camera.apply(hive.x, hive.y)
            # Diamond shape
            r = hive.radius
            points = [
                (sx, sy - r),
                (sx + r, sy),
                (sx, sy + r),
                (sx - r, sy),
            ]
            pygame.draw.polygon(self.screen, COLOR_HIVE, points)

    def _draw_bullets(self, bullets: list[Bullet], camera: Camera) -> None:
        for bullet in bullets:
            if not bullet.alive or not camera.is_visible(bullet.x, bullet.y):
                continue
            sx, sy = camera.apply(bullet.x, bullet.y)
            color = COLOR_BULLET_PLAYER if bullet.owner == "player" else COLOR_BULLET_SNIPE
            pygame.draw.circle(self.screen, color, (int(sx), int(sy)), bullet.radius)

    def _draw_hud(self, player: Player, score: int, hives: list[Hive],
                  level: int = 1) -> None:
        hives_left = sum(1 for h in hives if h.alive)
        text = f"Level: {level}   Score: {score}   Lives: {player.lives}   Hives: {hives_left}"
        surface = self.font.render(text, True, COLOR_HUD_TEXT, COLOR_HUD_BG)
        self.screen.blit(surface, (10, 10))
