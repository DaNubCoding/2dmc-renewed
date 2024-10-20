from src.sprites.debug.visual_debug import DebugRect
from src.sprites.debug.debug_menu import DebugMenu
from src.core.sprite import HeadlessSprite
from src.core.scene import Scene
from src.constants import *
import pygame

class DebugManager(HeadlessSprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layer.DEBUG)
        self.debug = False

        self.debug_menu = DebugMenu(self.scene)
        self.scene.add(self.debug_menu)

        self.debug_rects = []

    def update(self, dt: float) -> None:
        if self.game.key_down == pygame.K_F3:
            self.toggle()

    def toggle(self) -> None:
        self.debug_menu.toggle()
        self.debug = not self.debug
        if self.debug:
            for rect in self.debug_rects:
                self.scene.add(rect)
        else:
            for rect in self.debug_rects:
                self.scene.remove(rect)

    def add(self, rect: DebugRect) -> None:
        if rect not in self.debug_rects:
            self.debug_rects.append(rect)
        if self.debug:
            self.scene.add(rect)

    def remove(self, rect: DebugRect) -> None:
        try:
            self.debug_rects.remove(rect)
        except ValueError:
            pass
        if self.debug:
            self.scene.remove(rect)

    def __contains__(self, rect: DebugRect) -> bool:
        return rect in self.debug_rects
