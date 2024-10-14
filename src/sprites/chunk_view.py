from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.world.chunk import Chunk, ChunkLayer

from src.core.sprite import CameraSprite
from src.core.render_layer import Layer
from src.core.scene import Scene
from src.constants import *
from src.util import *
import pygame

class ChunkView(CameraSprite):
    def __init__(self, scene: Scene, chunk: Chunk, chunk_layer: ChunkLayer) -> None:
        super().__init__(scene, Layer[chunk_layer.name])
        self.chunk = ref_proxy(chunk)
        self.chunk_layer = chunk_layer
        self.blocks = chunk.blocks[chunk_layer]
        self.pos = chunk.pos * BLOCKCHUNK
        # Update screen position in init so that the chunk view doesn't get
        # drawn at the wrong location for one frame
        self.screen_pos = self.pos - self.scene.camera.pos
        self.modified = True

        self.image = pygame.Surface(BLOCKCHUNKXY, pygame.SRCALPHA)

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        if not self.on_screen: return

        if self.modified:
            for pos in iter_square(CHUNK):
                if pos not in self.blocks: continue
                block = self.blocks[pos]
                self.image.blit(block.image, pos * BLOCK)
            pygame.draw.rect(self.image, (0, 255, 0), (0, 0, *BLOCKCHUNKXY), 1)
            self.modified = False

        screen.blit(self.image, self.screen_pos)

    @property
    def on_screen(self) -> bool:
        return pygame.Rect(self.screen_pos, BLOCKCHUNKXY) \
            .colliderect(pygame.Rect(0, 0, *SIZE))
