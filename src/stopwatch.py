from __future__ import annotations

import time
from typing import Callable
from src.time_formatter import format_stopwatch_time
from src.types import TimerStateError, TimerStatus


class Stopwatch:
    def __init__(
        self, time_provider: Callable[[], float] = time.monotonic
    ) -> None:
        self._time_provider: Callable[[], float] = time_provider
        self._status: TimerStatus = TimerStatus.READY
        self._accumulated_time: float = 0.0
        self._start_timestamp: float | None = None

    @property
    def status(self) -> TimerStatus:
        return self._status

    @property
    def elapsed_time(self) -> float:
        if self._status == TimerStatus.RUNNING:
            assert self._start_timestamp is not None
            current_time = self._time_provider()
            return self._accumulated_time + (current_time - self._start_timestamp)
        if self._status in (TimerStatus.PAUSED, TimerStatus.STOPPED):
            return self._accumulated_time
        return 0.0

    @property
    def display_time(self) -> str:
        return format_stopwatch_time(self.elapsed_time)

    def start(self) -> None:
        if self._status == TimerStatus.RUNNING:
            raise TimerStateError("Timer is already running.")
        if self._status == TimerStatus.STOPPED:
            self._accumulated_time = 0.0
        self._start_timestamp = self._time_provider()
        self._status = TimerStatus.RUNNING

    def pause(self) -> None:
        if self._status != TimerStatus.RUNNING:
            raise TimerStateError(
                f"Cannot pause timer when status is {self._status}."
            )
        assert self._start_timestamp is not None
        self._accumulated_time += self._time_provider() - self._start_timestamp
        self._start_timestamp = None
        self._status = TimerStatus.PAUSED

    def resume(self) -> None:
        if self._status != TimerStatus.PAUSED:
            raise TimerStateError(
                f"Cannot resume timer when status is {self._status}."
            )
        self._start_timestamp = self._time_provider()
        self._status = TimerStatus.RUNNING

    def stop(self) -> None:
        if self._status == TimerStatus.RUNNING:
            assert self._start_timestamp is not None
            self._accumulated_time += self._time_provider() - self._start_timestamp
            self._start_timestamp = None
        self._status = TimerStatus.STOPPED

    def reset(self) -> None:
        self._accumulated_time = 0.0
        self._start_timestamp = None
        self._status = TimerStatus.READY
