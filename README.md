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
