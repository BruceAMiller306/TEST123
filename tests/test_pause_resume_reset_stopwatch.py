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


class PauseResumeResetStopwatchTest(unittest.TestCase):
    def test_pause_and_resume_stopwatch(self) -> None:
        # Given a running stopwatch
        clock = MockClock(0.0)
        app = StopwatchApp(time_provider=clock.time)
        app.click_start()
        clock.advance(3.0)
        app.update_display()
        self.assertEqual(app.display_text, "00:03.0")

        # When I click Pause
        app.click_pause()

        # Then the timer status is paused
        self.assertEqual(app.status, TimerStatus.PAUSED)
        self.assertEqual(str(app.status), "paused")

        # And the display stops advancing
        clock.advance(5.0)
        app.update_display()
        self.assertEqual(app.display_text, "00:03.0")

        # Given a paused stopwatch
        # When I click Resume
        app.click_resume()

        # Then the timer status is running
        self.assertEqual(app.status, TimerStatus.RUNNING)
        self.assertEqual(str(app.status), "running")

        # And the display continues advancing from the paused time
        clock.advance(2.0)
        app.update_display()
        self.assertEqual(app.display_text, "00:05.0")

    def test_reset_stopwatch_from_running_or_paused(self) -> None:
        # Given a running stopwatch
        clock = MockClock(0.0)
        app = StopwatchApp(time_provider=clock.time)
        app.click_start()
        clock.advance(4.0)

        # When I click Reset
        app.click_reset()

        # Then the timer status is ready
        self.assertEqual(app.status, TimerStatus.READY)
        self.assertEqual(str(app.status), "ready")
        # And the display resets to "00:00.0"
        self.assertEqual(app.display_text, "00:00.0")

        # Given a paused stopwatch
        app.click_start()
        clock.advance(4.0)
        app.click_pause()

        # When I click Reset
        app.click_reset()

        # Then the timer status is ready
        self.assertEqual(app.status, TimerStatus.READY)
        # And the display resets to "00:00.0"
        self.assertEqual(app.display_text, "00:00.0")


if __name__ == "__main__":
    unittest.main()
