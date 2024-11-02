from src.core.sprite import Sprite
from src.core.scene import Scene
from src.constants import *
from src.util import *
import pygame

class Crosshair(Sprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layer.CROSSHAIR)
        self.pos = Vec(0, 0)
        pygame.mouse.set_visible(False)

    def update(self, dt: float) -> None:
        self.screen_pos = Vec(pygame.mouse.get_pos())
        self.pos = self.screen_pos + self.scene.camera.pos
        self.block_pos = self.pos // BLOCK
        self.chunk_pos = self.block_pos // CHUNK

    def draw(self, screen: pygame.Surface) -> None:
        # Find the topleft position of the horizontal line of the crosshair
        hor_pos = self.screen_pos - Vec(CROSSHAIR_L // 2, CROSSHAIR_W // 2)
        hor_size = Vec(
            # Ensure the line doesn't go off the screen by clamping the size.
            # If the line does not go off the screen, the size is CROSSHAIR_L
            # which will be evaluated to be the minimum. If the line goes off
            # the left of the screen, the size is the distance from the left of
            # the screen to the right of the line, represented by `hor_pos.x +
            # CROSSHAIR_L`. If the line goes off the right of the screen, the
            # size is the distance from the left of the line to the right of
            # the screen, represented by `WIDTH - hor_pos.x`. The same logic
            # applies to the height of the line.
            min(hor_pos.x + CROSSHAIR_L, CROSSHAIR_L, WIDTH - hor_pos.x),
            min(hor_pos.y + CROSSHAIR_W, CROSSHAIR_W, HEIGHT - hor_pos.y)
        )
        # Ensure the topleft position of the line is not off the left or top of
        # the screen.
        hor_pos = Vec(max(0, hor_pos.x), max(0, hor_pos.y))

        # The same logic above applies to the vertical line of the crosshair.
        ver_pos = self.screen_pos - Vec(CROSSHAIR_W // 2, CROSSHAIR_L // 2)
        ver_size = Vec(
            min(ver_pos.x + CROSSHAIR_W, CROSSHAIR_W, WIDTH - ver_pos.x),
            min(ver_pos.y + CROSSHAIR_L, CROSSHAIR_L, HEIGHT - ver_pos.y)
        )
        ver_pos = Vec(max(0, ver_pos.x), max(0, ver_pos.y))

        # Create the images of the horizontal and vertical lines of the
        # crosshair at the calculated positions and invert the colors
        hor_line = screen.subsurface((hor_pos, hor_size))
        inv_hor_line = smart_invert_surface_colors(hor_line)
        ver_line = screen.subsurface((ver_pos, ver_size))
        inv_ver_line = smart_invert_surface_colors(ver_line)

        # Draw the lines at the calculated positions
        screen.blit(inv_hor_line, hor_pos)
        screen.blit(inv_ver_line, ver_pos)
