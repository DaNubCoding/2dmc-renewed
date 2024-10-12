from typing import Self as _Self, Any as _Any, Iterable as _Iterable
from multimethod import multimeta as _multimeta
from pygame.math import Vector2 as _Vector2
from numbers import Number as _Number
from pathlib import Path as _Path
from math import floor as _floor
import weakref as _weakref
import sys as _sys
import os as _os

_BUNDLE_DIR = getattr(
    _sys, '_MEIPASS',
    _Path(_os.path.abspath(_os.path.dirname(__file__))).parent
)
def pathof(file: str) -> str:
    """Gets the path to the given file that will work with exes.
    Args:
        file (str): The original path to go to
    Returns:
        str: The bundled - exe compatible file path
    """

    abspath = _os.path.abspath(_os.path.join(_BUNDLE_DIR, file))
    if not _os.path.exists(abspath):
        abspath = file
    return abspath

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
    """Convert a tuple of 2 numbers to a tuple of 2 ints.

    This uses the floor function to convert the numbers to ints.

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
    """A 2D vector class with more utility methods and modified behavior."""

    @property
    def itup(self) -> tuple[int, int]:
        """Return the vector as a tuple of ints.

        This uses the `inttup` function to convert the components to ints.

        Returns:
            The integer tuple.
        """
        return inttup(self)

    @property
    def ivec(self) -> _Self:
        """Return the vector as a vector of ints.

        This uses the `Vec.itup` property to convert the components to ints.

        **Note**: The resulting vector still has float components, but they are
        guaranteed to be whole numbers.

        Returns:
            The integer vector.
        """
        return Vec(self.itup)

    @property
    def concise(self) -> str:
        """Return the vector as a concise string.

        This differs from the default string representation by not including
        the square brackets.

        Example:
            Vec(1, 2) -> "1,2"
            Vec(1.0, 2.0) -> "1.0,2.0"
            Vec(1.5, -2.5) -> "1.5,-2.5"

        Returns:
            The concise string.
        """
        return f"{self.x},{self.y}"

    @property
    def iconcise(self) -> str:
        """Return the vector as a concise string of ints.

        This differs from the `Vec.concise` property by converting the
        components to ints in the process.

        Example:
            Vec(1.0, 2.0) -> "1,2"
            Vec(1.5, -2.5) -> "1,-3"

        Returns:
            The concise string of ints.
        """
        itup = self.itup
        return f"{itup[0]},{itup[1]}"

    @staticmethod
    def from_concise(concise: str) -> _Self:
        """Create a vector from a concise string.

        This is the inverse of the `Vec.concise` property.

        Args:
            concise: The concise string to create the vector from.

        Exceptions:
            ValueError: If the concise string is invalid.

        Returns:
            The vector.
        """
        try:
            x, y = concise.split(",")
        except ValueError:
            raise ValueError(f"Invalid concise string: {concise}")
        return Vec(float(x), float(y))

    def normalize(self) -> _Self:
        """Return a normalized vector.

        This differs from the default `normalize` method by returning a zero
        vector if the vector is a zero vector.

        Returns:
            The normalized vector.
        """
        try:
            return super().normalize()
        except ValueError:
            return Vec(0, 0)

    def normalize_ip(self) -> None:
        """Normalize the vector in place.

        This differs from the default `normalize_ip` method by setting the
        vector to a zero vector if it is a zero vector.
        """
        try:
            return super().normalize_ip()
        except ValueError:
            pass

    def clamp_magnitude(self, max_length: _Number) -> _Self:
        """Return a vector with a magnitude clamped to a maximum length.

        This differs from the default `clamp_magnitude` method by returning a
        zero vector if the vector is a zero vector.

        Args:
            max_length: The maximum length of the vector.

        Returns:
            The clamped vector.
        """
        try:
            return super().clamp_magnitude(max_length)
        except ValueError:
            return Vec(0, 0)

    def clamp_magnitude(self, min_length: _Number, max_length: _Number) -> _Self:
        """Return a vector with a magnitude clamped to a range.

        This differs from the default `clamp_magnitude` method by returning a
        zero vector if the vector is a zero vector.

        Args:
            min_length: The minimum length of the vector.
            max_length: The maximum length of the vector.

        Returns:
            The clamped vector.
        """
        try:
            return super().clamp_magnitude(min_length, max_length)
        except ValueError:
            return Vec(0, 0)

    def clamp_magnitude_ip(self, max_length: _Number) -> None:
        """Clamp the magnitude of the vector to a maximum length in place.

        This differs from the default `clamp_magnitude_ip` method by not
        modifying the vector if it is a zero vector.

        Args:
            max_length: The maximum length of the vector.
        """
        try:
            return super().clamp_magnitude_ip(max_length)
        except ValueError:
            pass

    def clamp_magnitude_ip(self, min_length: _Number, max_length: _Number) -> None:
        """Clamp the magnitude of the vector to a range in place.

        This differs from the default `clamp_magnitude_ip` method by not
        modifying the vector if it is a zero vector.

        Args:
            min_length: The minimum length of the vector.
            max_length: The maximum length of the vector.
        """
        try:
            return super().clamp_magnitude_ip(min_length, max_length)
        except ValueError:
            pass

    def __hash__(self) -> int:
        """Return the hash of the vector."""
        return tuple(self).__hash__()
