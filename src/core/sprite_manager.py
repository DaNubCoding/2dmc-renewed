from src.core.render_layer import RenderLayer
from src.core.sprite import Sprite
from src.constants import *
import pygame

class SpriteManager:
    def __init__(self) -> None:
        self.layers = {layer: RenderLayer() for layer in Layer}

    def update(self, dt: float) -> None:
        for layer in self.layers.values():
            layer.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        for layer in self.layers.values():
            layer.draw(screen)

    def add(self, sprite: Sprite) -> None:
        self.layers[sprite.layer].add(sprite)

    def add_rendering(self, sprite: Sprite) -> None:
        self.layers[sprite.layer].add_rendering(sprite)

    def remove(self, sprite: Sprite) -> None:
        self.layers[sprite.layer].remove(sprite)

    def remove_rendering(self, sprite: Sprite) -> None:
        self.layers[sprite.layer].remove_rendering(sprite)
