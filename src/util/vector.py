import src.util.general as general
from multimethod import multimeta
from pygame.math import Vector2
from numbers import Number
from typing import Self

class Vec(Vector2, metaclass=multimeta):
    """A 2D vector class with more utility methods and modified behavior."""

    @property
    def itup(self) -> tuple[int, int]:
        """Return the vector as a tuple of ints.

        This uses the `inttup` function to convert the components to ints.

        Returns:
            The integer tuple.
        """
        return general.inttup(self)

    @property
    def ivec(self) -> Self:
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
    def from_concise(concise: str) -> Self:
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

    def normalize(self) -> Self:
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

    def clamp_magnitude(self, max_length: Number) -> Self:
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

    def clamp_magnitude(self, min_length: Number, max_length: Number) -> Self:
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

    def clamp_magnitude_ip(self, max_length: Number) -> None:
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

    def clamp_magnitude_ip(self, min_length: Number, max_length: Number) -> None:
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