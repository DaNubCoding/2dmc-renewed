from src.constants import *
import pygame
import json

class Assets:
    def __init__(self) -> None:
        with open("res/data/blocks/names.json") as file:
            self.block_names = json.load(file)
        self.blocks = {name: self.block_img(name) for name in self.block_names}

    def block_img(self, name: str) -> pygame.Surface:
        image = pygame.image.load(f"res/assets/images/{name}.png")
        return pygame.transform.scale(image, BLOCKXY)
