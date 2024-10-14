from __future__ import annotations
from typing import Callable, Any
import datetime
import cProfile
import pstats
import os

class Profiler:
    activated = False
    selected: list[int] = []
    profilers: list[Profiler] = []
    started = False

    @classmethod
    def toggle(cls) -> None:
        cls.activated = not cls.activated
        if cls.activated:
            print("Profiler activated, please select profilers:")
            for i, profiler in enumerate(Profiler.profilers):
                print(f"{i + 1}) {profiler.name} (Index: {i})")
            print("Press Backspace to clear selection")
            print("Press F9 again to start selected profilers")
        else:
            print("Starting selected profilers: ", Profiler.selected)
            cls.started = True

    @classmethod
    def select(cls, index: int) -> None:
        if index >= len(Profiler.profilers):
            max_index = len(Profiler.profilers) - 1
            print(f"Profiler at index {index} does not exist, "
                  f"max index is {max_index}")
            return

        profiler = Profiler.profilers[index]

        if index in Profiler.selected:
            Profiler.selected.remove(index)
            print(f"Profiler at index {index} deselected: {profiler.name}")
            return

        Profiler.selected.append(index)
        print(f"Profiler at index {index} selected: {profiler.name}")

    @classmethod
    def clear(cls) -> None:
        Profiler.selected = []
        print("All profilers deselected")

    def __init__(self, func: Callable, save: bool = True, print: bool = False) -> None:
        self.func = func
        self.name = func.__name__
        self.save = save
        self.print = print
        self.index = len(Profiler.profilers)

        Profiler.profilers.append(self)

    def __call__(self, *args, **kwargs) -> Any:
        if not Profiler.started or self.index not in Profiler.selected:
            return self.func(*args, **kwargs)

        with cProfile.Profile() as pr:
            ret = self.func(*args, **kwargs)

        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        if self.print:
            stats.print_stats()

        if self.save:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            path = f"debug/profiles/{self.name}_{timestamp}.prof"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            stats.dump_stats(path)
            print(f"Profile saved to {path}")

        Profiler.selected.remove(self.index)
        print(f"Profiler {self.name} at index {self.index} finished")
        if not Profiler.selected:
            Profiler.started = False
            print("All profilers finished")

        return ret
