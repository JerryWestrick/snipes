"""Game entities — all positioned with float coordinates."""

from __future__ import annotations

from dataclasses import dataclass, field
from snipe.settings import (
    PLAYER_RADIUS, PLAYER_SPEED, PLAYER_START_LIVES,
    SNIPE_RADIUS, SNIPE_SPEED, SNIPE_MOVE_INTERVAL,
    HIVE_RADIUS,
    BULLET_RADIUS, BULLET_SPEED, BULLET_MAX_AGE,
    DIRECTIONS,
)


@dataclass
class Player:
    x: float
    y: float
    radius: float = PLAYER_RADIUS
    speed: float = PLAYER_SPEED
    lives: int = PLAYER_START_LIVES
    alive: bool = True
    invulnerable: float = 0.0  # seconds remaining

    @property
    def is_invulnerable(self) -> bool:
        return self.invulnerable > 0


@dataclass
class Bullet:
    x: float
    y: float
    direction: str  # one of the 8 direction keys: "N", "NE", etc.
    owner: str  # "player" or "snipe"
    radius: float = BULLET_RADIUS
    speed: float = BULLET_SPEED
    age: float = 0.0
    max_age: float = BULLET_MAX_AGE
    alive: bool = True

    @property
    def vx(self) -> float:
        return DIRECTIONS[self.direction][0] * self.speed

    @property
    def vy(self) -> float:
        return DIRECTIONS[self.direction][1] * self.speed


@dataclass
class Snipe:
    x: float
    y: float
    direction: str = "N"
    radius: float = SNIPE_RADIUS
    speed: float = SNIPE_SPEED
    alive: bool = True
    move_timer: float = 0.0
    move_interval: float = SNIPE_MOVE_INTERVAL


@dataclass
class Hive:
    x: float
    y: float
    radius: float = HIVE_RADIUS
    health: int = 1
    alive: bool = True
    spawn_timer: float = 0.0
    spawn_interval: float = 6.0
