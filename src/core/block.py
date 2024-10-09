from src.core.scene import Scene
from src.utils import Vec
import pygame

class Block:
    def __init__(self, scene: Scene, pos: Vec, name: str) -> None:
        self.scene = scene
        self.pos = Vec(pos)
        self.name = name
        self.image = scene.game.assets.blocks[name]

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (0, 0, 0), (*self.screen_pos, 32, 32))
