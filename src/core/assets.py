from src.constants import *
import pygame

class Assets:
    def __init__(self) -> None:
        self.block_names = [
            "grass_block",
            "dirt",
        ]

        self.blocks = {name: self.block_img(name) for name in self.block_names}

    def block_img(self, name: str) -> pygame.Surface:
        image = pygame.image.load(f"res/assets/images/{name}.png")
        return pygame.transform.scale(image, BLOCKXY)
