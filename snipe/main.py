"""Snipes — main entry point and game loop."""

from __future__ import annotations

import random
import pygame
from pygame.locals import *

from snipe.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    MOVE_KEYS, SHOOT_KEYS, DIRECTIONS,
    PLAYER_SPEED, SHOOT_COOLDOWN, INVULNERABLE_TIME,
    SCORE_SNIPE, SCORE_HIVE, LEVELS,
    HIVE_RADIUS, PLAYER_START_LIVES,
)
from snipe.maze import Maze
from snipe.entities import Player, Snipe, Hive, Bullet
from snipe.physics import move_circle, move_bullet, check_circle_collision
from snipe.ai import update_snipe
from snipe.camera import Camera
from snipe.renderer import Renderer
from snipe.screens import draw_title_screen, draw_game_over_screen, draw_level_screen


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snipes")
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        self.rng = random.Random()

    def run(self) -> None:
        """Main app loop — title → levels → game over → repeat."""
        while True:
            action = self._title_screen()
            if action == "quit":
                break

            # Play through levels, carrying score and lives
            total_score = 0
            lives = PLAYER_START_LIVES

            for level_num in range(len(LEVELS)):
                # Show level intro
                if self._level_intro(level_num + 1) == "quit":
                    break

                result, total_score, lives = self._game_loop(
                    level_num, total_score, lives
                )
                if result == "quit":
                    pygame.quit()
                    return
                if result == "dead":
                    # Game over — died
                    action = self._game_over_screen(False, total_score)
                    if action == "quit":
                        pygame.quit()
                        return
                    break  # back to title
                # result == "win" — continue to next level

            else:
                # Beat all levels!
                action = self._game_over_screen(True, total_score)
                if action == "quit":
                    pygame.quit()
                    return

        pygame.quit()

    def _title_screen(self) -> str:
        """Show title screen. Returns 'start' or 'quit'."""
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "quit"
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return "start"
                    if event.key == K_ESCAPE:
                        return "quit"

            draw_title_screen(self.screen)
            pygame.display.flip()
            self.clock.tick(30)

    def _level_intro(self, level_num: int) -> str:
        """Show level number briefly. Returns 'go' or 'quit'."""
        timer = 2.0  # seconds to show
        while timer > 0:
            dt = self.clock.tick(30) / 1000.0
            timer -= dt
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "quit"
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return "quit"
                    timer = 0  # any key skips

            draw_level_screen(self.screen, level_num)
            pygame.display.flip()
        return "go"

    def _game_loop(self, level_num: int, score: int, lives: int) -> tuple[str, int, int]:
        """Run one level. Returns (result, score, lives).

        result: 'win', 'dead', or 'quit'
        """
        level = LEVELS[level_num]

        # Setup maze
        maze = Maze(rooms_x=level["rooms_x"], rooms_y=level["rooms_y"])
        camera = Camera(maze.width, maze.height)

        # Player starts at center room
        prx = maze.rooms_x // 2
        pry = maze.rooms_y // 2
        px, py = maze.room_center(prx, pry)
        player = Player(x=px, y=py, lives=lives)

        # Place hives
        hive_rooms = maze.find_hive_rooms(level["hives"], (prx, pry))
        hives = []
        for rx, ry in hive_rooms:
            hx, hy = maze.room_center(rx, ry)
            hives.append(Hive(
                x=hx, y=hy,
                health=level["hive_health"],
                spawn_interval=level["spawn_interval"],
            ))

        max_snipes = level["max_snipes"]
        snipe_speed = level["snipe_speed"]

        snipes: list[Snipe] = []
        bullets: list[Bullet] = []
        shoot_timer = 0.0
        paused = False

        while True:
            dt = self.clock.tick(FPS) / 1000.0

            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "quit", score, player.lives
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return "quit", score, player.lives
                    if event.key == K_p:
                        paused = not paused

            if paused:
                self.renderer.draw(maze, player, snipes, hives, bullets,
                                   camera, score, level_num + 1)
                pause_font = pygame.font.SysFont("monospace", 36, bold=True)
                pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
                cx = SCREEN_WIDTH // 2 - pause_text.get_width() // 2
                cy = SCREEN_HEIGHT // 2 - pause_text.get_height() // 2
                self.screen.blit(pause_text, (cx, cy))
                pygame.display.flip()
                continue

            # --- INPUT ---
            keys = pygame.key.get_pressed()

            # Movement
            mdx, mdy = 0, 0
            for key, (kx, ky) in MOVE_KEYS.items():
                if keys[key]:
                    mdx += kx
                    mdy += ky
            if mdx and mdy:
                mdx *= 0.707
                mdy *= 0.707

            if player.alive:
                dx = mdx * PLAYER_SPEED * dt
                dy = mdy * PLAYER_SPEED * dt
                player.x, player.y = move_circle(
                    player.x, player.y, dx, dy, player.radius, maze.walls
                )

            # Shooting
            shoot_timer = max(0, shoot_timer - dt)
            sdx, sdy = 0, 0
            for key, (kx, ky) in SHOOT_KEYS.items():
                if keys[key]:
                    sdx += kx
                    sdy += ky

            if (sdx or sdy) and shoot_timer <= 0 and player.alive:
                if sdx and sdy:
                    sdx_n, sdy_n = sdx * 0.707, sdy * 0.707
                else:
                    sdx_n, sdy_n = float(sdx), float(sdy)

                best_dir = None
                best_diff = float("inf")
                for name, (dvx, dvy) in DIRECTIONS.items():
                    diff = (dvx - sdx_n) ** 2 + (dvy - sdy_n) ** 2
                    if diff < best_diff:
                        best_diff = diff
                        best_dir = name

                if best_dir:
                    bullet = Bullet(
                        x=player.x, y=player.y,
                        direction=best_dir,
                        owner="player",
                    )
                    bullets.append(bullet)
                    shoot_timer = SHOOT_COOLDOWN

            # Invulnerability countdown
            if player.invulnerable > 0:
                player.invulnerable -= dt

            # --- UPDATE BULLETS ---
            for bullet in bullets:
                if bullet.alive:
                    move_bullet(bullet, dt, maze.walls)

            # --- UPDATE SNIPES ---
            for snipe in snipes:
                new_bullet = update_snipe(
                    snipe, player.x, player.y, dt, maze.walls, self.rng
                )
                if new_bullet:
                    bullets.append(new_bullet)

            # --- UPDATE HIVES ---
            alive_snipes = sum(1 for s in snipes if s.alive)
            for hive in hives:
                if not hive.alive:
                    continue
                hive.spawn_timer += dt
                if hive.spawn_timer >= hive.spawn_interval and alive_snipes < max_snipes:
                    hive.spawn_timer = 0
                    snipe = Snipe(x=hive.x, y=hive.y, speed=snipe_speed)
                    snipes.append(snipe)

            # --- COLLISIONS ---
            # Player bullets vs snipes
            for bullet in bullets:
                if not bullet.alive or bullet.owner != "player":
                    continue
                for snipe in snipes:
                    if not snipe.alive:
                        continue
                    if check_circle_collision(
                        bullet.x, bullet.y, bullet.radius,
                        snipe.x, snipe.y, snipe.radius
                    ):
                        bullet.alive = False
                        snipe.alive = False
                        score += SCORE_SNIPE
                        break

            # Player bullets vs hives
            for bullet in bullets:
                if not bullet.alive or bullet.owner != "player":
                    continue
                for hive in hives:
                    if not hive.alive:
                        continue
                    if check_circle_collision(
                        bullet.x, bullet.y, bullet.radius,
                        hive.x, hive.y, hive.radius
                    ):
                        bullet.alive = False
                        hive.health -= 1
                        if hive.health <= 0:
                            hive.alive = False
                            score += SCORE_HIVE
                        break

            # Snipe bullets vs player
            if player.alive and not player.is_invulnerable:
                for bullet in bullets:
                    if not bullet.alive or bullet.owner != "snipe":
                        continue
                    if check_circle_collision(
                        bullet.x, bullet.y, bullet.radius,
                        player.x, player.y, player.radius
                    ):
                        bullet.alive = False
                        _kill_player(player, maze)
                        break

            # Snipe contact vs player
            if player.alive and not player.is_invulnerable:
                for snipe in snipes:
                    if not snipe.alive:
                        continue
                    if check_circle_collision(
                        snipe.x, snipe.y, snipe.radius,
                        player.x, player.y, player.radius
                    ):
                        snipe.alive = False
                        _kill_player(player, maze)
                        break

            # Opposing bullets cancel
            player_bullets = [b for b in bullets if b.alive and b.owner == "player"]
            snipe_bullets = [b for b in bullets if b.alive and b.owner == "snipe"]
            for pb in player_bullets:
                for sb in snipe_bullets:
                    if not pb.alive or not sb.alive:
                        continue
                    if check_circle_collision(
                        pb.x, pb.y, pb.radius,
                        sb.x, sb.y, sb.radius
                    ):
                        pb.alive = False
                        sb.alive = False

            # --- CLEAN UP ---
            snipes = [s for s in snipes if s.alive]
            bullets = [b for b in bullets if b.alive]

            # --- WIN/LOSE ---
            if not player.alive and player.lives <= 0:
                return "dead", score, 0

            hives_left = sum(1 for h in hives if h.alive)
            if hives_left == 0 and len(snipes) == 0:
                return "win", score, player.lives

            # --- DRAW ---
            camera.update(player.x, player.y)
            self.renderer.draw(maze, player, snipes, hives, bullets,
                               camera, score, level_num + 1)
            pygame.display.flip()

    def _game_over_screen(self, victory: bool, score: int) -> str:
        """Show game over screen. Returns 'again' or 'quit'."""
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "quit"
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        return "again"
                    if event.key == K_ESCAPE:
                        return "quit"

            draw_game_over_screen(self.screen, victory, score)
            pygame.display.flip()
            self.clock.tick(30)


def _kill_player(player: Player, maze: Maze) -> None:
    """Handle player death — lose a life and respawn at center."""
    player.lives -= 1
    if player.lives > 0:
        cx, cy = maze.room_center(maze.rooms_x // 2, maze.rooms_y // 2)
        player.x = cx
        player.y = cy
        player.invulnerable = INVULNERABLE_TIME
    else:
        player.alive = False


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
