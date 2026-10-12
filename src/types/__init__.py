"""Shared types for the whole application. Define each type once, here."""

from enum import Enum


class TimerStatus(str, Enum):
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"

    def __str__(self) -> str:
        return self.value


class TimerStateError(RuntimeError):
    """Raised when an operation is invalid for the current timer state."""
