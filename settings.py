"""Game constants."""

import pygame

# Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Maze layout (base — overridden per level)
CORRIDOR_WIDTH = 60  # pixels
WALL_THICKNESS = 8   # pixels
ROOM_SIZE = CORRIDOR_WIDTH + WALL_THICKNESS

# Player
PLAYER_RADIUS = 8
PLAYER_SPEED = 150  # pixels per second
PLAYER_START_LIVES = 5
INVULNERABLE_TIME = 2.0  # seconds

# Bullets
BULLET_RADIUS = 3
BULLET_SPEED = 300  # pixels per second
BULLET_MAX_AGE = 1.5  # seconds
SHOOT_COOLDOWN = 0.15  # seconds between shots

# Snipes
SNIPE_RADIUS = 8
SNIPE_SPEED = 80  # pixels per second
SNIPE_SHOOT_CHANCE = 0.01  # per frame chance
SNIPE_MOVE_INTERVAL = 0.5  # seconds between direction changes

# Hives
HIVE_RADIUS = 12

# Scoring
SCORE_SNIPE = 10
SCORE_HIVE = 50

# Level definitions: (rooms_x, rooms_y, num_hives, max_snipes, hive_health, spawn_interval, snipe_speed)
LEVELS = [
    # Level 1: small, easy
    {"rooms_x": 8,  "rooms_y": 6,  "hives": 2, "max_snipes": 6,  "hive_health": 1, "spawn_interval": 8.0, "snipe_speed": 60},
    # Level 2
    {"rooms_x": 10, "rooms_y": 8,  "hives": 3, "max_snipes": 10, "hive_health": 1, "spawn_interval": 6.0, "snipe_speed": 70},
    # Level 3
    {"rooms_x": 12, "rooms_y": 9,  "hives": 4, "max_snipes": 15, "hive_health": 1, "spawn_interval": 5.0, "snipe_speed": 80},
    # Level 4
    {"rooms_x": 14, "rooms_y": 10, "hives": 5, "max_snipes": 20, "hive_health": 2, "spawn_interval": 5.0, "snipe_speed": 90},
    # Level 5
    {"rooms_x": 16, "rooms_y": 12, "hives": 6, "max_snipes": 25, "hive_health": 2, "spawn_interval": 4.0, "snipe_speed": 100},
    # Level 6
    {"rooms_x": 18, "rooms_y": 13, "hives": 7, "max_snipes": 30, "hive_health": 2, "spawn_interval": 4.0, "snipe_speed": 110},
    # Level 7
    {"rooms_x": 20, "rooms_y": 15, "hives": 8, "max_snipes": 40, "hive_health": 3, "spawn_interval": 3.5, "snipe_speed": 120},
    # Level 8
    {"rooms_x": 22, "rooms_y": 16, "hives": 9, "max_snipes": 50, "hive_health": 3, "spawn_interval": 3.0, "snipe_speed": 130},
    # Level 9
    {"rooms_x": 25, "rooms_y": 18, "hives": 10, "max_snipes": 60, "hive_health": 4, "spawn_interval": 2.5, "snipe_speed": 140},
]

# Colors
COLOR_BG = (10, 10, 15)
COLOR_WALL = (60, 60, 70)
COLOR_PLAYER = (50, 255, 80)
COLOR_PLAYER_INV = (255, 255, 255)
COLOR_SNIPE = (255, 60, 60)
COLOR_SNIPE_GHOST = (60, 220, 255)
COLOR_HIVE = (220, 60, 255)
COLOR_BULLET_PLAYER = (255, 255, 50)
COLOR_BULLET_SNIPE = (255, 80, 80)
COLOR_HUD_TEXT = (200, 200, 200)
COLOR_HUD_BG = (20, 20, 30)

# 8 directions as (dx, dy) unit-ish vectors
# Cardinal = axis-aligned, Diagonal = 0.707 each
DIRECTIONS = {
    "N":  (0, -1),
    "NE": (0.707, -0.707),
    "E":  (1, 0),
    "SE": (0.707, 0.707),
    "S":  (0, 1),
    "SW": (-0.707, 0.707),
    "W":  (-1, 0),
    "NW": (-0.707, -0.707),
}

# Ricochet table: (direction, wall_face) -> new_direction or None (dead)
# Wall faces: "H" = horizontal (top/bottom), "V" = vertical (left/right)
RICOCHET = {
    ("N",  "H"): "S",   ("N",  "V"): None,
    ("NE", "H"): "SE",  ("NE", "V"): "NW",
    ("E",  "H"): None,  ("E",  "V"): "W",
    ("S",  "H"): "N",   ("S",  "V"): None,
    ("SE", "H"): "NE",  ("SE", "V"): "SW",
    ("W",  "H"): None,  ("W",  "V"): "E",
    ("SW", "H"): "NW",  ("SW", "V"): "SE",
    ("NW", "H"): "SW",  ("NW", "V"): "NE",
}

# Key mappings
MOVE_KEYS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}

SHOOT_KEYS = {
    pygame.K_w: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_a: (-1, 0),
    pygame.K_d: (1, 0),
}
