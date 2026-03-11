from collections import deque
from datetime import datetime
from typing import Any


class MemoryStore:
    """In-memory episodic memory for decisions and outcomes."""

    def __init__(self, max_events: int = 200):
        self._events: deque[dict[str, Any]] = deque(maxlen=max_events)

    def add_event(self, event_type: str, payload: dict[str, Any]) -> None:
        self._events.append(
            {
                "time": datetime.utcnow().isoformat() + "Z",
                "type": event_type,
                "payload": payload,
            }
        )

    def recent(self, limit: int = 20) -> list[dict[str, Any]]:
        if limit <= 0:
            return []
        return list(self._events)[-limit:]

    def recent_failures(self, limit: int = 20) -> int:
        events = self.recent(limit)
        return sum(1 for e in events if e.get("type") == "feedback" and not e.get("payload", {}).get("success", True))
