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

    def add(self, sprite: Sprite) -> bool:
        if sprite in self.updating_sprites:
            return False
        self.updating_sprites.append(sprite)
        sprite.on_add()
        sprite.in_scene = True
        if sprite.visible:
            return self.add_rendering(sprite)
        return True

    def add_rendering(self, sprite: Sprite) -> bool:
        if sprite in self.rendering_sprites:
            return False
        self.rendering_sprites.append(sprite)
        return True

    def remove(self, sprite: Sprite) -> bool:
        try:
            self.updating_sprites.remove(sprite)
            success = True
        except ValueError:
            success = False
        sprite.on_remove()
        sprite.in_scene = False
        if sprite.visible:
            success &= self.remove_rendering(sprite)
        return success

    def remove_rendering(self, sprite: Sprite) -> bool:
        try:
            self.rendering_sprites.remove(sprite)
        except ValueError:
            return False
        return True

    def __len__(self) -> int:
        return len(self.updating_sprites)
