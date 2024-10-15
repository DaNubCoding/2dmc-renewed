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
        # Whether the chunk view is sticky to the layer above it
        # Sticky chunk views will not be drawn, and will instead be drawn as
        # part of the chunk view above it
        # NOTE: in future, this will be set to False when things need to be
        # rendered in between layers
        self.sticky = True

        self.image = pygame.Surface(BLOCKCHUNKXY, pygame.SRCALPHA)

    def update(self, dt: float) -> None:
        self.visible = not self.sticky or \
            self.chunk_layer.value == len(ChunkLayer)

    def draw(self, screen: pygame.Surface) -> None:
        if not self.on_screen: return

        if self.modified:
            self.redraw()

        screen.blit(self.image, self.screen_pos)

        color = (0, 255, 0)
        if self.chunk_layer == ChunkLayer.MG:
            color = (0, 180, 0)
        elif self.chunk_layer == ChunkLayer.BG:
            color = (0, 100, 0)
        width = (4 - self.chunk_layer.value) * 2
        pygame.draw.rect(screen, color, (*self.screen_pos, *BLOCKCHUNKXY), width)

    def redraw(self) -> None:
        for layer in self.chunk.blocks:
            view = self.chunk.views[layer]
            # If we have reached the layer that this view is responsible for,
            # draw the blocks in that layer and stop
            if layer == self.chunk_layer:
                for pos, block in self.chunk.blocks[layer].items():
                    self.image.blit(block.image, pos * BLOCK)
                break
            # If we are on a layer below the layer that this view is
            # responsible for, and the view is not sticky, let that view draw
            # its own blocks (hence do nothing). If the view is sticky, draw
            # the blocks in that view onto this view
            if not view.sticky: break
            if view.modified:
                view.redraw()
            self.image.blit(view.image, (0, 0))

        self.modified = False

    @property
    def on_screen(self) -> bool:
        return pygame.Rect(self.screen_pos, BLOCKCHUNKXY) \
            .colliderect(pygame.Rect(0, 0, *SIZE))
