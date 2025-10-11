# 6.009 Lab 2: Snekoban

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}

PLAYER = "player"
COMPUTER = "computer"
TARGET = "target"
WALL = "wall"
WIDTH = "width"
HEIGHT = "height"


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    targets = set()
    positions = set()
    walls = set()
    player = set()
    first_row = level_description[0]
    width = len(first_row)
    height = len(level_description)

    result = {
        PLAYER: player,
        COMPUTER: positions,
        TARGET: targets,
        WALL: walls,
        WIDTH: width,
        HEIGHT: height,
    }

    for row in range(len(level_description)):
        for col in range(len(level_description[0])):
            grid_cell = level_description[row][col]
            for item in grid_cell:
                result[item].add((row, col))
    result
    return {
        PLAYER: player.pop(),
        COMPUTER: frozenset(positions),
        TARGET: frozenset(targets),
        WALL: frozenset(walls),
        WIDTH: len(level_description[0]),
        HEIGHT: len(level_description),
    }


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """
    targets_available = len(game[TARGET]) > 0
    if not targets_available:
        return False
    return game[COMPUTER] <= game[TARGET]
    # all_computers_on_a_target = len(game[COMPUTER] - game[TARGET]) == 0
    # return targets_available and all_computers_on_a_target


def check_valid_move(game, direction):
    """
    checks if the player can move in the direction given. Returns a tuple of two booleans.
    The first represents if the player can move, and the second represents whether or not
    there's a computer in front of the player and if it can move.
    """
    # get new position of the player by adding the row and columns
    # of the current position and the direction vector
    x, y = (
        game["player"][0] + direction_vector[direction][0],
        game["player"][1] + direction_vector[direction][1],
    )
    # get the position in front of the new position (i.e. two steps away from the player)
    # to see if there are two computers in a row
    x_f, y_f = (x + direction_vector[direction][0], y + direction_vector[direction][1])

    # check if there's a computer in front of it
    if (x, y) in game["computer"]:
        # check if there's something in front of the computer
        if not ((x_f, y_f) in game["wall"] or (x_f, y_f) in game["computer"]):
            # if both can move, return True for both
            return (True, True)
    # check if there's not a wall. If so, valid move so update board
    elif (x, y) not in game["wall"]:
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
        TARGET: game[TARGET],
        HEIGHT: game[HEIGHT],
        WIDTH: game[WIDTH],
        PLAYER: game[PLAYER],
        COMPUTER: game[COMPUTER],
        WALL: game[WALL],
    }
    # possible new position
    x, y = (
        game[PLAYER][0] + direction_vector[direction][0],
        game[PLAYER][1] + direction_vector[direction][1],
    )
    # possible new position for computer
    x_f, y_f = (x + direction_vector[direction][0], y + direction_vector[direction][1])

    # if there's a computer in front of the player, and both can move
    # update the positions of both
    valid, move_comp = check_valid_move(result, direction)
    if valid and move_comp:
        # move is valid so update player position
        result[PLAYER] = (x, y)
        # update computer position
        result[COMPUTER] = (result[COMPUTER] - {(x, y)}) | {(x_f, y_f)}
        # result[COMPUTER].remove((x, y))
        # result[COMPUTER].add((x_f, y_f))
    # only player can move, so check if there's not a wall.
    # If so, valid move so update board
    elif valid:
        result[PLAYER] = (x, y)
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
    output = [[[] for numb in range(game[WIDTH])] for y in range(game[HEIGHT])]
    # go through every set
    for item in [COMPUTER, TARGET, WALL]:
        for x, y in game[item]:
            # store whatever the item set is in the current coordinate
            output[x][y].append(item)
    output[game[PLAYER][0]][game[PLAYER][1]].append(PLAYER)
    return output


def construct_path(end_node, predecessor):
    path = []
    curr_node, step = predecessor[end_node]
    while curr_node != None:
        path.append(step)
        curr_node, step = predecessor[curr_node]

    path.reverse()
    return path


def make_doubly_linked_list():
    return {"length": 0, "head": None, "tail": None}


def push_doubly_linked_list(ll, item):
    head = ll["head"]
    if head is None:
        ll["head"] = {"value": item, "prev": None, "next": None}
        ll["tail"] = ll["head"]
    else:
        new_node = {"value": item, "prev": ll["tail"], "next": None}
        ll["tail"]["next"] = new_node
        ll["tail"] = new_node
    ll["length"] += 1


def pop_doubly_linked_list(ll):
    head = ll["head"]
    if head is None:
        return None
    else:
        item = ll["head"]["value"]
        ll["head"] = ll["head"]["next"]
        ll["length"] -= 1
        return item


def make_queue():
    size = 50000
    return {
        "data": [None] * size,
        "head": 0,
        "tail": 0,
        "size": 0,
        "capacity": size,
    }


def enqueue(q, item):
    if q["size"] == q["capacity"]:
        # optional: resize
        q["data"].extend([None] * q["capacity"])
        q["capacity"] *= 2
    q["data"][q["tail"]] = item
    q["tail"] = (q["tail"] + 1) % q["capacity"]
    q["size"] += 1


def dequeue(q):
    if q["size"] == 0:
        return None
    item = q["data"][q["head"]]
    q["head"] = (q["head"] + 1) % q["capacity"]
    q["size"] -= 1
    return item


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    # keep track of seen states of the game
    visited = set()
    # queue will hold positions needed to be explored as well the path
    # that got us to the position being added to queue
    queue = make_queue()

    # Mark the player's current position as visited
    # and also add it to queue
    start_node = (game[COMPUTER], game[PLAYER])
    predecessor = {start_node: (None, None)}
    # queue.append(game)
    enqueue(queue, game)
    visited.add(start_node)

    while queue["size"] != 0:
        # curr_game will be tuple containing the position needed to be explored
        # and the path that got us there
        # curr_game = queue.pop(0)
        curr_game = dequeue(queue)

        curr_state = (curr_game[COMPUTER], curr_game[PLAYER])
        if victory_check(curr_game):
            return construct_path(curr_state, predecessor)
        # add all 4 cardinal directions
        for direction in direction_vector.keys():
            next_game = step_game(curr_game, direction)
            state = (next_game[COMPUTER], next_game[PLAYER])
            if state not in visited:
                # queue.append(next_game)
                enqueue(queue, next_game)
                predecessor[state] = (curr_state, direction)
                visited.add(state)
    return None


if __name__ == "__main__":
    pass
