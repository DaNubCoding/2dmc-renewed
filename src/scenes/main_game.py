from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from src.core.world.chunk_manager import ChunkManager
from src.core.world.block_manager import BlockManager
from src.sprites.debug_menu import DebugMenu
from src.sprites.camera import Camera
from src.core.scene import Scene
import pygame

class MainScene(Scene):
    def __init__(self, game: Game, world_name: str) -> None:
        super().__init__(game)
        self.camera = Camera(self)
        self.add(self.camera)

        self.block_manager = BlockManager()
        self.chunk_manager = ChunkManager(self, world_name)
        self.chunk_manager.start()

        self.debug_menu = DebugMenu(self)
        self.add(self.debug_menu)

    def update(self, dt: float) -> None:
        if self.game.key_down == pygame.K_F3:
            self.debug_menu.toggle()

        self.sprite_manager.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((120, 167, 255))
        self.sprite_manager.draw(screen)

    def quit(self) -> None:
        self.chunk_manager.quit()
