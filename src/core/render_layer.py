from src.util.deferred_dict import DeferredDict
from src.core.sprite import Sprite
from uuid import UUID
import pygame

class RenderLayer:
    def __init__(self) -> None:
        self.updating_sprites = DeferredDict[UUID, Sprite]()
        self.rendering_sprites = DeferredDict[UUID, Sprite]()

    def update(self, dt: float) -> None:
        for sprite in self.updating_sprites.values():
            sprite.update(dt)
        self.updating_sprites.commit()

    def draw(self, screen: pygame.Surface) -> None:
        for sprite in self.rendering_sprites.values():
            sprite.pre_render()
            sprite.draw(screen)
        self.rendering_sprites.commit()

    def add(self, sprite: Sprite) -> bool:
        if sprite.uuid in self.updating_sprites:
            return False
        self.updating_sprites[sprite.uuid] = sprite
        sprite.on_add()
        sprite.in_scene = True
        if sprite.visible:
            return self.add_rendering(sprite)
        return True

    def add_rendering(self, sprite: Sprite) -> bool:
        if sprite.uuid in self.rendering_sprites:
            return False
        self.rendering_sprites[sprite.uuid] = sprite
        return True

    def remove(self, sprite: Sprite) -> bool:
        success = bool(self.updating_sprites.pop(sprite.uuid, False))
        sprite.on_remove()
        sprite.in_scene = False
        if sprite.visible:
            success &= self.remove_rendering(sprite)
        return success

    def remove_rendering(self, sprite: Sprite) -> bool:
        return bool(self.rendering_sprites.pop(sprite.uuid, False))

    def __len__(self) -> int:
        return len(self.updating_sprites)
