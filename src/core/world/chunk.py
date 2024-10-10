from __future__ import annotations

from src.sprites.chunk_view import ChunkView
from src.utils import Vec, iter_square
from src.core.world.block import Block
from src.core.scene import Scene
from enum import Enum, auto
from src.constants import *
from random import uniform

class Chunk:
    def __init__(self, scene: Scene, pos: Vec) -> None:
        self.scene = scene
        self.pos = Vec(pos)

        self.bg_blocks: dict[Vec, Block] = {}
        self.mg_blocks: dict[Vec, Block] = {}
        self.fg_blocks: dict[Vec, Block] = {}
        self.blocks = {
            ChunkLayer.BG: self.bg_blocks,
            ChunkLayer.MG: self.mg_blocks,
            ChunkLayer.FG: self.fg_blocks,
        }
        self.views = {
            ChunkLayer.BG: ChunkView(self.scene, self, ChunkLayer.BG),
            ChunkLayer.MG: ChunkView(self.scene, self, ChunkLayer.MG),
            ChunkLayer.FG: ChunkView(self.scene, self, ChunkLayer.FG),
        }

        # NOTE: TEMPORARY FILL
        for x, y in iter_square(CHUNK):
            if uniform(0, 1) < 0.25: continue
            self.mg_blocks[Vec(x, y)] = Block(self.scene, self.pos + Vec(x, y), "dirt")

        for view in self.views.values():
            self.scene.add(view)

    def unload(self) -> None:
        for view in self.views.values():
            self.scene.remove(view)

class ChunkLayer(Enum):
    BG = auto()
    MG = auto()
    FG = auto()
