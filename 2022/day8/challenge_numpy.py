#!/usr/bin/python
# --- Day 8: Treetop Tree House ---
# The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.

# First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

# The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

# 30373
# 25512
# 65332
# 33549
# 35390
# Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

# A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

# All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

# The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
# The top-middle 5 is visible from the top and right.
# The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
# The left-middle 5 is visible, but only from the right.
# The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
# The right-middle 3 is visible from the right.
# In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
# With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

# Consider your map; how many trees are visible from outside the grid?
import os
import sys
import logging
from math import prod
import numpy as np

logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
PUZZLE_INPUT = f"{os.path.dirname(os.path.realpath(__file__))}/puzzle_input.txt"


def parse_input():
    with open(PUZZLE_INPUT, "r") as f:
        lines = f.readlines()
    return lines


dtype = np.dtype(
    [
        ("x", int),
        ("y", int),
        ("height", int),
        ("visible_north", bool),
        (
            "visible_south",
            bool,
        ),
        (
            "visible_east",
            bool,
        ),
        ("visible_west", bool),
        ("visible_north_count", int),
        ("visible_south_count", int),
        ("visible_east_count", int),
        ("visible_west_count", int),
    ]
)
array = np.empty((99, 99), dtype=dtype)
lines = parse_input()
for y, line in enumerate(lines):
    values = line.strip()
    for x, value in enumerate(values):
        array[y][x]["x"] = x
        array[y][x]["y"] = y
        array[y][x]["height"] = int(value)


def get_visible_trees(array, x, y, direction):
    if direction == "north":
        for i in range(y - 1, -1, -1):
            if array[i][x]["height"] >= array[y][x]["height"]:
                return False
        return True
    elif direction == "south":
        for i in range(y + 1, len(array)):
            if array[i][x]["height"] >= array[y][x]["height"]:
                return False
        return True
    elif direction == "east":
        for i in range(x + 1, len(array[y])):
            if array[y][i]["height"] >= array[y][x]["height"]:
                return False
        return True
    elif direction == "west":
        for i in range(x - 1, -1, -1):
            if array[y][i]["height"] >= array[y][x]["height"]:
                return False
        return True


for y, line in enumerate(array):
    for x, value in enumerate(line):
        array[y][x]["visible_north"] = get_visible_trees(array, x, y, "north")
        array[y][x]["visible_south"] = get_visible_trees(array, x, y, "south")
        array[y][x]["visible_east"] = get_visible_trees(array, x, y, "east")
        array[y][x]["visible_west"] = get_visible_trees(array, x, y, "west")

visible_trees = 0
for y, line in enumerate(array):
    for x, value in enumerate(line):
        if (
            array[y][x]["visible_north"]
            or array[y][x]["visible_south"]
            or array[y][x]["visible_east"]
            or array[y][x]["visible_west"]
        ):
            visible_trees += 1

print(f"no. of visible trees: {visible_trees}")

# --- Part Two ---
# Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

# To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

# The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

# In the example above, consider the middle 5 in the second row:

# 30373
# 25512
# 65332
# 33549
# 35390
# Looking up, its view is not blocked; it can see 1 tree (of height 3).
# Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
# Looking right, its view is not blocked; it can see 2 trees.
# Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).
# A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

# However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

# 30373
# 25512
# 65332
# 33549
# 35390
# Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
# Looking left, its view is not blocked; it can see 2 trees.
# Looking down, its view is also not blocked; it can see 1 tree.
# Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
# This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

# Consider each tree on your map. What is the highest scenic score possible for any tree?

most_scenic_score = 0
for y, line in enumerate(array):
    for x, value in enumerate(line):
        north = 0
        south = 0
        east = 0
        west = 0
        for i in range(y - 1, -1, -1):
            north += 1
            if array[i][x]["height"] >= array[y][x]["height"]:
                break
        for i in range(y + 1, len(array)):
            south += 1
            if array[i][x]["height"] >= array[y][x]["height"]:
                break
        for i in range(x + 1, len(array[y])):
            east += 1
            if array[y][i]["height"] >= array[y][x]["height"]:
                break
        for i in range(x - 1, -1, -1):
            west += 1
            if array[y][i]["height"] >= array[y][x]["height"]:
                break
        scenic_score = prod([north, south, east, west])
        if scenic_score > most_scenic_score:
            most_scenic_score = scenic_score

print(f"most scenic score: {most_scenic_score}")
