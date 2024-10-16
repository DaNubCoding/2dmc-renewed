from typing import TypeVar, Generic, Any
from multimethod import multimeta
from enum import Enum

T = TypeVar("T", bound=Enum)

class IntEnumDict(Generic[T], dict, metaclass=multimeta):
    def __init__(self, enum_type: T) -> None:
        if not all(isinstance(member.value, int) for member in enum_type):
            raise ValueError("IntEnumDict only accepts enums with int values")

        self.enum_type = enum_type
        super().__init__()

    def __setitem__(self, key: T, value: Any) -> None:
        super().__setitem__(key, value)

    def __setitem__(self, key: str, value: Any) -> None:
        try:
            key = self.enum_type[key]
        except KeyError:
            raise KeyError(f"Key must be one of [{
                ', '.join(self.enum_type.__members__)
            }]")
        super().__setitem__(key, value)

    def __setitem__(self, key: int, value: Any) -> None:
        try:
            key = self.enum_type(key)
        except ValueError:
            raise ValueError(f"Key must be one of [{
                ', '.join(map(str, self.enum_type))
            }]")
        super().__setitem__(key, value)

    def __getitem__(self, key: T) -> Any:
        return super().__getitem__(key)

    def __getitem__(self, key: str) -> Any:
        try:
            key = self.enum_type[key]
        except KeyError:
            raise KeyError(f"Key must be one of [{
                ', '.join(self.enum_type.__members__)
            }]")
        return super().__getitem__(key)

    def __getitem__(self, key: int) -> Any:
        try:
            key = self.enum_type(key)
        except ValueError:
            raise ValueError(f"Key must be one of [{
                ', '.join(map(str, self.enum_type))
            }]")
        return super().__getitem__(key)

    def __delitem__(self, key: T) -> None:
        super().__delitem__(key)

    def __delitem__(self, key: str) -> None:
        try:
            key = self.enum_type[key]
        except KeyError:
            raise KeyError(f"Key must be one of [{
                ', '.join(self.enum_type.__members__)
            }]")
        super().__delitem__(key)

    def __delitem__(self, key: int) -> None:
        try:
            key = self.enum_type(key)
        except ValueError:
            raise ValueError(f"Key must be one of [{
                ', '.join(map(str, self.enum_type))
            }]")
        super().__delitem__(key)

    def __contains__(self, key: T) -> bool:
        return super().__contains__(key)

    def __contains__(self, key: str) -> bool:
        try:
            key = self.enum_type[key]
        except KeyError:
            return False
        return super().__contains__(key)

    def __contains__(self, key: int) -> bool:
        try:
            key = self.enum_type(key)
        except ValueError:
            return False
        return super().__contains__(key)

    def get(self, key: T, default: Any = None) -> Any:
        return super().get(key, default)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            key = self.enum_type[key]
        except KeyError:
            return default
        return super().get(key, default)

    def get(self, key: int, default: Any = None) -> Any:
        try:
            key = self.enum_type(key)
        except ValueError:
            return default
        return super().get(key, default)

    def pop(self, key: T, default: Any = None) -> Any:
        return super().pop(key, default)

    def pop(self, key: str, default: Any = None) -> Any:
        try:
            key = self.enum_type[key]
        except KeyError:
            return default
        return super().pop(key, default)

    def pop(self, key: int, default: Any = None) -> Any:
        try:
            key = self.enum_type(key)
        except ValueError:
            return default
        return super().pop(key, default)

    def setdefault(self, key: T, default: Any = None) -> Any:
        return super().setdefault(key, default)

    def setdefault(self, key: str, default: Any = None) -> Any:
        try:
            key = self.enum_type[key]
        except KeyError:
            return default
        return super().setdefault(key, default)

    def setdefault(self, key: int, default: Any = None) -> Any:
        try:
            key = self.enum_type(key)
        except ValueError:
            return default
        return super().setdefault(key, default)

    def update(self, other: dict[T, Any]) -> None:
        super().update(other)

    def update(self, other: dict[str, Any]) -> None:
        other = {
            self.enum_type[key]: value
            for key, value in other.items()
        }
        super().update(other)

    def update(self, other: dict[int, Any]) -> None:
        other = {
            self.enum_type(key): value
            for key, value in other.items()
        }
        super().update(other)
