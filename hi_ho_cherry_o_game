import numpy as np
import myfunctions as mf


# calls spin and removes the result from the player's tree
# if the tree ends up with over 10 cherries from their tree by putting more back than they have, reset the tree to 10
# if the tree ends up with negative cherries by removing more than they have, reset the tree to 0
# print their tree status and turn result
# incriment turn count
def turn(player):
    print('Player', player+1, 'has', tree[player], 'cherries in their tree at the start of their turn.')
    tree[player] -= spin(player)
    if tree[player] > 10:
        tree[player] = 10
    elif tree[player] < 1:
        tree[player] = 0
    print('Player', player+1, 'has', tree[player], 'cherries left in their tree.\n')
    turn_count[player] += 1
       
        
# spins the spinner (1-7) and  determines how many cherries to remove from the active player's tree
# if cherries are returned to the tree, value is negative
# prints the spinner results
# tree values can exceed 0 or 10. nonsense value are handled by turn function.
def spin(player):
    cherries_removed = 0
    result = np.random.randint(1,8)
    if result in range(1,5):
        cherries_removed += result
        print('Player', player+1, 'removes', result, 'cherries from their tree!')
        return cherries_removed
    elif result == 5:
        cherries_removed -= 2
        print('Player', player+1, 'spun the bird and put 2 cherries back in the tree!')    
        return cherries_removed
    elif result == 6:
        cherries_removed -= 2
        print('Player', player+1, 'spun the dog and put 2 cherries back in the tree!')
        return cherries_removed
    else:
        print('Uh oh! Player', player+1, 'spilled their basket and put all their cherries back in the tree!')
        return -10
    

#ask the user how many players there are
players = mf.input_in_range(1, 5, 'How many players?')   


#define initial arrays with initial values
#trees are full (10 cherries per player)
#turn count is 0 for each player at the beginning of the game
#the game hasn't ended yet
tree = [10]*(players)
turn_count = [0]*(players)
game_end = False


# players take turns until someone's tree gets to 0
while game_end == False:
    for player in range(0, players):
        turn(player)
        if tree[player] < 1:
            game_end = True
            print('The game is over. Player', player+1, 'wins! It took', turn_count[player], 'turns.')
            break
