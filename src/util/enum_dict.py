from __future__ import annotations

from typing import TypeVar, Generic
from multimethod import multimeta
from enum import IntEnum

KT = TypeVar("KT", bound=IntEnum)
VT = TypeVar("VT")

class IntEnumDict(Generic[KT, VT], dict[KT, VT], metaclass=multimeta):
    """A dictionary that only accepts IntEnum keys.

    This dictionary is designed to be used with IntEnums only. It will take
    either the enum member itself, the enum name as a string, or the enum value
    as an integer as the key, and will return the member or value associated
    with that key. This dictionary will raise a KeyError if the key is not a
    member, name, or value of the enum.
    """

    def __init__(self, source: dict[KT, VT]) -> None:
        super().__init__(source)
        self._enum_type = type(next(iter(source)))

    def __setitem__(self, key: KT, value: VT) -> None:
        super().__setitem__(key, value)

    def __setitem__(self, key: str, value: VT) -> None:
        try:
            key = self._enum_type[key]
        except KeyError:
            raise KeyError(f"Key must be one of [{
                ', '.join(self._enum_type.__members__)
            }]")
        super().__setitem__(key, value)

    def __setitem__(self, key: int, value: VT) -> None:
        try:
            key = self._enum_type(key)
        except ValueError:
            raise KeyError(f"Key must be one of [{
                ', '.join(map(str, self._enum_type))
            }]")
        super().__setitem__(key, value)

    def __getitem__(self, key: KT) -> VT:
        return super().__getitem__(key)

    def __getitem__(self, key: str) -> VT:
        try:
            key = self._enum_type[key]
        except KeyError:
            raise KeyError(f"Key must be one of [{
                ', '.join(self._enum_type.__members__)
            }]")
        return super().__getitem__(key)

    def __getitem__(self, key: int) -> VT:
        try:
            key = self._enum_type(key)
        except ValueError:
            raise KeyError(f"Key must be one of [{
                ', '.join(map(str, self._enum_type))
            }]")
        return super().__getitem__(key)

    def __delitem__(self, key: KT) -> None:
        super().__delitem__(key)

    def __delitem__(self, key: str) -> None:
        try:
            key = self._enum_type[key]
        except KeyError:
            raise KeyError(f"Key must be one of [{
                ', '.join(self._enum_type.__members__)
            }]")
        super().__delitem__(key)

    def __delitem__(self, key: int) -> None:
        try:
            key = self._enum_type(key)
        except ValueError:
            raise KeyError(f"Key must be one of [{
                ', '.join(map(str, self._enum_type))
            }]")
        super().__delitem__(key)

    def __contains__(self, key: KT) -> bool:
        return super().__contains__(key)

    def __contains__(self, key: str) -> bool:
        try:
            key = self._enum_type[key]
        except KeyError:
            return False
        return super().__contains__(key)

    def __contains__(self, key: int) -> bool:
        try:
            key = self._enum_type(key)
        except ValueError:
            return False
        return super().__contains__(key)

    def get(self, key: KT, default: VT = None) -> VT:
        return super().get(key, default)

    def get(self, key: str, default: VT = None) -> VT:
        try:
            key = self._enum_type[key]
        except KeyError:
            return default
        return super().get(key, default)

    def get(self, key: int, default: VT = None) -> VT:
        try:
            key = self._enum_type(key)
        except ValueError:
            return default
        return super().get(key, default)

    def pop(self, key: KT, default: VT = None) -> VT:
        return super().pop(key, default)

    def pop(self, key: str, default: VT = None) -> VT:
        try:
            key = self._enum_type[key]
        except KeyError:
            return default
        return super().pop(key, default)

    def pop(self, key: int, default: VT = None) -> VT:
        try:
            key = self._enum_type(key)
        except ValueError:
            return default
        return super().pop(key, default)

    def setdefault(self, key: KT, default: VT = None) -> VT:
        return super().setdefault(key, default)

    def setdefault(self, key: str, default: VT = None) -> VT:
        try:
            key = self._enum_type[key]
        except KeyError:
            return default
        return super().setdefault(key, default)

    def setdefault(self, key: int, default: VT = None) -> VT:
        try:
            key = self._enum_type(key)
        except ValueError:
            return default
        return super().setdefault(key, default)
