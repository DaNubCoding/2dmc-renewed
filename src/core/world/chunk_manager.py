from src.core.world.chunk import Chunk
from threading import Thread, Lock
from src.core.scene import Scene
from src.utils import iter_rect
from src.constants import *
import pygame
import json
import os

class ChunkManager:
    def __init__(self, scene: Scene, world_name: str) -> None:
        self.scene = scene
        # The set of chunk positions that have been calculated to be in view
        self.in_view_positions: set[Vec] = set()
        # The set of chunk positions that are in view but have yet to be loaded
        self.pending_positions: set[Vec] = set()
        # The set of chunk objects that have been loaded
        self.loaded_chunks: dict[Vec, Chunk] = {}
        self.queue_clock = pygame.time.Clock()
        self.load_clock = pygame.time.Clock()
        self.prev_center = None

        self.world_name = world_name
        self.world_dir = f"user_data/saves/{self.world_name}"
        self.regions_dir = f"{self.world_dir}/regions"
        # Create the regions directory (and parents) if it doesn't exist yet
        if not os.path.exists(self.regions_dir):
            os.makedirs(self.regions_dir)
        # Data that will be saved directly to disk
        self.region_data: dict[Vec, dict] = {}
        # Lock to prevent chunk loading and saving from conflicting
        self.region_data_lock = Lock()

    def start(self) -> None:
        Thread(target=self.queue_chunks, daemon=True).start()
        Thread(target=self.load_chunks, daemon=True).start()
        Thread(target=self.autosave_regions, daemon=True).start()

    def queue_chunks(self) -> None:
        while True:
            # Perform the check at most CHUNK_CHECK_MAX_FREQ times per second
            self.queue_clock.tick(CHUNK_CHECK_MAX_FREQ)

            new_center = self.scene.camera.pos // BLOCKCHUNK
            # If the camera hasn't moved into a new chunk, don't do anything
            if new_center == self.prev_center: continue

            self.prev_center = new_center
            # Calcuate the new chunk positions that are in view
            new_positions = self.get_new_chunk_positions()

            # Unload chunks that are no longer in view
            for chunk in self.in_view_positions - new_positions:
                self.in_view_positions.remove(chunk)
                if chunk in self.pending_positions:
                    self.pending_positions.remove(chunk)
                if chunk in self.loaded_chunks:
                    self.loaded_chunks.pop(chunk).unload()

            # Load chunks that are now in view
            for chunk in new_positions - self.in_view_positions:
                self.in_view_positions.add(chunk)
                self.pending_positions.add(chunk)

    def load_chunks(self) -> None:
        while True:
            # Load at most CHUNK_LOAD_MAX_FREQ times per second
            self.load_clock.tick(CHUNK_LOAD_MAX_FREQ)

            if not self.pending_positions: continue
            chunk_pos = self.pending_positions.pop()
            chunk = Chunk(self.scene, chunk_pos)
            self.loaded_chunks[chunk_pos] = chunk

    def autosave_regions(self) -> None:
        while True:
            # Save at most once every AUTOSAVE_INTERVAL seconds
            pygame.time.wait(AUTOSAVE_INTERVAL * 1000)

            self.save_regions()

            self.region_data.clear()

    def save_regions(self) -> None:
        with self.region_data_lock:
            for region, data in self.region_data.items():
                file = open(f"{self.regions_dir}/{region.iconcise}.json", "w")
                json.dump(data, file, indent=2)
                file.close()

        print(f"Saved {len(self.region_data)} regions")

    def get_new_chunk_positions(self) -> None:
        center = (self.scene.camera.pos + SIZE // 2) // BLOCKCHUNK
        left = center.x - WIDTH // BLOCKCHUNK // 2 - 2
        right = center.x + WIDTH // BLOCKCHUNK // 2 + 2
        top = center.y - HEIGHT // BLOCKCHUNK // 2 - 2
        bottom = center.y + HEIGHT // BLOCKCHUNK // 2 + 2
        return {pos for pos in iter_rect(left, right, top, bottom)}

    def quit(self) -> None:
        self.save_regions()
