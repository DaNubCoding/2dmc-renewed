from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.render_layer import Layer
    from src.core.scene import Scene

from abc import ABC as AbstractClass, abstractmethod
from src.util import *
from uuid import uuid4
import pygame

class Sprite(AbstractClass):
    def __init__(self, scene: Scene, layer: Layer) -> None:
        self.uuid = uuid4()
        self.game = scene.game
        self.scene = ref_proxy(scene)
        self.layer = layer
        self.pos = Vec(0, 0)
        self._visible = True

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass

    def post_update(self, dt: float) -> None:
        # Not all sprites need to implement this method, so it's not abstract
        pass

    def remove(self) -> None:
        self.scene.sprite_manager.remove(self)

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        self._visible = value
        if value:
            self.scene.sprite_manager.add_rendering(self)
        else:
            try:
                self.scene.sprite_manager.remove_rendering(self)
            except ValueError:
                pass

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}{{{self.uuid}}}"

    def __repr__(self) -> str:
        return self.__str__()

class HeadlessSprite(Sprite):
    def __init__(self, scene: Scene, layer: Layer) -> None:
        super().__init__(scene, layer)
        self._visible = False

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        # Headless sprites don't need to be drawn. This is just here to satisfy
        # the abstract method so that subclasses don't have to implement it
        pass

class CameraSprite(Sprite):
    def __init__(self, scene: Scene, layer: Layer) -> None:
        super().__init__(scene, layer)
        self.screen_pos = self.pos

    def post_update(self, dt: float) -> None:
        self.screen_pos = self.pos - self.scene.camera.pos

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass
