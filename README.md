# Hi Ho! Cherry-O
I don't want anyone to get the wrong idea about this project. I hate Hi Ho! Cherry-O. It is a terrible game. In fact, it isn't even a game. One criteria for a game is that players make decisions. Ideally, those decisions will be meaningful and interesting. Now, many children's games DO have meaningful and interesting decisions. But Hi Ho! Cherry-O is not among them. It even has a terrible name. However, Hi Ho! Cherry-O is a game I have played many times with my kids. 

The 'game', such as it is, has players trying to remove cherries from their tree. Each player starts with 10 cherries in their tree. Players take turns spinning a spinner and the result tells the player how many cherries to remove from their tree to their basket. However, the spinner results could also have players returning two cherries to their trees or possibly even spilling their basket and putting all of their cherries back. The game ends when someone successfully empties their tree. The player that does so wins immediately.

Ironically, the same things that make it a terrible game make it a good candidate for analysis. The first thing I did was make a simulation of the "game". The only decision the user gets to make is how many players to play with (the right answer is 0). Then the game runs on autopilot.

One result of these rules is that a game could possibly last forever. Every turn, players have a 1 in 7 chance of starting the game over. With no way to end a game besides emptying a tree, games can drag on and on and results in some very **LONG** games. I have definitely played games of this with my kids that reflected this. They at least *felt* like they took forever. 

So I thought I would explore the game in more detail. I wanted to know a few things about the game:
First, since the game ends as soon as someone empties their basket, how much of an advantage does the person going first each round have?
Next, I wanted more information about how long a game should last. 
Then finally, I want to look at those long games. How likely are they? How many games would you have to play before you could expect to play an extremely long game, say 100 or 200 turns?

With those questions in mind, let's start with the theoretical probability. I did this below using a Markov chain.

# Theoretical Probabilities

