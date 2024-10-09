from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.world.chunk import Chunk, ChunkLayer

from src.core.sprite import CameraSprite
from src.core.render_layer import Layer
from src.utils import Vec, iter_square
from src.core.scene import Scene
from src.constants import *
import pygame

class ChunkView(CameraSprite):
    def __init__(self, scene: Scene, chunk: Chunk, chunk_layer: ChunkLayer) -> None:
        super().__init__(scene, Layer[chunk_layer.name])
        self.chunk = chunk
        self.chunk_layer = chunk_layer
        self.blocks = chunk.blocks[chunk_layer]
        self.pos = chunk.pos
        self.modified = True

        self.image = pygame.Surface(BLOCKCHUNKXY, pygame.SRCALPHA)

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        if self.modified:
            for pos in iter_square(CHUNK):
                if pos not in self.blocks: continue
                block = self.blocks[pos]
                self.image.blit(block.image, pos * BLOCK)
            self.modified = False

        screen.blit(self.image, self.screen_pos)
