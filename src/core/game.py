from src.scenes.main_scene import MainScene
from src.core.scene import Scene
from pygame.locals import QUIT
import pygame


class AbortScene(Exception):
    def __str__(self):
        return "Scene aborted but not caught with a try/except block."


class AbortGame(Exception):
    def __str__(self):
        return "Game aborted but not caught with a try/except block."


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.dt = self.clock.tick(0) * 0.05
        self.scene = MainScene(self)

    def run(self) -> None:
        while True:
            try:
                self.update()
                self.scene.update(self.dt)
            except AbortScene:
                continue
            except AbortGame:
                break

            self.scene.draw(self.screen)
            pygame.display.flip()

            fps = round(self.clock.get_fps())
            pygame.display.set_caption(f"2DMC Renewed | FPS: {fps}")

            self.dt = self.clock.tick(0) * 0.05

        pygame.quit()

    def update(self) -> None:
        self.events = {event.type: event for event in pygame.event.get()}

        if QUIT in self.events:
            raise AbortGame

    def change_scene(self, scene: Scene) -> None:
        self.scene = scene