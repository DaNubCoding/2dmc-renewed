from src.core.sprite import HeadlessSprite
from src.core.scene import Scene
from src.constants import *
from src.util import *
import pygame

class Camera(HeadlessSprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layer.PLAYER)
        self.pos = Vec(0, 0)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pos.y -= 400 * dt
        if keys[pygame.K_s]:
            self.pos.y += 400 * dt
        if keys[pygame.K_a]:
            self.pos.x -= 400 * dt
        if keys[pygame.K_d]:
            self.pos.x += 400 * dt
