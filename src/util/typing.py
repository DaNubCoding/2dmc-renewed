from typing import Protocol as _Protocol

from pygame.typing import (
    Point as Coord,
    IntPoint as IntCoord,
    ColorLike as Color,
    RectLike as Rect,
)

class WorldObject(_Protocol):
    in_scene: bool
    pos: Coord
    screen_pos: Coord
    size: IntCoord
