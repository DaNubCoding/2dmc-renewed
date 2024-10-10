from src.scenes.main_game import MainScene
from src.core.assets import Assets
from src.core.scene import Scene
from pygame.locals import QUIT
from src.constants import *
import pygame

class AbortScene(Exception):
    def __str__(self):
        return "Scene aborted but not caught with a try/except block."

class AbortGame(Exception):
    def __str__(self):
        return "Game aborted but not caught with a try/except block."

class Game:
    def __init__(self) -> None:
        # NOTE: temporary world name input
        world_name = input("World Name: ")

        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(0) / 1000

        self.assets = Assets()
        self.scene = MainScene(self, world_name)

    def run(self) -> None:
        while True:
            try:
                self.update()
                self.scene.update(self.dt)
            except AbortScene:
                continue
            except AbortGame:
                self.scene.quit()
                break

            self.scene.draw(self.screen)
            pygame.display.flip()

            fps = round(self.clock.get_fps())
            pygame.display.set_caption(f"2DMC Renewed | FPS: {fps}")

            self.dt = self.clock.tick(0) / 1000

        pygame.quit()

    def update(self) -> None:
        self.events = {event.type: event for event in pygame.event.get()}

        if QUIT in self.events:
            raise AbortGame

    def change_scene(self, scene: Scene) -> None:
        self.scene = scene
