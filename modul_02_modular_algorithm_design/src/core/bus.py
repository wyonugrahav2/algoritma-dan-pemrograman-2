"""
Event Bus (Message Bus) sederhana.

Memfasilitasi komunikasi antar-modul lewat publish/subscribe, sehingga
satu modul tidak perlu mengimpor modul lain secara langsung
(no direct dependency) -- cukup publish event dan modul lain yang
subscribe akan menerimanya.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, DefaultDict, List

Listener = Callable[[Any], None]


class EventBus:
    """Bus event in-memory, synchronous, thread-unsafe (cukup untuk skala modul ini)."""

    def __init__(self) -> None:
        self._listeners: DefaultDict[str, List[Listener]] = defaultdict(list)
        self._history: List[tuple[str, Any]] = []

    def subscribe(self, event_name: str, listener: Listener) -> None:
        self._listeners[event_name].append(listener)

    def unsubscribe(self, event_name: str, listener: Listener) -> None:
        if listener in self._listeners.get(event_name, []):
            self._listeners[event_name].remove(listener)

    def publish(self, event_name: str, payload: Any = None) -> None:
        self._history.append((event_name, payload))
        for listener in self._listeners.get(event_name, []):
            listener(payload)

    def history(self) -> List[tuple[str, Any]]:
        return list(self._history)

    def clear_history(self) -> None:
        self._history.clear()


# Instance global yang dipakai lintas modul.
event_bus = EventBus()
