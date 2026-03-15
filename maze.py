"""Maze generation — outputs a list of wall rectangles."""

from __future__ import annotations

import random
import pygame
from settings import CORRIDOR_WIDTH, WALL_THICKNESS, ROOM_SIZE


class Maze:
    """A maze defined as wall geometry (list of pygame.Rect).

    Layout: rooms are open rectangles connected by passages.
    Walls are solid rectangles between rooms.
    """

    def __init__(self, rooms_x: int = 10, rooms_y: int = 8, seed: int | None = None):
        self.rooms_x = rooms_x
        self.rooms_y = rooms_y
        self.width = rooms_x * ROOM_SIZE + WALL_THICKNESS
        self.height = rooms_y * ROOM_SIZE + WALL_THICKNESS
        self._rng = random.Random(seed)

        # Track which walls are open (passages carved)
        # h_walls[ry][rx] = True means wall BELOW room (rx,ry) is open
        # v_walls[ry][rx] = True means wall RIGHT of room (rx,ry) is open
        self._h_open = [[False] * self.rooms_x for _ in range(self.rooms_y)]
        self._v_open = [[False] * self.rooms_x for _ in range(self.rooms_y)]

        self._generate()
        self.walls: list[pygame.Rect] = self._build_wall_rects()

    def room_center(self, rx: int, ry: int) -> tuple[float, float]:
        """Get the pixel center of a room."""
        x = WALL_THICKNESS + rx * ROOM_SIZE + CORRIDOR_WIDTH / 2
        y = WALL_THICKNESS + ry * ROOM_SIZE + CORRIDOR_WIDTH / 2
        return (x, y)

    def _generate(self) -> None:
        """Carve maze using recursive backtracker, then add loops."""
        visited = set()
        start = (0, 0)
        visited.add(start)
        stack = [start]

        while stack:
            rx, ry = stack[-1]
            neighbors = []
            for drx, dry in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = rx + drx, ry + dry
                if 0 <= nx < self.rooms_x and 0 <= ny < self.rooms_y and (nx, ny) not in visited:
                    neighbors.append((nx, ny, drx, dry))

            if neighbors:
                nx, ny, drx, dry = self._rng.choice(neighbors)
                # Open the wall between (rx,ry) and (nx,ny)
                if drx == 1:   # going right
                    self._v_open[ry][rx] = True
                elif drx == -1:  # going left
                    self._v_open[ny][nx] = True
                elif dry == 1:   # going down
                    self._h_open[ry][rx] = True
                elif dry == -1:  # going up
                    self._h_open[ny][nx] = True
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        self._add_loops()

    def _add_loops(self, factor: float = 0.15) -> None:
        """Open some extra walls to create loops."""
        closed_walls = []
        for ry in range(self.rooms_y):
            for rx in range(self.rooms_x):
                if rx < self.rooms_x - 1 and not self._v_open[ry][rx]:
                    closed_walls.append(("v", rx, ry))
                if ry < self.rooms_y - 1 and not self._h_open[ry][rx]:
                    closed_walls.append(("h", rx, ry))

        num_to_open = int(len(closed_walls) * factor)
        for kind, rx, ry in self._rng.sample(closed_walls, min(num_to_open, len(closed_walls))):
            if kind == "v":
                self._v_open[ry][rx] = True
            else:
                self._h_open[ry][rx] = True

    def _build_wall_rects(self) -> list[pygame.Rect]:
        """Convert the logical maze into wall rectangles."""
        walls = []
        wt = WALL_THICKNESS
        cw = CORRIDOR_WIDTH
        rs = ROOM_SIZE

        # Outer border
        walls.append(pygame.Rect(0, 0, self.width, wt))                    # top
        walls.append(pygame.Rect(0, self.height - wt, self.width, wt))     # bottom
        walls.append(pygame.Rect(0, 0, wt, self.height))                   # left
        walls.append(pygame.Rect(self.width - wt, 0, wt, self.height))     # right

        # Horizontal interior walls (between rows of rooms)
        for ry in range(self.rooms_y - 1):
            wall_y = wt + (ry + 1) * rs - wt  # top of the wall strip
            for rx in range(self.rooms_x):
                if not self._h_open[ry][rx]:
                    # Wall is solid — full width of this room column
                    wall_x = wt + rx * rs - wt
                    # Extend wall to cover from left pillar to right pillar
                    walls.append(pygame.Rect(
                        wt + rx * rs,
                        wall_y,
                        cw,
                        wt,
                    ))

            # Pillars at intersections (always solid)
            for rx in range(self.rooms_x + 1):
                pillar_x = rx * rs
                walls.append(pygame.Rect(pillar_x, wall_y, wt, wt))

        # Vertical interior walls (between columns of rooms)
        for rx in range(self.rooms_x - 1):
            wall_x = wt + (rx + 1) * rs - wt
            for ry in range(self.rooms_y):
                if not self._v_open[ry][rx]:
                    walls.append(pygame.Rect(
                        wall_x,
                        wt + ry * rs,
                        wt,
                        cw,
                    ))

            # Pillars at intersections (always solid)
            for ry in range(self.rooms_y + 1):
                pillar_y = ry * rs
                walls.append(pygame.Rect(wall_x, pillar_y, wt, wt))

        return walls

    def find_dead_end_rooms(self) -> list[tuple[int, int]]:
        """Find rooms with only one passage."""
        dead_ends = []
        for ry in range(self.rooms_y):
            for rx in range(self.rooms_x):
                openings = 0
                if rx > 0 and self._v_open[ry][rx - 1]:
                    openings += 1
                if rx < self.rooms_x - 1 and self._v_open[ry][rx]:
                    openings += 1
                if ry > 0 and self._h_open[ry - 1][rx]:
                    openings += 1
                if ry < self.rooms_y - 1 and self._h_open[ry][rx]:
                    openings += 1
                if openings == 1:
                    dead_ends.append((rx, ry))
        return dead_ends

    def find_hive_rooms(self, num_hives: int, player_room: tuple[int, int]) -> list[tuple[int, int]]:
        """Find rooms for hives, spread out and away from player."""
        dead_ends = self.find_dead_end_rooms()
        self._rng.shuffle(dead_ends)

        prx, pry = player_room
        min_dist = max(self.rooms_x, self.rooms_y) // 3

        candidates = [
            (rx, ry) for rx, ry in dead_ends
            if abs(rx - prx) + abs(ry - pry) > min_dist
        ]

        # Add random rooms if not enough dead ends
        if len(candidates) < num_hives:
            all_rooms = [
                (rx, ry)
                for ry in range(self.rooms_y)
                for rx in range(self.rooms_x)
                if abs(rx - prx) + abs(ry - pry) > min_dist
                   and (rx, ry) not in candidates
            ]
            self._rng.shuffle(all_rooms)
            candidates.extend(all_rooms)

        # Select with spacing
        selected = []
        min_hive_dist = max(self.rooms_x, self.rooms_y) // 4
        for rx, ry in candidates:
            if len(selected) >= num_hives:
                break
            if all(abs(rx - sx) + abs(ry - sy) > min_hive_dist for sx, sy in selected):
                selected.append((rx, ry))

        # Relax if needed
        if len(selected) < num_hives:
            for rx, ry in candidates:
                if len(selected) >= num_hives:
                    break
                if (rx, ry) not in selected:
                    selected.append((rx, ry))

        return selected[:num_hives]
