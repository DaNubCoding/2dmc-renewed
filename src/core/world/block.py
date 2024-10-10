from src.core.scene import Scene
from src.utils import Vec
import pygame

class Block:
    def __init__(self, scene: Scene, pos: Vec, name: str) -> None:
        self.scene = scene
        self.id = scene.block_manager.ids[name]
        self.pos = Vec(pos)
        self.name = name
        self.image = scene.game.assets.blocks[name]

    @property
    def data(self) -> dict:
        return {
            "id": self.id,
        }
