from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.world.chunk_manager import ChunkManager

from src.sprites.chunk_view import ChunkView
from src.utils import Vec, iter_square
from src.core.world.block import Block
from src.core.scene import Scene
from enum import Enum, auto
from typing import Optional
from src.constants import *
from random import uniform
import json
import os

class Chunk:
    def __init__(self, scene: Scene, pos: Vec) -> None:
        self.scene = scene
        self.manager: ChunkManager = scene.chunk_manager

        self.pos = Vec(pos)
        self.region = self.pos // REGION

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

        """
        Pipeline:
        - Try to load region data from memory
          - If it doesn't exist, try to load region data from disk
            - If it doesn't exist on disk, add new region to memory
              - Generate new chunk data
            - If it does exist on disk, load region data from disk to memory
              - Load chunk data from region data
          - If it does exist, load chunk data from region data
        """

        loaded_successfully = self.try_load()
        if not loaded_successfully:
            self.generate()

        for view in self.views.values():
            self.scene.add(view)

        data = {
            "blocks": {
                layer.name.lower(): {
                    pos.iconcise: block.data
                    for pos, block in blocks.items()
                }
                for layer, blocks in self.blocks.items()
            }
        }
        with self.manager.region_data_lock:
            # Create a region data entry if it doesn't exist
            if self.region not in self.manager.region_data:
                self.manager.region_data[self.region] = {}
                print("Entering new region:", self.region)
            # Save data to the manager's region data to be saved to disk later
            self.manager.region_data[self.region][self.pos.iconcise] = data

    def try_load(self) -> bool:
        # Load region data from disk if it doesn't exist in memory
        if self.region not in self.manager.region_data:
            region_data = self.read_region_file()
            # If region data doesn't exist on disk, return False for generation
            if region_data is None: return False
            # Otherwise, load region data into memory
            with self.manager.region_data_lock:
                self.manager.region_data[self.region] = region_data

        # Load data from region data if it exists
        region_data = self.manager.region_data[self.region]
        if self.pos.iconcise not in region_data: return False

        data = region_data[self.pos.iconcise]
        # Load chunk data from region data
        for layer, blocks in data["blocks"].items():
            for pos, block_data in blocks.items():
                # Construct block object from data
                id = self.scene.block_manager.names[block_data["id"]]
                pos = Vec.from_concise(pos)
                block = Block(self.scene, pos, id)
                self.blocks[ChunkLayer[layer.upper()]][pos] = block

        return True

    def read_region_file(self) -> Optional[dict]:
        path = f"{self.manager.regions_dir}/{self.region.iconcise}.json"
        # If the region file doesn't exist, return None
        if not os.path.exists(path): return None

        # Otherwise, read the region file and return its data
        with open(path) as file:
            print("Reading region file:", path)
            return json.load(file)

    def generate(self) -> None:
        # NOTE: TEMPORARY FILL
        # Otherwise, generate a new chunk with random blocks
        for x, y in iter_square(CHUNK):
            if uniform(0, 1) < 0.25: continue
            block = Block(self.scene, self.pos + Vec(x, y), "dirt")
            self.mg_blocks[Vec(x, y)] = block

    def unload(self) -> None:
        for view in self.views.values():
            self.scene.remove(view)

class ChunkLayer(Enum):
    BG = auto()
    MG = auto()
    FG = auto()
