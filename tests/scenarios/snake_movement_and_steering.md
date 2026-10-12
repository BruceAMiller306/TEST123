# Snake movement and steering

Given a new game on a 20x20 board with a snake facing Right
When the game advances 1 tick
Then the snake's head advances by 1 cell to the right
And the snake length remains unchanged

Given a snake moving Right
When the player attempts to steer Left
Then the heading remains Right (180-degree reversal is ignored)
