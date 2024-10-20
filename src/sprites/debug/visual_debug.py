from src.core.sprite import Sprite
from src.core.scene import Scene
from src.constants import *
from src.util import *
import pygame

class DebugRect(Sprite):
    def __init__(self, scene: Scene, master: WorldObject, color: Color, width: int = 1) -> None:
        super().__init__(scene, Layer.DEBUG)
        self.master = master
        self.manager = self.scene.debug_manager
        self.rect = pygame.Rect(master.pos, master.size)
        self.color = color
        self.width = width

    def update(self, dt: float) -> None:
        self.rect.topleft = self.master.screen_pos
        if not self.master.in_scene:
            self.remove()

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect, self.width)

    def add(self) -> None:
        self.manager.add(self)
        if self.manager.debug:
            self.scene.add(self)

    def remove(self) -> None:
        self.manager.remove(self)
        self.scene.remove(self)

    def toggle(self, add: bool = None) -> None:
        if add is None:
            add = self not in self.manager
        if add:
            self.add()
        else:
            self.remove()
