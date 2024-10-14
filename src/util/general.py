from numbers import Number as Number
from typing import Any, Iterable
from pathlib import Path as Path
import src.util.vector as vector
from math import floor as floor
import weakref as weakref
import sys as sys
import os as os

BUNDLE_DIR = getattr(
    sys, '_MEIPASS',
    Path(os.path.abspath(os.path.dirname(__file__))).parent
)
def pathof(file: str) -> str:
    """Gets the path to the given file that will work with exes.
    Args:
        file (str): The original path to go to
    Returns:
        str: The bundled - exe compatible file path
    """

    abspath = os.path.abspath(os.path.join(BUNDLE_DIR, file))
    if not os.path.exists(abspath):
        abspath = file
    return abspath

def ref_proxy(obj: Any) -> Any:
    """Create a weak reference proxy to an object if it isn't already one.

    Args:
        obj: The object to create a weak reference proxy to.

    Returns:
        The weak reference proxy.
    """
    if isinstance(obj, weakref.ProxyTypes):
        return obj
    return weakref.proxy(obj)

def read_file(path: str) -> str:
    """Opens a file, read the contents of the file, then closes it.

    Args:
        path: The path of the file to read from.

    Returns:
        The full contents of the file.
    """
    with open(path, "r") as file:
        return file.read()

def inttup(tup: tuple[Number, Number]) -> tuple:
    """Convert a tuple of 2 numbers to a tuple of 2 ints.

    This uses the floor function to convert the numbers to ints.

    Args:
        tup: The tuple to convert.

    Returns:
        The integer tuple.
    """
    return (floor(tup[0]), floor(tup[1]))

def iter_rect(left: int, right: int, top: int, bottom: int) -> Iterable[tuple[int, int]]:
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
            yield vector.Vec(x, y)

def iter_square(size: int) -> Iterable[tuple[int, int]]:
    """Iterate over the coordinates of a square.

    Args:
        size: The size of the square.

    Yields:
        The coordinates of the square.
    """
    yield from iter_rect(0, size - 1, 0, size - 1)
