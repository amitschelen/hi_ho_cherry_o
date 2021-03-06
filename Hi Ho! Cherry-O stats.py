import numpy as np
from numpy.linalg import matrix_power
import scipy as sc
from scipy.optimize import curve_fit
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#col = to, row = from. 10 -> 0. So prob from 8 to 10 = 3/7
trans_mat = [[3/7, 1/7, 1/7, 1/7, 1/7, 0, 0, 0, 0, 0, 0],
             [3/7, 0, 1/7, 1/7, 1/7, 1/7, 0, 0, 0, 0, 0],
             [3/7, 0, 0, 1/7, 1/7, 1/7, 1/7, 0, 0, 0, 0],
             [1/7, 2/7, 0, 0, 1/7, 1/7, 1/7, 1/7, 0, 0, 0],
             [1/7, 0, 2/7, 0, 0, 1/7, 1/7, 1/7, 1/7, 0, 0],
             [1/7, 0, 0, 2/7, 0, 0, 1/7, 1/7, 1/7, 1/7, 0],
             [1/7, 0, 0, 0, 2/7, 0, 0, 1/7, 1/7, 1/7, 1/7],
             [1/7, 0, 0, 0, 0, 2/7, 0, 0, 1/7, 1/7, 2/7],
             [1/7, 0, 0, 0, 0, 0, 2/7, 0, 0, 1/7, 3/7],
             [1/7, 0, 0, 0, 0, 0, 0, 2/7, 0, 0, 4/7],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

#initial distribution matrix
init_mat = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
rounds = 50

# initialize zero arrays
results_mat = np.zeros((rounds+1, 11))
end_probs_2p = np.zeros((rounds+1, 1))
end_probs_3p = np.zeros((rounds+1, 1))
end_probs_4p = np.zeros((rounds+1, 1))


# find the probability the game ends at different player counts after i rounds. 
# end_prob_np: column vector (i=row, total rows = rounds) containing probabilities the game ends after i rounds at n players
for i in range(0, rounds+1):
    results_mat[i] = np.dot(init_mat, matrix_power(trans_mat, i))
    end_probs_1p = results_mat[:,10].reshape(rounds+1,1)
    end_probs_2p[i] = 1-(1-end_probs_1p[i])**2
    end_probs_3p[i] = 1-(1-end_probs_1p[i])**3
    end_probs_4p[i] = 1-(1-end_probs_1p[i])**4

plt.figure(figsize=(20,10))
plt.grid()
plt.plot(end_probs_1p, label='1 player')
plt.plot(end_probs_2p, label='2 player')
plt.plot(end_probs_3p, label='3 player')
plt.plot(end_probs_4p, label='4 player')
plt.legend(fontsize = 16)
plt.xlabel('Number of Rounds', fontsize = 20)
plt.xticks(np.linspace(0,50,num=11))
plt.ylabel('Cumulative Probability of Game Ending', fontsize = 20)
plt.yticks(np.linspace(0,1,num=11))
plt.title('Number of Rounds Probabilites for 1 - 4 Players in "Hi Ho! Cherry-O"', fontsize = 28)
plt.show()

repetitions = 10
max_players = 4
num_games = 150

# calls spin and removes the result from the player's tree
# if the tree ends up with over 10 cherries from their tree by putting more back than they have, reset the tree to 10
# if the tree ends up with negative cherries by removing more than they have, reset the tree to 0
# incriment turn count
def turn(player):
    tree[player] -= spin(player)
    if tree[player] > 10:
        tree[player] = 10
    elif tree[player] < 1:
        tree[player] = 0
    turn_count[player] += 1

    
# spins the spinner (1-7) and  determines how many cherries to remove from the active player's tree
# if cherries are returned to the tree, value is negative
# tree values can exceed 0 or 10. nonsense value are handled by turn function.
def spin(player):
    cherries_removed = 0
    result = np.random.randint(0,7)
    if result in range(0,4):
        cherries_removed += result+1
        return cherries_removed
    elif result == 4:
        cherries_removed -= 2   
        return cherries_removed
    elif result == 5:
        cherries_removed -= 2
        return cherries_removed
    else:
        return -10
    
    
winners = []
game_len = []
game_turns_mat = np.zeros((repetitions, max_players, num_games))
max_turns_mat=np.zeros((repetitions, max_players, num_games))

# generate random results
# Plays num_games times at each player count
# resets player trees to 10 and turn count to 0 at the start of every loop
# each player takes a turn until a tree reaches 0
# appends winning player to winning_player array
# counts number of game turns in game_turns_mat
for rep in range(0, repetitions):
    for players in range(0, max_players):
        for game in range(0, num_games):
            game_end = False
            tree = [10]*(players+1)    
            turn_count = [0]*(players+1)        
# This finishes the round and records all of the players that empty their trees            
            while game_end == False:
                for player in range(0, players+1):   
                    turn(player)
                    if tree[player] < 1:    
                        game_end = True
                        game_turns_mat[rep, players, game] = turn_count[player]
                        max_turns_mat[rep, players, game] = max(game_turns_mat[rep, players, :])
                        winners.append(player)
                        break
max_turns_mat_avg = max_turns_mat.mean(axis=0)


# Turns game_turns_mat and max_turns_mat to dataframe with multiinices in 'names'
names=['repetition','player_count','game_number']
repindices = []
player_list = []
for i in range(0,repetitions):
    repindices.append('rep'+str(i))
playerindices = []
for i in range(0,max_players):
    playerindices.append(str(i+1)+' player')
    player_list.append('player '+str(i+1))
index = pd.MultiIndex.from_product([repindices, playerindices, np.linspace(0,num_games-1,num_games).astype(int)], names=names)
game_data_df=pd.DataFrame({'game_data_df': game_turns_mat.flatten().astype(int)}, index=index)
game_data_df.columns = ['game_len']
game_data_df['longest_game_so_far'] = max_turns_mat.ravel().astype(int)
game_data_df['winners']=winners
game_data_df = game_data_df.reset_index()


# defines max_turns variable used later. Maximum number of turns at any player count
# initializes arrays for counting turns less than each length
max_turns = int(np.max(game_turns_mat))
count_mat = np.zeros((repetitions, max_players, max_turns+1))


# record proportion of games that ended after i rounds for each count of players, for each repetition, thens turn counts into percents
for rep in range(0, repetitions):
    for players in range(0, max_players):
        for i in range(0, max_turns+1):
            count_mat[rep, players,i] = len([k for k  in game_turns_mat[rep,players,:] if k<=i])
count_mat_percents = count_mat/num_games


# Turns count_mat and count_mat_percents to dataframe with multiinices in 'names'
names=['repetition','player_count','rounds_number']
index = pd.MultiIndex.from_product([repindices, playerindices, np.linspace(0,max_turns,max_turns+1).astype(int)], names=names)
completed_df=pd.DataFrame({'completed_df': count_mat.flatten().astype(int)}, index=index)
completed_df.columns = ['count_completed']
completed_df['percent_completed'] = completed_df['count_completed']/num_games
completed_df = completed_df.reset_index()

color_cycle = ['blue', 'orange', 'green', 'red', 'purple', 'cyan', 'black']
marker_cycle = ['.','x','1','+','d','o']

palette=sns.color_palette()[0:max_players]
plt.figure(figsize=(10,5))
sns.histplot(game_data_df, x='player_count', hue='winners', multiple='dodge', palette=palette)
plt.legend(player_list)
plt.title('Games Won per Player',fontsize=20)
plt.xlabel('Player Count',fontsize=16)
plt.ylabel('Number of Games Won',fontsize=16)
plt.show()

#finds the mean and listed quantiles for games completed at each player count and displays that info in a table
quantiles_mat = np.zeros((max_players, 7))
quantiles = [0.1, 0.25, 0.5, 0.75, 0.90, 0.99]
for player in range(0,max_players):
    quantiles_mat[player, 0] = round(game_data_df.loc[game_data_df.player_count == str(player+1)+' player', 'game_len'].mean(),0)
    for q in range(0,6):
        quantiles_mat[player, q+1] = round(game_data_df.loc[game_data_df.player_count == str(player+1)+' player', 'game_len'].quantile(quantiles[q]),0)
print('\nRounds to Complete X% of Games')
quantiles_df = pd.DataFrame(data=quantiles_mat, index=playerindices, columns=['Average','10%','25%','50%','75%','90%','99%'])
display(quantiles_df)
print('\n\n')

# Histogram
plt.figure(figsize=(10,5))
sns.histplot(game_data_df, x='game_len', hue='player_count', bins = 75, element='step')
plt.title('Distribution of Game Lengths',fontsize=20)
plt.xlabel('Number of Rounds', fontsize=16)
plt.ylabel('Number of Games', fontsize=16)   
plt.show()
print('\n\n')

# Violin Plot
plt.figure(figsize=(10,5))
sns.violinplot(x='player_count', y='game_len', data=game_data_df)
plt.title('Distribution of Game Lengths',fontsize=20)
plt.xlabel('Player Count', fontsize=16)
plt.ylabel('Number of Rounds', fontsize=16)   
plt.show()
print('\n\n')


# Plot the turn counts for each game
plt.figure(figsize=(20,10))
plt.title('Cumulative Percent of Games Ended', fontsize=28)
for rep in range(0,repetitions):
    for player in range(0,max_players):
        plt.scatter(x=completed_df.loc[(completed_df.player_count == '1 player')&(completed_df.repetition == 'rep0')]['rounds_number'],
                        y=completed_df.loc[(completed_df.player_count==str(player+1)+' player')&(completed_df.repetition == 'rep'+str(rep))]['percent_completed'], 
                        color =color_cycle[player], alpha=0.25)
plt.legend(playerindices, fontsize=16)
plt.grid()
plt.xlabel('Number of Rounds', fontsize=20)
plt.xlim(0,50)
plt.xticks(np.linspace(0,50,num=11))
plt.ylabel('Cumulative Percent of Game Ended', fontsize=20)
plt.yticks(np.linspace(0,1,num=11))
plt.show()

plt.figure(figsize=(20,10))
plt.title('Cumulative Percent of Games Ended with Theoretical Curve', fontsize=28)
for rep in range(0,repetitions):
    for player in range(0,max_players):
        plt.scatter(x=completed_df.loc[(completed_df.player_count == '1 player')&(completed_df.repetition == 'rep0')]['rounds_number'],
                    y=completed_df.loc[(completed_df.player_count==str(player+1)+' player')&(completed_df.repetition == 'rep'+str(rep))]['percent_completed'], 
                    color =color_cycle[player], alpha=0.25)
plt.legend(playerindices,fontsize=16)
plt.grid()
plt.xlabel('Number of Rounds', fontsize=20)
plt.xlim(0,50)
plt.xticks(np.linspace(0,50,num=11))
plt.ylabel('Cumulative Percent of Game Ended', fontsize=20)
plt.yticks(np.linspace(0,1,num=11))
plt.plot(end_probs_1p, label='theoretical probability', color='black')
plt.plot(end_probs_2p, color='black')
plt.plot(end_probs_3p, color='black')
plt.plot(end_probs_4p, color='black')
#plt.legend(fontsize=16)
plt.show()

# use markov chain to calculate the probability the game lasts more than x turns at each player count.
for player in range(0,max_players):
    print('\n'+str(player+1)+' player game theoretical probabilities:')
    for turns in [50, 100, 200]:
        print('Probability that a game lasts more than', turns,'turns = ', 
             '{:e}'.format((1-np.dot(init_mat, matrix_power(trans_mat, turns))[10])**(player+1)),
             '  -  Expect 1 in ', '{:e}'.format(1/((1-np.dot(init_mat, matrix_power(trans_mat, turns))[10])**(player+1))), 'games.')
    print('\n')

# plot the max number of turns for all trials at once if num_games <= 150
plt.figure(figsize=(20,10))
plt.title('Max Turns, Observed', fontsize=28)
if num_games <=150:
    for rep in range(0,repetitions):
        for player in range(0,max_players):
            plt.scatter(x=np.linspace(0, num_games,num_games), y=max_turns_mat[rep,player,:], color = color_cycle[player], alpha = 0.2)    
# Plot the maximum number of turns, averaged over all trials 
for player in range(0,max_players):
    plt.plot(max_turns_mat_avg[player,:], label = str(player+1)+ ' player observed average',  linewidth=3, color = color_cycle[player])
plt.legend(loc='upper left', fontsize=16)
plt.grid()
plt.xlabel('Games Played', fontsize=20)
plt.ylabel('Longest Game Recorded in Each Repetition', fontsize=20)
plt.show()
print('\n\n')

# estimate logarithmic line of best fit for each player count
def log_fit(x,a,b,c):
    return a+b*np.log(x+c)
a_vals=[]
b_vals=[]
c_vals=[]
x_vals = game_data_df.loc[(game_data_df.player_count == '1 player')&(game_data_df.repetition == 'rep0')]['game_number']
for player in range(0, max_players):
    y_vals = max_turns_mat_avg[player,:]
    popt, _ = curve_fit(log_fit, x_vals, y_vals, p0=[-5, 30, 5])
    a, b, c = popt
    a_vals.append(a)
    b_vals.append(b)
    c_vals.append(c)
    print(str(player+1)+' player regression: y = %.5f  + %.5f*log(x + %.5f)' % (a, b, c))


# plot data again with regressions
x_reg = np.arange(0,num_games)
plt.figure(figsize=(20,10))
plt.title('Max Turns Regressions', fontsize=28)
if num_games <=150:
    for rep in range(0,repetitions):
        for player in range(0,max_players):
            plt.scatter(x=np.linspace(0, num_games,num_games), y=max_turns_mat[rep,player,:], color = color_cycle[player], alpha = 0.1)         
for player in range(0,max_players):
    plt.plot(max_turns_mat_avg[player,:], linewidth=3, color = color_cycle[player], alpha = 0.25)
    y_reg = log_fit(x_reg, a_vals[player], b_vals[player], c_vals[player])
    plt.plot(x_reg, y_reg, color=color_cycle[player])
labels=[]
for player in range(0,max_players):
    labels.append(str(player+1)+' player observed average')
    labels.append(str(player+1)+' player regression')
plt.legend(labels, loc='upper left', fontsize=16)
plt.grid()
plt.xlabel('Games Played', fontsize=20)
plt.ylabel('Longest Game Recorded in Each Repetition', fontsize=20)
plt.show()

# prediction
def exp_calc(x,a,b,c):
    return np.exp((x-a)/b)-c
for player in range(0,max_players):
    print('\n\n'+str(player+1)+' player game:')
    for turns in [50, 100, 200]:
        print('\nregression predicts             ', '{:e}'.format(exp_calc(turns, a_vals[player], b_vals[player], c_vals[player])), 'games to play a game of length', turns,
             '\ncompared to theoretical value of', '{:e}'.format(1/((1-np.dot(init_mat, matrix_power(trans_mat, turns))[10])**(player+1))))
