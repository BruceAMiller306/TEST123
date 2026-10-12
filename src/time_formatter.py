def format_stopwatch_time(seconds: float) -> str:
    total_seconds = max(0.0, seconds)
    minutes = int(total_seconds) // 60
    remaining_seconds = int(total_seconds) % 60
    tenths = int((total_seconds * 10) % 10)
    return f"{minutes:02d}:{remaining_seconds:02d}.{tenths:d}"
