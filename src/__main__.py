"""Entry point: `python -m src` runs the application."""

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
