from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.world.chunk_manager import ChunkManager

from src.sprites.chunk_view import ChunkView
from src.util.enum_dict import IntEnumDict
from src.core.world.block import Block
from src.core.scene import Scene
from typing import Optional
from src.constants import *
from src.util import *
from math import floor
import json
import os

class Chunk:
    def __init__(self, scene: Scene, pos: Vec) -> None:
        self.scene = ref_proxy(scene)
        self.manager: ChunkManager = ref_proxy(scene.chunk_manager)
        self.seed = self.manager.seed
        self.noise = self.manager.noise

        self.pos = Vec(pos)
        self.region = self.pos // REGION

        self.blocks = IntEnumDict(ChunkLayer)
        for layer in ChunkLayer:
            self.blocks[layer] = {}

        self.views = IntEnumDict(ChunkLayer)
        for layer in ChunkLayer:
            self.views[layer] = ChunkView(self.scene, self, layer)

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
        for pos in iter_square(CHUNK):
            world_pos = self.pos * CHUNK + pos
            terrain_height = floor(self.noise([world_pos.x / 250]) * 25)
            if world_pos.y > terrain_height + 4:
                block = Block(self.scene, world_pos, "stone")
                self.blocks["MG"][pos] = block
            elif world_pos.y > terrain_height:
                block = Block(self.scene, world_pos, "dirt")
                self.blocks["MG"][pos] = block
            elif world_pos.y == terrain_height:
                block = Block(self.scene, world_pos, "grass_block")
                self.blocks["MG"][pos] = block

    def unload(self) -> None:
        for view in self.views.values():
            self.scene.remove(view)
