# 6.009 Lab 2: Snekoban

import json
import typing

# direction vector
d_v = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation, which is a dictionary that contains 6 keys:
    -  player maps to a tuple containing the player position (row, column)
    - computer maps to a set of the positions of the computers. This is fine since no
      computers can be in the same position, so all of them are unique
    - target: maps to a set of the positions of all the flags.
    - wall: maps to a frozenset of the positions of the walls. 
    - w: maps to width of the board
    - h: maps to height of the board


    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]


    """
    targets = set()
    positions = set()
    walls = set()
    player = ()
    for row in range(len(level_description)):
        for col in range(len(level_description[0])):
            if 'player' in level_description[row][col]:
                player = (row, col)
            if 'target' in level_description[row][col]:
                targets.add((row, col))
            if 'computer' in level_description[row][col]:
                positions.add((row, col))
            if 'wall' in level_description[row][col]:
                walls.add((row, col))
    return {
        'player': player,
        'computer': positions,
        'target': frozenset(targets),
        'wall': frozenset(walls),
        'w': len(level_description[0]),
        'h': len(level_description)
    }
    

def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """
    # if there are no targets available, winning impossible so return False
    if len(game['target']) == 0:
        return False
    # check if every computer is in the same position as the flags
    for computer in game['computer']:
        # if any computer isn't matched to a flag, player has not won yet
        if computer not in game['target']:
            return False
    return True

def check_valid_move(game, direction):
    """
    checks if the player can move in the direction given. Returns a tuple of two booleans.
    The first represents if the player can move, and the second represents whether or not 
    there's a computer in front of the player and if it can move.
    """
    # get new position of the player by adding the row and columns
    # of the current position and the direction vector
    x, y = (game['player'][0]+d_v[direction][0], game['player'][1]+d_v[direction][1])
    # get the position in front of the new position (i.e. two steps away from the player)
    # to see if there are two computers in a row
    x_f, y_f = (x+d_v[direction][0], y+d_v[direction][1])

    # check if there's a computer in front of it
    if (x, y) in game['computer']:
        # check if there's something in front of the computer
        if not ((x_f, y_f) in game['wall'] or (x_f, y_f) in game['computer']):
            # if both can move, return True for both
            return (True, True)
    # check if there's not a wall. If so, valid move so update board
    elif (x, y) not in game['wall']:
        return (True, False)
    return (False, False)

def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    result = {
        'target': game['target'],
        'h': game['h'],
        'w': game['w'],
        'player': game['player'],
        'computer': game['computer'].copy(),
        'wall': game['wall']
    }
    # possible new position
    x, y = (game['player'][0]+d_v[direction][0], game['player'][1]+d_v[direction][1])
    # possible new position for computer
    x_f, y_f = (x+d_v[direction][0], y+d_v[direction][1])

    # if there's a computer in front of the player, and both can move
    # update the positions of both
    valid, move_comp = check_valid_move(result, direction)
    if valid and move_comp:
        # move is valid so update player position
        result['player'] = (x, y)
        # update computer position
        result['computer'].remove((x, y))
        result['computer'].add((x_f, y_f))
    # only player can move, so check if there's not a wall. 
    # If so, valid move so update board
    elif valid:
        result['player'] = (x, y)
    return result

def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    output = [ [ [] for numb in range(game['w']) ]  for y in range(game['h']) ] 
    # go through every set
    for item in ['computer', 'target', 'wall']:
        for x, y in game[item]:
            # store whatever the item set is in the current coordinate
            output[x][y].append(item)
    output[game['player'][0]][game['player'][1]].append('player')
    return output

def get_dead_edges(game, deadspots, dc_coords, r_wall_loc, c_wall_loc):
    """
    Given the following parameters:
    - game: the current state of the game
    - deadspots, the current list of deadspots found (i.e. corners)
    - dc_coords: the coordinates of a dead corner found
    - r_wall_loc: the position of the wall that forms the corner. So for example, if 
        the top-left corner was found, then r_wall_loc would be 'left' since the corner
        was formed by a wall on the left.
    - c_wall_loc: same concept as r_wall_loc but for horizontal walls. Going back to the 
        top-left corner example, this would be 'top' since the corner was formed by a wall
        on the top of the corner's position.

    Adds dead edges to deadspots by starting from a corner found and then checking its
    row and then column. Does not mutate given deadspots.
    """
    result = deadspots.copy()
    # go through row
    # check if wall is on left or right.
    # Then find the length of the wall and the possible directions
    # that a player could move if it was adjacent to the wall

    # if in any position, a player can't move in three directions, dead edge found.
    if r_wall_loc == 'left':
        length = range(dc_coords[1], game['w'] -1)
        poss_directions = ['right', 'up', 'down']
    # wall is on right
    else:
        length = range(dc_coords[1], 0, -1)
        poss_directions = ['left', 'up', 'down']
    # for every position adjacent to the wall...
    for d_col in length:
        # get current position being checked
        curr_post = (dc_coords[0] + d_v[c_wall_loc][0], d_v[c_wall_loc][1] + d_col )
        # check if wall is still next to position
        if curr_post in game['wall']:
            # check if there is a target on the edge
            for t in game['target']:
                # if there's a target on the edge, then this can't be a dead edge
                if t[0] == dc_coords[0]:
                    break
            # if there isn't, check if you can move in 3 directions:
            moves = [check_valid_move(game, d)[0] for d in poss_directions if check_valid_move(game, d)[0]]
            if False in moves:
                # dead edge found
                if not (dc_coords[0], d_col) in result:
                    result.add((dc_coords[0], d_col))
        else:
            break
    # go through column
    # check if wall is on top or bottom.
    # Then get the wall's width (i.e. length of wall) and the possible direction
    # that a player could move if it was adjacent to the wall
    if c_wall_loc == 'up':
        width = range(dc_coords[0], 0, -1)
        poss_directions = ['right', 'left', 'down']
    else:
        width = range(dc_coords[0], game['h'] -1)
        poss_directions = ['right', 'up', 'left']
    # for every spot on this current row...
    for d_row in width:
        # get current spot or position
        curr_post = (d_row + d_v[r_wall_loc][0], dc_coords[1] + d_v[c_wall_loc][1] )
        # check if wall is still next to position
        if curr_post in game['wall']:
            # check if there is a target on the edge
            for t in game['target']:
                if t[1] == dc_coords[1]:
                    break
            # if there isn't, check if you can move in 3 directions:
            moves = [check_valid_move(game, d)[0] for d in poss_directions if check_valid_move(game, d)[0]]
            if False in moves:
                # dead edge found
                if not (d_row, dc_coords[1]) in result:
                    result.add((d_row, dc_coords[1]))
        break
    return result

