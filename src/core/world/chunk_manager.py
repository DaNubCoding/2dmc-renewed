from src.core.world.chunk import Chunk
from src.core.scene import Scene
from src.utils import iter_rect
from threading import Thread
from src.constants import *
import pygame

class ChunkManager:
    def __init__(self, scene: Scene) -> None:
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

    def start(self) -> None:
        Thread(target=self.queue_chunks, daemon=True).start()
        Thread(target=self.load_chunks, daemon=True).start()

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

    def get_new_chunk_positions(self) -> None:
        center = (self.scene.camera.pos + SIZE // 2) // BLOCKCHUNK
        left = center.x - WIDTH // BLOCKCHUNK // 2 - 1
        right = center.x + WIDTH // BLOCKCHUNK // 2 + 1
        top = center.y - HEIGHT // BLOCKCHUNK // 2 - 1
        bottom = center.y + HEIGHT // BLOCKCHUNK // 2 + 1
        return {pos for pos in iter_rect(left, right, top, bottom)}
