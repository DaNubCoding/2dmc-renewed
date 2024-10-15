from src.core.render_layer import Layer
from src.core.sprite import Sprite
from src.core.scene import Scene
from src.util import *
import pygame
import time

class DebugMenu(Sprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layer.HUD)
        self.visible = False
        self.font = self.game.assets.fonts[20]
        self.data = {
            "FPS": 0,
            "Selected Position": (0, 0),
            "Selected Chunk": (0, 0),
            "Loaded Chunks": 0,
            "Loaded Regions": 0,
        }
        self.update_timer = LoopTimer(0.05)

    def update(self, dt: float) -> None:
        if not self.visible: return
        if not self.update_timer.done: return

        self.data["FPS"] = int(self.game.clock.get_fps())
        self.data["Selected Position"] = self.scene.crosshair.block_pos.iconcise
        self.data["Selected Chunk"] = self.scene.crosshair.chunk_pos.iconcise
        self.data["Loaded Chunks"] = f"{len(self.scene.chunk_manager.loaded_chunks)}/{len(self.scene.chunk_manager.loaded_chunks) + len(self.scene.chunk_manager.pending_positions)}"
        self.data["Loaded Regions"] = len(self.scene.chunk_manager.region_data)

    def draw(self, screen: pygame.Surface) -> None:
        y = 10
        for key, value in self.data.items():
            text = self.font.render(f"{key}: {value}", True, (255, 255, 255))
            screen.blit(text, (10, y))
            y += text.get_height()

    def toggle(self) -> None:
        self.visible = not self.visible
