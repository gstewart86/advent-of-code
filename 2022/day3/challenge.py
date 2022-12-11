#!/usr/bin/python
import logging
import sys
from pprint import pformat
import os

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
PUZZLE_INPUT = f"{os.path.dirname(os.path.realpath(__file__))}/puzzle_input.txt"


def parse_input():
    with open(PUZZLE_INPUT, "r") as f:
        lines = f.readlines()
    return lines


# --- Day 3: Rucksack Reorganization ---
# One Elf has the important job of loading all of the rucksacks with supplies for the jungle journey. Unfortunately, that Elf didn't quite follow the packing instructions, and so a few items now need to be rearranged.

# Each rucksack has two large compartments. All items of a given type are meant to go into exactly one of the two compartments. The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.

# The Elves have made a list of all of the items currently in each rucksack (your puzzle input), but they need your help finding the errors. Every item type is identified by a single lowercase or uppercase letter (that is, a and A refer to different types of items).

# The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the same number of items in each of its two compartments, so the first half of the characters represent items in the first compartment, while the second half of the characters represent items in the second compartment.

# For example, suppose you have the following list of contents from six rucksacks:

# vJrwpWtwJgWrhcsFMMfFFhFp
# jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
# PmmdzqPrVvPwwTWBwg
# wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
# ttgJtRGJQctTZtZT
# CrZsJsPPZsGzwwsLwLmpwMDw
# The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means its first compartment contains the items vJrwpWtwJgWr, while the second compartment contains the items hcsFMMfFFhFp. The only item type that appears in both compartments is lowercase p.
# The second rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL. The only item type that appears in both compartments is uppercase L.
# The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only common item type is uppercase P.
# The fourth rucksack's compartments only share item type v.
# The fifth rucksack's compartments only share item type t.
# The sixth rucksack's compartments only share item type s.
# To help prioritize item rearrangement, every item type can be converted to a priority:

# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.
# In the above example, the priority of the item type that appears in both compartments of each rucksack is 16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19 (s); the sum of these is 157.

# Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?

from itertools import zip_longest


def grouper(iterable, n, *, incomplete="fill", fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    if incomplete == "fill":
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == "strict":
        return zip(*args, strict=True)
    if incomplete == "ignore":
        return zip(*args)
    else:
        raise ValueError("Expected fill, strict, or ignore")


def character_range(start, stop, alphanumeric=False) -> list:
    """https://www.codingem.com/python-range-of-letters/"""
    char_list = list(chr(n) for n in range(ord(start), ord(stop) + 1))
    if alphanumeric:
        # Remove characters that are not letter or numbers
        for elem in list(char_list):
            if not elem.isalnum():
                char_list.remove(elem)
    return char_list


duplicate_item_total_priority = 0
elf_group_badge_total_priority = 0

character_priorty = {}
for char in enumerate(
    character_range("a", "z", alphanumeric=True)
    + character_range("A", "Z", alphanumeric=True)
):
    character_priorty[char[-1]] = char[0] + 1

with open(PUZZLE_INPUT) as f:
    rucksacks = [line.strip() for line in f.readlines()]

# Part 1 - Duplicate Item priority
for sack in rucksacks:
    items_per_compartment = int(len(sack) / 2)
    cmpt1 = sack[:items_per_compartment]
    cmpt2 = sack[items_per_compartment:]
    common_letter = next(iter(set(cmpt1).intersection(cmpt2)))
    duplicate_item_total_priority += character_priorty[common_letter]

# Part 2 - Duplicate Item priority
elf_group_size = 3
elf_groups = grouper(rucksacks, 3)
for group in elf_groups:
    common_letter = set(group[0]) & set(group[1]) & set(group[2])
    common_letter = next(iter(common_letter))
    elf_group_badge_total_priority += character_priorty[common_letter]


print("duplicate item total priority", duplicate_item_total_priority)
print("elf group badge total priority", elf_group_badge_total_priority)
