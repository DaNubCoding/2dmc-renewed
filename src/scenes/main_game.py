from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from src.sprites.camera import Camera
from src.sprites.block import Block
from src.core.scene import Scene
import pygame

class MainScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.camera = Camera(self)
        self.add(self.camera)
        for x in range(100):
            for y in range(100):
                self.add(Block(self, (x * 32, y * 32)))

    def update(self, dt: float) -> None:
        self.sprite_manager.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((120, 167, 255))
        self.sprite_manager.draw(screen)