![theoretical probabilities](https://github.com/amitschelen/hi_ho_cherry_o/blob/main/01%20theoretical%20probabilities.png)

One immediate takeaway of the graph above is that games will likely end much quicker as soon as you add a second player. *(Why in the world would anyone ever play this game alone?)* Then for each player you add after that, the probability of the game ending in earlier rounds increases. This makes sense to me, since each player you add increases the number of people that can trigger the end of the game. 

The next step is to model the game with a Monte Carlo simulation to gather some data for analysis to see how the theoretical probabilities compare to what is seen in practice. In this simulation, the game is played a certain number of times (say, 1000) and then those plays are repeated over a few iterations (say, 10). I then use the data from these iterations to look at characteristics of the games played.
# First Player Advantage?
The first question I had was about turn order. How does going first affect your chance of winning? Since the game ends as soon as someone empties their tree, it seems like going first should give you the earliest chance to do that and thus a greater chance of winning. So let's take a look at who wins at each player count.
So, is there a first-player advantage? 
![games won per player](https://github.com/amitschelen/hi_ho_cherry_o/blob/main/02%20games%20won%20per%20player.png)

It seems that the answer is, "Somewhat". The 4th player won fewer of the played games than the other players and earlier players won more often. So, if you want to help your kid win without cheating, let them go first.


Now let's begin the analysis of game length and number of turns
# Graphs and Such
![quantiles](https://github.com/amitschelen/hi_ho_cherry_o/blob/main/03%20quantiles.png)
![hist](https://github.com/amitschelen/hi_ho_cherry_o/blob/main/04%20distribution%20of%20game%20lengths%20hist.png)
![violin](https://github.com/amitschelen/hi_ho_cherry_o/blob/main/05%20distribution%20of%20game%20lengths%20violin.png)
![cumulative percent ended](https://github.com/amitschelen/hi_ho_cherry_o/blob/main/07%20cumulative%20percent%20of%20games%20ended.png)

We can see a few things from the figures above. 

First, the table shows us average is higher than the mean for all player counts. This implies the data is skewed right and thus we have some large outliers pulling the average up. We see that same information conveyed in the histograms and boxplots also.

Next, the scatter plot shows what percent of games ended after each round for each iteration. This looks very close to the theoretical probability calculated initially. So let's take a closer look at how they align.

# Observed and theoretical together for each player count
![cumulative percent ended with curve](https://github.com/amitschelen/hi_ho_cherry_o/blob/main/06%20cumulative%20percent%20of%20games%20ended%20with%20theoretical%20curve.png)

The theoretical probability curves from the Markov chain match the data very well. 

An important (and terrible) characteristic of Hi Ho! Cherry-O is that the game length is unbounded. A game could theoretically last forever. This is just plain BAD game design! So I want to know, just how terrible can the game be? And how likely is it to be that terrible. For instance, how likely am I to play a game lasting over 200 turns? How many games would I have to play to be likely to play a game over 200 turns?

So...Let's look at longest turns of each iteration. Recall that the game is played many times in a row through several iterations. In each trip through the 1000 games, I keep a running list of the longest game played so far. In theory, the more times the game is played, the longer the longest game should be. But those long games are rare events that result in long stretches of no change. That's why I repeat the simulation multiple times. 

Now let's take a look at the those long games.

# Longest Games, Theoretical
![long games calculated](https://github.com/amitschelen/hi_ho_cherry_o/blob/main/08%20theoretical%20predictions.png)

For 1 player, things start out kind of reasonable. You would only need to play more than about 50 games before you can expect to play a game over 50 turns. And you'd play 2500 games before you could expect to play a game over 100 turns. And actually we see that play out in the data above.

But the numbers get very large very quickly. For 4 players, you would need to play more than 42,000,000,000,000 (42 trillion) games before you expect to play a game with more than 100 turns and 5,000,000,000,000,000,000,000,000,000 before you expect to play a game with more than 200 turns. That's a lot.

An importantly observation is that for each player count, doubling the turns we're looking at roughly doubles the order of magnitude. That implies a logarithmic or exponential relationship. Based on the input and output variables here, a logarithmic relationships makes sense.

Let's see how that theoretical probability aligns with our observed maximum turns for each iteration.

# Longest Games, Observed and Predicted
![max turns observed](https://github.com/amitschelen/hi_ho_cherry_o/blob/main/09%20max%20turns%20observed.png)

Then I ran a regression on that data:
![regressions](https://github.com/amitschelen/hi_ho_cherry_o/blob/main/10%20regressions.png)
![observed with regression](https://github.com/amitschelen/hi_ho_cherry_o/blob/main/11%20max%20turns%20observed%20with%20regression.png)
![comparison](https://github.com/amitschelen/hi_ho_cherry_o/blob/main/12%20comparison.png)

The regression matches the theoretical probabilities to a reasonable extent. At lower player counts and turn lengths, the two analyses are off by up to an order of magnitude. At 4 players trying to predict the occurrence of a 200-turn-length game, they are off by a factor of 100. But on the scale of 10^29, that is a very low percent error. These errors mostly highlight the limitations of the theoretical probabilities. They do not take into account the variance of the data. I did not calculate the variance for this analysis, but it is clear from the scatter plot above that it is very high.

# Conclusion
The main thing I take away from this is that those long games are incredibly unlikely. Playing with 2, 3, or 4 players should only take 6-8 turns on average. However, the long games are unpredictable rare events. They can come at any point. You never know when a 2 player game might drag on to 50 or more turns. Both the theoretical probability and regression analysis predict that this should happen once every 1000 games or so. That certainly puts it in the category of 'rare, but not impossible'. On the flip side, a 4 player game stretching to 200 turns probably will never occur. Just taking the lower of the two estimates, I hope for all of humanity's sake that 4.6x10^27 games of Hi Ho! Cherry-O are not played collectively by us. But maybe if we try, we might agree on how terrible this game is, throw all the copies in the trash, and move on to more fun and interesting games.

