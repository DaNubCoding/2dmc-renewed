from typing import Generic, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")

class DeferredDict(Generic[KT, VT], dict[KT, VT]):
    """A dictionary that defers the addition and removal of items until
    `commit` is called. This is useful for when items are added or removed
    during iteration.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._deferred_add: dict[KT, VT] = {}
        self._deferred_remove: set[KT] = set()

    def __setitem__(self, key: KT, value: VT) -> None:
        if key in self._deferred_remove:
            self._deferred_remove.remove(key)
        else:
            self._deferred_add[key] = value

    def __delitem__(self, key: KT) -> None:
        if key in self._deferred_add:
            del self._deferred_add[key]
        else:
            self._deferred_remove.add(key)

    def __contains__(self, key: KT) -> bool:
        return (key in self._deferred_add or super().__contains__(key)) \
            and key not in self._deferred_remove

    def __getitem__(self, key: KT) -> VT:
        if key in self._deferred_add:
            return self._deferred_add[key]
        return super().__getitem__(key)

    def get(self, key: KT, default: VT = None) -> VT:
        if key in self._deferred_add:
            return self._deferred_add[key]
        if key in self._deferred_remove:
            return default
        return super().get(key, default)

    def pop(self, key: KT, default: VT = None) -> VT:
        if key in self._deferred_add:
            return self._deferred_add.pop(key)
        if key in self:
            self._deferred_remove.add(key)
            return self[key]
        return default

    def clear(self) -> None:
        super().clear()
        self._deferred_add.clear()
        self._deferred_remove.clear()

    def commit(self) -> None:
        """Commit all deferred changes."""
        for key, value in self._deferred_add.items():
            super().__setitem__(key, value)
        self._deferred_add.clear()

        for key in self._deferred_remove:
            super().__delitem__(key)
        self._deferred_remove.clear()

__all__ = ["DeferredDict"]
