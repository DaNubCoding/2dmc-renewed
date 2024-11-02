from src.core.sprite import Sprite
from src.core.scene import Scene
from src.constants import *
from src.util import *
import pygame

class Crosshair(Sprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layer.CROSSHAIR)
        self.pos = Vec(0, 0)
        pygame.mouse.set_visible(False)

    def update(self, dt: float) -> None:
        self.screen_pos = Vec(pygame.mouse.get_pos())
        self.pos = self.screen_pos + self.scene.camera.pos
        self.block_pos = self.pos // BLOCK
        self.chunk_pos = self.block_pos // CHUNK

    def draw(self, screen: pygame.Surface) -> None:
        try:
            hor_line = screen.subsurface((self.screen_pos - Vec(16, 2), (32, 4)))
            ver_line = screen.subsurface((self.screen_pos - Vec(2, 16), (4, 32)))
            inv_hor_line = invert_surface_colors(hor_line)
            inv_ver_line = invert_surface_colors(ver_line)
            screen.blit(inv_hor_line, self.screen_pos - Vec(16, 2))
            screen.blit(inv_ver_line, self.screen_pos - Vec(2, 16))
        except ValueError:
            pass
