from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """Abstract base class for all agents in the robolog platform."""

    def __init__(self, state: Dict[str, Any]):
        self.state = state

    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """Execute the agent's duties and return updated state."""
        pass

    def log(self, message: str) -> None:
        print(f"[{self.__class__.__name__}] {message}")
