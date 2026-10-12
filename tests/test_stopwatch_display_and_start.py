import unittest
from src.stopwatch_app import StopwatchApp
from src.types import TimerStatus


class MockClock:
    def __init__(self, start_time: float = 0.0) -> None:
        self.current_time: float = start_time

    def time(self) -> float:
        return self.current_time

    def advance(self, seconds: float) -> None:
        self.current_time += seconds


class StopwatchDisplayAndStartTest(unittest.TestCase):
    def test_app_opens_with_zero_display_and_ready_status(self) -> None:
        # Given a new stopwatch app
        clock = MockClock(0.0)
        app = StopwatchApp(time_provider=clock.time)

        # When the app opens
        # Then the display shows "00:00.0"
        self.assertEqual(app.display_text, "00:00.0")
        # And the timer status is ready
        self.assertEqual(app.status, TimerStatus.READY)
        self.assertEqual(str(app.status), "ready")

    def test_click_start_starts_timer_and_updates_display(self) -> None:
        # Given a stopwatch in ready state
        clock = MockClock(0.0)
        app = StopwatchApp(time_provider=clock.time)
        self.assertEqual(app.status, TimerStatus.READY)

        # When I click Start
        app.click_start()

        # Then the timer status is running
        self.assertEqual(app.status, TimerStatus.RUNNING)
        self.assertEqual(str(app.status), "running")

        # And the display updates as time elapses
        clock.advance(2.0)
        app.update_display()
        self.assertEqual(app.display_text, "00:02.0")


if __name__ == "__main__":
    unittest.main()
