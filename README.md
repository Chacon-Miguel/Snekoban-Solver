# Snekoban Solver
 A-Star Algorithm for solving Sokoban maps

## Contents
MAKE SURE TO INCLUDE STUFF ABOUT THE GUI, TEST LEVELS, INPUTS, OUTPUS, ETC.

## Introduction
In this lab, a version of a popular game called Sokoban was implemented. The original game involves moving a person around a virtual warehouse floor, pushing boxes onto target locations, until each target is covered with a box. In our version ("Snekoban"), rather than a warehouse worker, the player controls a little python, and the goal is to push computers around a world surrounded by walls until every target is covered with a computer.

I first started by implementing the rules of the game (which are described in much more detail below), and then wrote an additional program that solves Sokoban puzzles, producing as output a sequence of moves that takes us from a starting configuration to one that solves the puzzle.

## Game Rules
This section talks through the various components that make up the game, and the rules of the game. 

### Board
The game board is an $m \times n$ grid, where $m$ and $n$ are the number of rows and columns, respectively. The location of each cell at row `i` and column `j` are represented as a Python tuple, `(i, j)`. Each cell of the board may contain zero, one, or multiple objects. In a valid puzzle, there will always be the same number of computers as targets.

The canonical representation represents the board as a Python list of lists of lists of strings, where the first two layers of lists are for rows and columns, and the third layer of list is to list all the objects in each location. For instance, here is a board with a computer in location `(1, 2)`, and a player and a target in location `(2, 3)` has the following canonical representation:

```
[
   [["wall"],  ["wall"],  ["wall"],      ["wall"],             ["wall"], ["wall"]],
   [["wall"],  [],        ["computer"],  [],                   [],       ["wall"]],
   [["wall"],  [],        [],            ["target", "player"], [],       ["wall"]],
   [["wall"],  ["wall"],  ["wall"],      ["wall"],             ["wall"], ["wall"]]
]
```

### Objects
There are four possible different kinds of objects in the game: the player, computers, walls, and targets.

#### The Player
The player of the game controls a python. The player can move around the board by pressing the arrow keys. Pressing an arrow key will attempt to move the player in the given direction, subject to some interactions described below.

#### Walls
Walls are stationary objects that prevent movement. Any object attempting to move to a location occupied by a wall instead remains in its original position.

In all of the provided puzzles, the board is completely surrounded by walls. Your code does not need to handle other cases.

#### Computers
Computers are objects that the player can push around the board. If the player attempts to move to a location containing a computer, the computer should be "pushed" in the same direction in which the player was moving, unless doing so would move the computer in question onto a wall or another computer (in which case all objects, including the player, remain in their original positions instead).

For example, starting from the board configuration shown on the left below, moving downward will push the computer down, resulting in the configuration on the right:

#### Targets
Targets represent locations to which we would like to push computers. Targets are always stationary.

The goal of the game is to push computers onto targets. Each game starts with the same number of computers and targets, and the game is won when every spot containing a target also contains a computer.

It is possible that some targets already begin in the same spot as a computer, but in some cases, the solution may involve moving that computer away, either temporarily or permanently.

### Implementation

#### Internal Representation of Game
The game was represented as a dictionary with the following keys:

player: it's a tuple containing the snake's current position
computer: a set of the positions of the computers
target: a frozenset of the positions of the targets
wall: a frozenset of the positions of the walls
w: width of the board
h: height of the board

Since the walls cannot move (i.e. static), the best representation for them was a frozenset of the positions on the board where they are located. This allows us to get $O(1)$ time to check if the player is going to run into a wall. That's also why the same representation was used for targets.

Then, since two computers can't be in the same position, we are guaranteed that there positions are unique. Thus, a set was used to represent them since this allows us to get $O(1)$ time to check where the computers are.

And lastly, the player's positions was stored as a tuple since all other positions were stored in either sets of frozensets as tuples. 

#### Rules of the Game

The main rules are the following:
* The player and computers cannot move outside the board.
* The player and computers cannot be in the same position as a wall
* The player can only push one computer.

When the player then moves in one of the cardinal directions, the new potential position is calculated and the following is checked:
* if the new position contains a wall. We do this by checking if the position is in the set of the wall positions. If it is, the player cannot move.
* if the new positions contains a computer, which is checked by seeing if the new position is in the set of computer positions. If this is the case, we calculate the position in front of the new position. (The position if the player moved in the same direction twice.) If there are two computer in front of the snake, then we cannot move.
* If only one computer is present, we then see if moving both are still in bounds. If it is, we change it's position along with the snake.

#### Solving the game
The first step taken to solve the game is to find the deadspots of the game, which are positions where if a computer lands on it, the game becomes unsolvable. A simple approach was taken. First, the corners formed by the walls were found. If a target was not on them, then the corner is a deadspot (since the player won't be able to push it out of the corner). From there, every wall that helps in forming a corner is then checked for dead edges. These positions are then saved in a set since they are all unique.

From there, a set called visited is started, which will contain all of the game states we've seen thus far (game states, meaning positions of all players). A queue, implemented as a list is also initiated.

The queue will hold lists that then hold the following items:
* a game state that needs to be explored
* a list of steps that got us to this game state.

The first thing added to the queue is thus the starting state of the game, and an empty list since no steps have been taken thus far. Moreover, the first thing added to the set visited is a tuple containing the frozensets of the computer's position and another frozenset containing the player's positions.

Afterwards, the initial game state is taken off the queue. A function that checks if the game has been won is called to see if we stop searching for a solution. If the game hasn't been won, we continue, where the first thing we do is get the neighboring game states. These are obtained by simply moving the snake in the 4 cardinal directions.

Once the game states are obtained, we then check if any computers have been moved to a deadspot. If that's the case, there is no need to continue exploring this game state since its unsolvable. We thus don't add it to the queue. Then, for all valid game states, we get the estimated remaining distance along with the current moved distance and sort them using that heuristic. We then add all of them to the queue and continue until a solution is found.

If the queue at some point becomes empty before a solution was found, then we know that no solution is possible so we return `None`.