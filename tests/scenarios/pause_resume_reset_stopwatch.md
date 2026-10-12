# Pause, resume, and reset stopwatch

Given a running stopwatch
When I click Pause
Then the timer status is paused
And the display stops advancing

Given a paused stopwatch
When I click Resume
Then the timer status is running
And the display continues advancing from the paused time

Given a running or paused stopwatch
When I click Reset
Then the timer status is ready
And the display resets to "00:00.0"
