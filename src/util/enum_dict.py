from __future__ import annotations

from typing import Any, TypeVar, Generic
from multimethod import multimeta
from enum import IntEnum

T = TypeVar("T", bound=IntEnum)
V = TypeVar("V")

class IntEnumDict(Generic[T, V], dict, metaclass=multimeta):
    def __init__(self, source: dict[T, V]) -> None:
        super().__init__(source)
        self.enum = type(next(iter(source)))

    def __setitem__(self, key: T, value: V) -> None:
        super().__setitem__(key, value)

    def __setitem__(self, key: str, value: V) -> None:
        try:
            key = self.enum[key]
        except KeyError:
            raise KeyError(f"Key must be one of [{
                ', '.join(self.enum.__members__)
            }]")
        super().__setitem__(key, value)

    def __setitem__(self, key: int, value: V) -> None:
        try:
            key = self.enum(key)
        except ValueError:
            raise KeyError(f"Key must be one of [{
                ', '.join(map(str, self.enum))
            }]")
        super().__setitem__(key, value)

    def __getitem__(self, key: T) -> V:
        return super().__getitem__(key)

    def __getitem__(self, key: str) -> V:
        try:
            key = self.enum[key]
        except KeyError:
            raise KeyError(f"Key must be one of [{
                ', '.join(self.enum.__members__)
            }]")
        return super().__getitem__(key)

    def __getitem__(self, key: int) -> V:
        try:
            key = self.enum(key)
        except ValueError:
            raise KeyError(f"Key must be one of [{
                ', '.join(map(str, self.enum))
            }]")
        return super().__getitem__(key)

    def __delitem__(self, key: T) -> None:
        super().__delitem__(key)

    def __delitem__(self, key: str) -> None:
        try:
            key = self.enum[key]
        except KeyError:
            raise KeyError(f"Key must be one of [{
                ', '.join(self.enum.__members__)
            }]")
        super().__delitem__(key)

    def __delitem__(self, key: int) -> None:
        try:
            key = self.enum(key)
        except ValueError:
            raise KeyError(f"Key must be one of [{
                ', '.join(map(str, self.enum))
            }]")
        super().__delitem__(key)

    def __contains__(self, key: T) -> bool:
        return super().__contains__(key)

    def __contains__(self, key: str) -> bool:
        try:
            key = self.enum[key]
        except KeyError:
            return False
        return super().__contains__(key)

    def __contains__(self, key: int) -> bool:
        try:
            key = self.enum(key)
        except ValueError:
            return False
        return super().__contains__(key)

    def get(self, key: T, default: V = None) -> V:
        return super().get(key, default)

    def get(self, key: str, default: V = None) -> V:
        try:
            key = self.enum[key]
        except KeyError:
            return default
        return super().get(key, default)

    def get(self, key: int, default: V = None) -> V:
        try:
            key = self.enum(key)
        except ValueError:
            return default
        return super().get(key, default)

    def pop(self, key: T, default: V = None) -> V:
        return super().pop(key, default)

    def pop(self, key: str, default: V = None) -> V:
        try:
            key = self.enum[key]
        except KeyError:
            return default
        return super().pop(key, default)

    def pop(self, key: int, default: V = None) -> V:
        try:
            key = self.enum(key)
        except ValueError:
            return default
        return super().pop(key, default)

    def setdefault(self, key: T, default: V = None) -> V:
        return super().setdefault(key, default)

    def setdefault(self, key: str, default: V = None) -> V:
        try:
            key = self.enum[key]
        except KeyError:
            return default
        return super().setdefault(key, default)

    def setdefault(self, key: int, default: V = None) -> V:
        try:
            key = self.enum(key)
        except ValueError:
            return default
        return super().setdefault(key, default)
