from src.core.sprite import Sprite
from typing import Callable
import pygame

class RenderLayer:
    def __init__(self, key: Callable[[Sprite], int] = None) -> None:
        self.key = key
        self.updating_sprites: list[Sprite] = []
        self.rendering_sprites: list[Sprite] = []

    def update(self, dt: float) -> None:
        for sprite in self.updating_sprites:
            sprite.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        if self.key is not None:
            self.rendering_sprites.sort(key=self.key)

        for sprite in self.rendering_sprites:
            sprite.pre_render()
            sprite.draw(screen)

    def add(self, sprite: Sprite) -> None:
        self.updating_sprites.append(sprite)
        if sprite.visible:
            self.add_rendering(sprite)

    def add_rendering(self, sprite: Sprite) -> None:
        self.rendering_sprites.append(sprite)

    def remove(self, sprite: Sprite) -> None:
        self.updating_sprites.remove(sprite)
        if sprite.visible:
            self.remove_rendering(sprite)

    def remove_rendering(self, sprite: Sprite) -> None:
        self.rendering_sprites.remove(sprite)

    def __len__(self) -> int:
        return len(self.updating_sprites)
