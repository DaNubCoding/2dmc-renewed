from src.core.sprite import CameraSprite
from src.core.render_layer import Layer
from src.core.scene import Scene
from src.utils import Vec
import pygame

class Block(CameraSprite):
    def __init__(self, scene: Scene, pos: Vec) -> None:
        super().__init__(scene, Layer.MIDDLEGROUND)
        self.pos = Vec(pos)

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (0, 0, 0), (*self.screen_pos, 32, 32))
