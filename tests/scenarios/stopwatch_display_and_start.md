# Stopwatch display and start

Given a new stopwatch app
When the app opens
Then the display shows "00:00.0"
And the timer status is ready

Given a stopwatch in ready state
When I click Start
Then the timer status is running
And the display updates as time elapses
