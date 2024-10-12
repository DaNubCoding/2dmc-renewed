from typing import Self as _Self, Any as _Any, Iterable as _Iterable
from multimethod import multimeta as _multimeta
from pygame.math import Vector2 as _Vector2
from numbers import Number as _Number
from math import floor as _floor
import weakref as _weakref

def ref_proxy(obj: _Any) -> _Any:
    """Create a weak reference proxy to an object if it isn't already one.

    Args:
        obj: The object to create a weak reference proxy to.

    Returns:
        The weak reference proxy.
    """
    if isinstance(obj, _weakref.ProxyTypes):
        return obj
    return _weakref.proxy(obj)

def read_file(path: str) -> str:
    """Opens a file, read the contents of the file, then closes it.

    Args:
        path: The path of the file to read from.

    Returns:
        The full contents of the file.
    """
    with open(path, "r") as file:
        return file.read()

def inttup(tup: tuple[_Number, _Number]) -> tuple:
    """Convert a tuple of 2 _numbers to a tuple of 2 ints.

    Args:
        tup: The tuple to convert.

    Returns:
        The integer tuple.
    """
    return (_floor(tup[0]), _floor(tup[1]))

def iter_rect(left: int, right: int, top: int, bottom: int) -> _Iterable[tuple[int, int]]:
    """Iterate over the coordinates of a rectangle.

    Args:
        left: The leftmost x-coordinate (inclusive).
        right: The rightmost x-coordinate (inclusive).
        top: The topmost y-coordinate (inclusive).
        bottom: The bottommost y-coordinate (inclusive).

    Yields:
        The coordinates of the rectangle.
    """
    for x in range(int(left), int(right) + 1):
        for y in range(int(top), int(bottom) + 1):
            yield Vec(x, y)

def iter_square(size: int) -> _Iterable[tuple[int, int]]:
    """Iterate over the coordinates of a square.

    Args:
        size: The size of the square.

    Yields:
        The coordinates of the square.
    """
    yield from iter_rect(0, size - 1, 0, size - 1)

class Vec(_Vector2, metaclass=_multimeta):
    @property
    def itup(self) -> tuple[int, int]:
        return inttup(self)

    @property
    def ivec(self) -> _Self:
        return Vec(self.itup)

    @property
    def concise(self) -> str:
        return f"{self.x},{self.y}"

    @property
    def iconcise(self) -> str:
        itup = self.itup
        return f"{itup[0]},{itup[1]}"

    @staticmethod
    def from_concise(concise: str) -> _Self:
        x, y = concise.split(",")
        return Vec(float(x), float(y))

    def normalize(self) -> _Self:
        try:
            return super().normalize()
        except ValueError:
            return Vec(0, 0)

    def normalize_ip(self) -> None:
        try:
            return super().normalize_ip()
        except ValueError:
            pass

    def clamp_magnitude(self, max_length: _Number) -> _Self:
        try:
            return super().clamp_magnitude(max_length)
        except ValueError:
            return Vec(0, 0)

    def clamp_magnitude(self, min_length: _Number, max_length: _Number) -> _Self:
        try:
            return super().clamp_magnitude(min_length, max_length)
        except ValueError:
            return Vec(0, 0)

    def clamp_magnitude_ip(self, max_length: _Number) -> None:
        try:
            return super().clamp_magnitude_ip(max_length)
        except ValueError:
            pass

    def clamp_magnitude_ip(self, min_length: _Number, max_length: _Number) -> None:
        try:
            return super().clamp_magnitude_ip(min_length, max_length)
        except ValueError:
            pass

    def __hash__(self) -> int:
        return tuple(self).__hash__()
