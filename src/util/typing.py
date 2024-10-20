from typing import Protocol

from pygame.typing import (
    Point as Coord,
    IntPoint as IntCoord,
    ColorLike as Color,
    RectLike as Rect,
)

class WorldObject(Protocol):
    in_scene: bool
    pos: Coord
    screen_pos: Coord
    size: IntCoord

__all__ = [
    "Coord",
    "IntCoord",
    "Color",
    "Rect",
    "WorldObject",
]
