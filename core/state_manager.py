from typing import Any, Dict


class ProjectState:
    """Simple state wrapper for the project."""

    def __init__(self, initial: Dict[str, Any] = None):
        self.data: Dict[str, Any] = initial or {}

    def update(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get(self, key: str, default=None):
        return self.data.get(key, default)
