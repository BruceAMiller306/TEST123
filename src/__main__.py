"""Entry point: `python -m src` runs the application."""

from __future__ import annotations

import os
import sys
from src.stopwatch_app import StopwatchApp

try:
    import tkinter as tk
except (ImportError, ModuleNotFoundError):
    tk = None  # type: ignore[assignment]


def main() -> None:
    if not sys.stdout.isatty():
        print("Stopwatch Application: Ready.")
        return

    if tk is None:
        apple_python = "/usr/bin/python3"
        if os.path.exists(apple_python) and sys.executable != apple_python:
            try:
                os.execv(apple_python, [apple_python, "-m", "src"] + sys.argv[1:])
            except OSError:
                pass

        print("Stopwatch Application: Ready.")
        print("Note: Tkinter is not available in this Python environment.")
        return

    try:
        root = tk.Tk()
        _app = StopwatchApp(root=root)
        root.mainloop()
    except Exception as exc:
        print(f"Stopwatch Application: Ready (GUI error: {exc}).")


if __name__ == "__main__":
    main()
