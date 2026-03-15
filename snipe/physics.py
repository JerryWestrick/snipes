"""Movement, collision, and ricochet."""

from __future__ import annotations

import pygame
from snipe.settings import DIRECTIONS, RICOCHET
from snipe.entities import Bullet


def move_circle(x: float, y: float, dx: float, dy: float, radius: float,
                walls: list[pygame.Rect]) -> tuple[float, float]:
    """Move a circle by (dx, dy), sliding along walls.

    Returns the new (x, y) position.
    """
    # Try full move
    new_x = x + dx
    new_y = y + dy

    # Check X axis
    if _circle_hits_any_wall(new_x, y, radius, walls):
        new_x = x  # revert X

    # Check Y axis
    if _circle_hits_any_wall(new_x, new_y, radius, walls):
        new_y = y  # revert Y

    return new_x, new_y


def move_bullet(bullet: Bullet, dt: float, walls: list[pygame.Rect]) -> None:
    """Move a bullet, handle wall ricochet or death."""
    bullet.age += dt
    if bullet.age >= bullet.max_age:
        bullet.alive = False
        return

    dx = bullet.vx * dt
    dy = bullet.vy * dt
    new_x = bullet.x + dx
    new_y = bullet.y + dy

    # Check wall collision
    hit_wall, wall_face = _bullet_wall_check(new_x, new_y, bullet.radius, walls)
    if hit_wall:
        result = RICOCHET.get((bullet.direction, wall_face))
        if result is None:
            # Cardinal hit perpendicular wall — bullet dies
            bullet.alive = False
        else:
            # Ricochet — change direction, don't move this frame
            bullet.direction = result
    else:
        bullet.x = new_x
        bullet.y = new_y


def check_circle_collision(x1: float, y1: float, r1: float,
                           x2: float, y2: float, r2: float) -> bool:
    """Check if two circles overlap."""
    dx = x1 - x2
    dy = y1 - y2
    dist_sq = dx * dx + dy * dy
    radii = r1 + r2
    return dist_sq < radii * radii


def _circle_hits_any_wall(x: float, y: float, radius: float,
                          walls: list[pygame.Rect]) -> bool:
    """Check if a circle at (x, y) overlaps any wall rect."""
    for wall in walls:
        if _circle_rect_overlap(x, y, radius, wall):
            return True
    return False


def _circle_rect_overlap(cx: float, cy: float, radius: float,
                         rect: pygame.Rect) -> bool:
    """Check if a circle overlaps a rectangle."""
    # Find closest point on rect to circle center
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))
    dx = cx - closest_x
    dy = cy - closest_y
    return (dx * dx + dy * dy) < (radius * radius)


def _bullet_wall_check(x: float, y: float, radius: float,
                       walls: list[pygame.Rect]) -> tuple[bool, str]:
    """Check if a bullet at (x,y) hits a wall. Returns (hit, face).

    face is "H" for horizontal wall (top/bottom face hit)
    or "V" for vertical wall (left/right face hit).
    """
    for wall in walls:
        if not _circle_rect_overlap(x, y, radius, wall):
            continue

        # Determine which face was hit based on circle center vs rect center
        wcx = wall.centerx
        wcy = wall.centery

        # Distance from circle center to wall center
        dx = x - wcx
        dy = y - wcy

        # Compare overlap on each axis relative to wall dimensions
        overlap_x = (wall.width / 2 + radius) - abs(dx)
        overlap_y = (wall.height / 2 + radius) - abs(dy)

        if overlap_x < overlap_y:
            return True, "V"  # hit left or right face
        else:
            return True, "H"  # hit top or bottom face

    return False, ""
