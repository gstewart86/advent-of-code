#!/usr/bin/python
import os
import sys
import logging
from pprint import pformat, pprint

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


class ElfTroupe:
    def __init__(self):
        self.elves = []
        with open(PUZZLE_INPUT) as food_list_file:
            food_list = food_list_file.read()
        for elf in enumerate(food_list.split("\n\n")):
            elf_list = [int(x) for x in elf[1].split("\n")]
            elf_cals = sum(elf_list)
            self.elves.append((elf[0], elf_cals, elf_list))
        self.elves = sorted(self.elves, key=lambda x: x[1], reverse=True)
        self.highest_elves = sum([x[1] for x in self.elves[0:3]])


elves = ElfTroupe()
# pprint(vars(print(", ".join("%s: %s" % item for item in vars(elves).items()))))
pprint(elves.elves[0:3])
print(elves.highest_elves)
