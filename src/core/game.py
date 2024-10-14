from src.scenes.main_game import MainScene
from src.util.profiler import Profiler
from src.core.assets import Assets
from src.core.scene import Scene
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
        pygame.display.set_caption("2DMC Renewed")
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(0) / 1000

        self.assets = Assets()
        self.scene = MainScene(self, world_name)

        self.update_profiler = Profiler(self.scene.update)
        self.draw_profiler = Profiler(self.scene.draw)

    def run(self) -> None:
        while True:
            try:
                self.update()
                # self.scene.update(self.dt)
                self.update_profiler(self.dt)
            except AbortScene:
                continue
            except AbortGame:
                self.scene.quit()
                break

            # self.scene.draw(self.screen)
            self.draw_profiler(self.screen)
            pygame.display.flip()

            self.dt = self.clock.tick(0) / 1000

        pygame.quit()

    def update(self) -> None:
        self.events = {event.type: event for event in pygame.event.get()}

        if pygame.QUIT in self.events:
            raise AbortGame

        elif pygame.KEYDOWN in self.events:
            key: int = self.events[pygame.KEYDOWN].key
            if key == pygame.K_F9:
                Profiler.toggle()
            elif pygame.K_1 <= key <= pygame.K_9 and Profiler.activated:
                Profiler.select(key - pygame.K_0 - 1)
            elif key == pygame.K_0 and Profiler.activated:
                Profiler.clear()

    def change_scene(self, scene: Scene) -> None:
        self.scene = scene
