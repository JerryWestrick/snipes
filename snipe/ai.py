"""Snipe AI behavior."""

from __future__ import annotations

import random
import math
from snipe.entities import Snipe, Bullet
from snipe.settings import DIRECTIONS, SNIPE_SHOOT_CHANCE
from snipe.physics import move_circle


_DIR_NAMES = list(DIRECTIONS.keys())


def update_snipe(snipe: Snipe, player_x: float, player_y: float,
                 dt: float, walls: list, rng: random.Random) -> Bullet | None:
    """Update a snipe's movement and maybe shoot. Returns a bullet or None."""
    if not snipe.alive:
        return None

    # Movement timer
    snipe.move_timer += dt
    if snipe.move_timer >= snipe.move_interval:
        snipe.move_timer = 0.0
        snipe.direction = _pick_direction(snipe, player_x, player_y, rng)

    # Move in current direction
    dvx, dvy = DIRECTIONS[snipe.direction]
    dx = dvx * snipe.speed * dt
    dy = dvy * snipe.speed * dt
    snipe.x, snipe.y = move_circle(snipe.x, snipe.y, dx, dy, snipe.radius, walls)

    # Maybe shoot
    if rng.random() < SNIPE_SHOOT_CHANCE:
        return _shoot_at_player(snipe, player_x, player_y)
    return None


def _pick_direction(snipe: Snipe, player_x: float, player_y: float,
                    rng: random.Random) -> str:
    """Pick a direction biased toward the player."""
    dx = player_x - snipe.x
    dy = player_y - snipe.y

    # Target direction components
    tx = 1 if dx > 0 else (-1 if dx < 0 else 0)
    ty = 1 if dy > 0 else (-1 if dy < 0 else 0)

    # Weight directions toward player
    candidates = []
    for name, (dvx, dvy) in DIRECTIONS.items():
        weight = 1
        # Normalize diagonal components for comparison
        sx = 1 if dvx > 0 else (-1 if dvx < 0 else 0)
        sy = 1 if dvy > 0 else (-1 if dvy < 0 else 0)
        if sx == tx and tx != 0:
            weight += 2
        if sy == ty and ty != 0:
            weight += 2
        candidates.extend([name] * weight)

    return rng.choice(candidates)


def _shoot_at_player(snipe: Snipe, player_x: float, player_y: float) -> Bullet:
    """Shoot toward the player using the nearest of 8 directions."""
    dx = player_x - snipe.x
    dy = player_y - snipe.y
    angle = math.atan2(dy, dx)

    # Find nearest of 8 directions
    best_dir = "N"
    best_diff = float("inf")
    for name, (dvx, dvy) in DIRECTIONS.items():
        dir_angle = math.atan2(dvy, dvx)
        diff = abs(angle - dir_angle)
        if diff > math.pi:
            diff = 2 * math.pi - diff
        if diff < best_diff:
            best_diff = diff
            best_dir = name

    return Bullet(
        x=snipe.x,
        y=snipe.y,
        direction=best_dir,
        owner="snipe",
    )
