from src.core.sprite import HeadlessSprite, Sprite
from src.core.render_layer import Layer
from src.core.scene import Scene
from src.utils import Vec
import pygame

class Camera(HeadlessSprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layer.PLAYER)
        self.pos = Vec(0, 0)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pos.y -= 5 * dt
        if keys[pygame.K_s]:
            self.pos.y += 5 * dt
        if keys[pygame.K_a]:
            self.pos.x -= 5 * dt
        if keys[pygame.K_d]:
            self.pos.x += 5 * dt