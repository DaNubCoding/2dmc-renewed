from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from src.core.world.chunk_manager import ChunkManager
from src.utils import Vec, iter_square
from src.sprites.camera import Camera
from src.core.world.chunk import Chunk
from src.core.scene import Scene
import pygame

class MainScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.camera = Camera(self) # 296 q1-8, 10, 11
        self.add(self.camera)

        self.chunk_manager = ChunkManager(self)
        self.chunk_manager.start()

    def update(self, dt: float) -> None:
        self.sprite_manager.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((120, 167, 255))
        self.sprite_manager.draw(screen)
