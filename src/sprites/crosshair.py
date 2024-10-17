from src.core.sprite import Sprite
from src.core.scene import Scene
from src.constants import *
from src.util import *
import pygame

class Crosshair(Sprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layer.CROSSHAIR)
        self.pos = Vec(0, 0)

    def update(self, dt: float) -> None:
        self.screen_pos = Vec(pygame.mouse.get_pos())
        self.pos = self.screen_pos + self.scene.camera.pos
        self.block_pos = self.pos // BLOCK
        self.chunk_pos = self.block_pos // CHUNK

    def draw(self, screen) -> None:
        # TODO: Draw the crosshair image at self.pos
        pass