def get_deadspots(game):
    """Returns a set that holds all deadspots in game"""
    deadspots = set()
    # for every position...
    for row in range(1, game['h']-1):
        for col in range(1, game['w']-1):

            # get current position
            position = (row, col)

            # if there's a target on this edge, skip it
            # since this can never be a deadspot
            if position in game['target']:
                continue

            # get positions in all 4 caridnal directions
            t_post = (row + d_v['up'][0], col + d_v['up'][1])
            b_post = (row + d_v['up'][0], col + d_v['up'][1])
            l_post = (row + d_v['left'][0], col + d_v['left'][1])
            r_post = (row + d_v['right'][0], col + d_v['right'][1])

            # get corners since if a computer lands on one
            # the computer can't be pushed anymore, so the game is lost
            # once corner is found, get all dead edges that start from the corner found
            if position not in game['wall']:
                # check if wall is on top
                if t_post in game['wall']:
                    # check if on left
                    if l_post in game['wall']:
                        # dead corner found
                        deadspots.add((row, col))
                        deadspots = get_dead_edges(game, deadspots, (row, col), 'left', 'up')
                    # check if on right
                    elif r_post in game['wall']:
                        deadspots.add((row, col))
                        deadspots = get_dead_edges(game, deadspots, (row, col), 'right', 'up')
                elif b_post in game['wall']:
                    # check if on left
                    if l_post in game['wall']:
                        deadspots.add((row, col))
                        deadspots = get_dead_edges(game, deadspots, (row, col), 'left', 'down')
                    # check if on right
                    elif r_post in game['wall']:
                        deadspots.add((row, col))
                        deadspots = get_dead_edges(game, deadspots, (row, col), 'right', 'up')
    return deadspots

def get_min_distances(computers, goals):
    """
    Returns total min distance between computer and either the targets or the player
    """
    # target pull distances has the key as 
    # (target, computer position) -> pull distance
    total_min_distance = 0
    for goal in goals:
        min_distance = float('inf')
        for computer in computers:
            min_distance = min( min_distance, get_manhattan(goal, computer) )
        total_min_distance += min_distance
    
    return total_min_distance


def get_manhattan(pos_1, pos_2):
    return abs(pos_1[1] - pos_2[1]) + abs(pos_1[0] - pos_2[0])

def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.

    First get all the deadspots of the game, which are the positions where, if a computer
    lands on it, the game is no longer solveable. Then, use uniform-cost search by greedily 
    choosing the next positions to add to the queue. 

    Adding positions to the queue until the game is won. If the queue ever becomes empty,
    then we know that there are no solutions to the game, so return None
    """
    # get deadspots
    deadspots = set(get_deadspots(game))

    # keep track of seen states of the game
    visited = set()
    # queue will hold positions needed to be explored as well the path 
    # that got us to the position being added to queue
    queue = []
    # Mark the player's current position as visited
    # and also add it to queue
    queue.append([game, []])
    visited.add((frozenset(game['computer']), frozenset([game['player']])))
    # visited.add( frozenset(game['computer']) )
    while len(queue) != 0:
        # curr_game will be tuple containing the position needed to be explored
        # and the path that got us there
        curr_game = queue.pop(0)
        # get all adjacent position of the dequeued position curr_path
        # If the adjacent position hasn't been visited, then mark it
        # and then enqueue it

        # if game has been solved, return the path used to get to victory
        if victory_check(curr_game[0]):
            return curr_game[1]
        # add all 4 cardinal directions
        next_nodes = []
        for direction, coords in d_v.items():
            # total mininum distance
            total_min_d = 0
            next_node = step_game(curr_game[0], direction)
            # check if any computer is in dead spot. If so this, state doesn't 
            # need to be added to queue
            for pos in next_node['computer']:
                if pos in deadspots:
                    break
            else:
                # get min distance between computers and targets
                total_min_d += get_min_distances(next_node['computer'], next_node['target']) 
                total_min_d += get_min_distances(next_node['computer'], [next_node['player']])
                next_nodes.append((total_min_d, next_node, direction))
            # sort 4 cardinal direction in ascending order and enqueue all of them
            sorted_nodes = sorted(next_nodes, key = lambda x: x[0])

            for distance, node, direction in sorted_nodes:
                state = (frozenset(node['computer']), frozenset([node['player']]))
                # state = frozenset(node['computer'])
                if state not in visited:
                    queue.insert(0, [node, curr_game[1] + [direction]])
                    visited.add(state)
    return None

if __name__ == "__main__":
    pass