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
        self.size = {"x": len(lines[0]), "y": len(lines)}
        for y, line in enumerate(lines):
            line = line.rstrip()
            for x, char in enumerate(line):
                self.trees.append(Tree(x, y, int(char)))

    def __repr__(self):
        return f"Forest(trees={len(self.trees)})"

    def find_trees(self, filter_params={}):
        logger.debug(f"Searching for trees with filter params: {filter_params}")

        def _find_trees(tree_list, filter_params):
            for item in tree_list:
                if all(
                    item.__dict__.get(key, None) == val
                    for key, val in filter_params.items()
                ):
                    yield item

        # detect dict in filter params
        filter_param_dict = False
        for key, value in filter_params.items():
            if isinstance(value, dict):
                filter_param_dict = True
                break

        # Find all the items that match the lt/gt filter
        if filter_param_dict:
            initial_found_items = []
            for item in self.trees:
                for sub_key, sub_value in value.items():
                    if sub_key == "$lt":
                        if item.__dict__[key] < sub_value:
                            initial_found_items.append(item)
                    elif sub_key == "$gt":
                        if item.__dict__[key] > sub_value:
                            initial_found_items.append(item)
                    elif sub_key == "$lte":
                        if item.__dict__[key] <= sub_value:
                            initial_found_items.append(item)
                    elif sub_key == "$gte":
                        if item.__dict__[key] >= sub_value:
                            initial_found_items.append(item)

                    # Then remove dictionaries from the filter params
                    filter_params = {
                        key: value
                        for key, value in filter_params.items()
                        if not isinstance(value, dict)
                    }

        # Find all the items that match the remaining filter params
        found_items = []
        if filter_param_dict:
            found_items = _find_trees(initial_found_items, filter_params)
        else:
            found_items = _find_trees(self.trees, filter_params)
        return found_items

    def related_trees(self, tree):
        logger.debug(f"Finding related trees for tree: {tree}")
        related_trees = {"left": [], "right": [], "up": [], "down": []}
        related_trees["left"] = self.find_trees({"y": tree.y, "x": {"$lt": tree.x}})
        related_trees["right"] = self.find_trees({"y": tree.y, "x": {"$gt": tree.x}})
        related_trees["up"] = self.find_trees({"x": tree.x, "y": {"$lt": tree.y}})
        related_trees["down"] = self.find_trees({"x": tree.x, "y": {"$gt": tree.y}})

        # Important to sort these to ensure closest tree is evaluated first
        related_trees["left"] = sorted(
            related_trees["left"], key=lambda x: x.x, reverse=True
        )
        related_trees["up"] = sorted(
            related_trees["up"], key=lambda x: x.y, reverse=True
        )
        return related_trees

    def check_visbility(self, tree):
        logger.debug(f"Checking visibility for tree: {tree}")
        visibile_from = ["left", "right", "up", "down"]
        visibility = {"left": 0, "right": 0, "up": 0, "down": 0}
        related_trees = self.related_trees(tree)
        for direction, trees in related_trees.items():
            for related_tree in trees:
                visibility[direction] += 1
                logger.debug(
                    f"{related_tree} visible from {tree}. Visibility count: {visibility[direction]}"
                )
                if related_tree.height >= tree.height:
                    logger.debug(
                        f"{tree} is not visible from {direction} due to {related_tree}"
                    )
                    visibile_from.remove(direction)
                    break
        tree.visible_from = visibile_from
        tree.visibility = visibility
        logger.debug(
            f"visibility for: {tree}, visible from: {tree.visible_from}, visibility: {tree.visibility}"
        )
        return tree


class Tree:
    def __init__(self, x, y, height):
        self.id = x + y
        self.x: int = x
        self.y: int = y
        self.height: int = height
        self.visible_from = []
        self.visibility = {}

    def __repr__(self):
        return f"Tree(x={self.x}, y={self.y}, height={self.height}, visible_from={self.visible_from}, visibility={self.visibility}, scenic_score={self.scenic_score})"

    def __str__(self):
        return f"Tree(x={self.x}, y={self.y}, height={self.height}, visible_from={self.visible_from}, visibility={self.visibility}, scenic_score={self.scenic_score})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __gt__(self, other):
        return self.height > other.height

    def __lt__(self, other):
        return self.height < other.height

    @property
    def scenic_score(self):
        return prod(self.visibility.values())


forest = Forest(parse_input())
logger.info(f"forest: {forest}")
for idx, tree in enumerate(forest.trees):
    forest.trees[idx] = forest.check_visbility(tree)

print(
    f"no. of visible trees: {len([tree for tree in forest.trees if tree.visible_from])}"
)

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

most_scenic_tree = sorted(forest.trees, key=lambda x: x.scenic_score, reverse=True)[0]
print(f"most scenic tree: {most_scenic_tree}")
