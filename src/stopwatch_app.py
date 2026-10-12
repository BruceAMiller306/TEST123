from __future__ import annotations

import time
from typing import Any, Callable
from src.stopwatch import Stopwatch
from src.types import TimerStatus

try:
    import tkinter as tk
except (ImportError, ModuleNotFoundError):
    tk = None  # type: ignore[assignment]


class StopwatchApp:
    def __init__(
        self,
        root: Any | None = None,
        time_provider: Callable[[], float] = time.monotonic,
    ) -> None:
        self._stopwatch: Stopwatch = Stopwatch(time_provider=time_provider)
        self._root: Any | None = root
        self._display_text: str = self._stopwatch.display_time

        self._display_label: Any | None = None
        self._status_label: Any | None = None
        self._start_button: Any | None = None
        self._pause_button: Any | None = None
        self._resume_button: Any | None = None
        self._reset_button: Any | None = None

        if self._root is not None and tk is not None:
            self._build_widgets()

    @property
    def display_text(self) -> str:
        self._display_text = self._stopwatch.display_time
        return self._display_text

    @property
    def status(self) -> TimerStatus:
        return self._stopwatch.status

    def click_start(self) -> None:
        self._stopwatch.start()
        self.update_display()

    def click_pause(self) -> None:
        self._stopwatch.pause()
        self.update_display()

    def click_resume(self) -> None:
        self._stopwatch.resume()
        self.update_display()

    def click_reset(self) -> None:
        self._stopwatch.reset()
        self.update_display()

    def update_display(self) -> None:
        self._display_text = self._stopwatch.display_time
        if self._display_label is not None:
            self._display_label.config(text=self._display_text)
        if self._status_label is not None:
            self._status_label.config(text=self.status.value.upper())
        self._update_button_states()

    def _tick(self) -> None:
        if self.status == TimerStatus.RUNNING:
            self.update_display()
            if self._root is not None:
                self._root.after(50, self._tick)

    def _update_button_states(self) -> None:
        if tk is None or self._start_button is None:
            return

        state_ready = self.status == TimerStatus.READY
        state_running = self.status == TimerStatus.RUNNING
        state_paused = self.status == TimerStatus.PAUSED

        self._start_button.config(
            state=tk.NORMAL if state_ready else tk.DISABLED
        )
        self._pause_button.config(
            state=tk.NORMAL if state_running else tk.DISABLED
        )
        self._resume_button.config(
            state=tk.NORMAL if state_paused else tk.DISABLED
        )
        self._reset_button.config(
            state=tk.NORMAL if not state_ready else tk.DISABLED
        )

    def _build_widgets(self) -> None:
        assert tk is not None
        assert self._root is not None

        self._root.title("Stopwatch")
        self._root.geometry("380x240")
        self._root.resizable(False, False)

        main_frame = tk.Frame(self._root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        self._status_label = tk.Label(
            main_frame,
            text=self.status.value.upper(),
            font=("Helvetica", 14, "bold"),
            fg="#666666",
        )
        self._status_label.pack(pady=(0, 10))

        self._display_label = tk.Label(
            main_frame,
            text=self._display_text,
            font=("Courier", 48, "bold"),
            fg="#222222",
        )
        self._display_label.pack(pady=(0, 20))

        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack()

        self._start_button = tk.Button(
            buttons_frame,
            text="Start",
            width=8,
            command=self._on_start_clicked,
        )
        self._start_button.grid(row=0, column=0, padx=5)

        self._pause_button = tk.Button(
            buttons_frame,
            text="Pause",
            width=8,
            command=self._on_pause_clicked,
        )
        self._pause_button.grid(row=0, column=1, padx=5)

        self._resume_button = tk.Button(
            buttons_frame,
            text="Resume",
            width=8,
            command=self._on_resume_clicked,
        )
        self._resume_button.grid(row=0, column=2, padx=5)

        self._reset_button = tk.Button(
            buttons_frame,
            text="Reset",
            width=8,
            command=self._on_reset_clicked,
        )
        self._reset_button.grid(row=0, column=3, padx=5)

        self._update_button_states()

    def _on_start_clicked(self) -> None:
        self.click_start()
        if self._root is not None:
            self._root.after(50, self._tick)

    def _on_pause_clicked(self) -> None:
        self.click_pause()

    def _on_resume_clicked(self) -> None:
        self.click_resume()
        if self._root is not None:
            self._root.after(50, self._tick)

    def _on_reset_clicked(self) -> None:
        self.click_reset()
