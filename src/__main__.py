"""Entry point: `python -m src` runs the application."""

from __future__ import annotations

import os
import sys
import webbrowser
from pathlib import Path
from src.html_game_generator import generate_html_game


def main() -> None:
    html_content = generate_html_game()
    repo_root = Path(__file__).resolve().parent.parent
    html_file = repo_root / "src" / "index.html"
    html_file.write_text(html_content, encoding="utf-8")

    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print(f"Snake Arena: HTML game generated at {html_file}")
        return

    file_uri = html_file.resolve().as_uri()
    print("==========================================")
    print("Snake Arena (4\" x 4\" HTML Game)")
    print(f"Game file ready: {file_uri}")
    print("Opening in your web browser...")
    print("==========================================")
    webbrowser.open(file_uri)


if __name__ == "__main__":
    main()
