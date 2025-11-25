"""History manager for undo/redo functionality."""

from typing import Optional
from turing_machine import MachineState


class HistoryManager:
    """Manages undo/redo history for the Turing machine."""

    def __init__(self, max_history: int = 1000):
        self.history: list[MachineState] = []
        self.redo_stack: list[MachineState] = []
        self.max_history = max_history

    def push(self, state: MachineState) -> None:
        """Save a state to history."""
        self.history.append(state)
        self.redo_stack.clear()

        if len(self.history) > self.max_history:
            self.history.pop(0)

    def undo(self) -> Optional[MachineState]:
        """Undo to previous state. Returns the state to restore, or None."""
        if len(self.history) < 2:
            return None

        current = self.history.pop()
        self.redo_stack.append(current)

        return self.history[-1] if self.history else None

    def redo(self) -> Optional[MachineState]:
        """Redo to next state. Returns the state to restore, or None."""
        if not self.redo_stack:
            return None

        state = self.redo_stack.pop()
        self.history.append(state)
        return state

    def clear(self) -> None:
        """Clear all history."""
        self.history.clear()
        self.redo_stack.clear()

    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return len(self.history) >= 2

    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return len(self.redo_stack) > 0

    def get_history_length(self) -> int:
        """Get the number of states in history."""
        return len(self.history)
