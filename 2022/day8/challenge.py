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
from pprint import pformat, pprint

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


class Forest:
    def __init__(self, lines):
        self.trees = []
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                self.trees.append(Tree(x, y, char))

    def __repr__(self):
        return f"Forest(trees={len(self.trees)})"

    def count_visible_trees(self):
        visible_trees = 0
        for tree in self.trees:
            if self.is_visible(tree):
                visible_trees += 1
        return visible_trees

    def find_trees(self, filter_params={}):
        found_items = []

        for item in self.trees:
            # if all(
            #     item.__dict__.get(key, None) == val
            #     for key, val in filter_params.items()
            # ):

            for key, value in filter_params.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if sub_key == "$lt":
                            if item.__dict__[key] >= sub_value:
                                break
                        elif sub_key == "$gt":
                            if item.__dict__[key] <= sub_value:
                                break
                else:
                    if item.__dict__[key] != value:
                        break
            else:

                found_items.append(item)
        return found_items

    def related_trees(self, tree):
        related_trees = {"left": [], "right": [], "top": [], "bottom": []}
        related_trees["left"] = self.find_trees({"y": tree.y, "x": {"$lt": tree.x}})
        related_trees["right"] = self.find_trees({"y": tree.y, "x": {"$gt": tree.x}})
        related_trees["top"] = self.find_trees({"x": tree.x, "y": {"$lt": tree.y}})
        related_trees["bottom"] = self.find_trees({"x": tree.x, "y": {"$gt": tree.y}})
        return related_trees

    def is_visible(self, tree):
        related_trees = self.related_trees(tree)
        for direction, trees in related_trees.items():
            if not trees:
                continue
            if direction in ["left", "top"]:
                trees.sort(key=lambda x: x.__dict__[direction], reverse=True)
            else:
                trees.sort(key=lambda x: x.__dict__[direction])
            for related_tree in trees:
                if related_tree.height > tree.height:
                    return False
        return True


class Tree:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.visible_from = []

    def __repr__(self):
        return f"Tree(x={self.x}, y={self.y}, height={self.height})"


lines = parse_input()
forest = Forest(lines)
logger.info(f"forest: {forest}")
# logger.info(f"trees: {forest.trees}")
print(forest.related_trees(forest.trees[2]))
