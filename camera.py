"""Viewport camera centered on the player."""

from __future__ import annotations

from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    """Tracks a target position and provides an offset for rendering."""

    def __init__(self, maze_width: float, maze_height: float):
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.x: float = 0
        self.y: float = 0

    def update(self, target_x: float, target_y: float) -> None:
        """Center the camera on the target."""
        self.x = target_x - SCREEN_WIDTH / 2
        self.y = target_y - SCREEN_HEIGHT / 2

    def apply(self, x: float, y: float) -> tuple[float, float]:
        """Convert world coordinates to screen coordinates."""
        return (x - self.x, y - self.y)

    def is_visible(self, x: float, y: float, margin: float = 50) -> bool:
        """Check if a world position is visible on screen."""
        sx, sy = self.apply(x, y)
        return (-margin < sx < SCREEN_WIDTH + margin and
                -margin < sy < SCREEN_HEIGHT + margin)
