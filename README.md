# Hi Ho! Cherry-O
I don't want anyone to get the wrong idea about this project. I hate Hi Ho! Cherry-O. It is a terrible game. In fact, it isn't even a game. One criteria for a game is that players make decisions. Ideally, those decisions will be meaningful and interesting. Now, many children's games DO have meaningful and interesting decisions. But Hi Ho! Cherry-O is not among them. It even has a terrible name.

Anyway...
The same things that make it a terrible game make it a good candidate for analysis. The first file here is a simulation of the "game". The only decision the user gets to make is how many players to play with (the right answer is 0). Then the game runs on autopilot

The next step is to run a Monte Carlo simulation to get some statistics about possible games. Since the number of turns is unbounded (you could literally play this game forever), I'm curious about how the game typically plays out. How many turns does it take on average? What do the outliers look like? How is this affected by player count? etc. Then I want to compare this to the theoretical probabilities using a Markov chain. More to come on this.
