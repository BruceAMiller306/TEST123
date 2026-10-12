# Snake collisions and game over

Given a snake head at the right boundary (19, 10) moving Right
When the game advances 1 tick
Then the snake collides with the wall
And the game status is Game Over

Given a snake curled such that moving Down hits its own body
When the game advances 1 tick
Then the snake collides with itself
And the game status is Game Over
