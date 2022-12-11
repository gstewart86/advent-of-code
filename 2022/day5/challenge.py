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


# --- Day 5: Supply Stacks ---
# The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

# The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.

# The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

# They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:

#     [D]
# [N] [C]
# [Z] [M] [P]
#  1   2   3

# move 1 from 2 to 1
# move 3 from 1 to 3
# move 2 from 2 to 1
# move 1 from 1 to 2
# In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.

# Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

# [D]
# [N] [C]
# [Z] [M] [P]
#  1   2   3
# In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

#         [Z]
#         [N]
#     [C] [D]
#     [M] [P]
#  1   2   3
# Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:

#         [Z]
#         [N]
# [M]     [D]
# [C]     [P]
#  1   2   3
# Finally, one crate is moved from stack 1 to stack 2:

#         [Z]
#         [N]
#         [D]
# [C] [M] [P]
#  1   2   3
# The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

# After the rearrangement procedure completes, what crate ends up on top of each stack?

from copy import deepcopy


ORIGINAL_CRATE_STACKS = {
    1: ["B", "P", "N", "Q", "H", "D", "R", "T"],
    2: ["W", "G", "B", "J", "T", "V"],
    3: ["N", "R", "H", "D", "S", "V", "M", "Q"],
    4: ["P", "Z", "N", "M", "C"],
    5: ["D", "Z", "B"],
    6: ["V", "C", "W", "Z"],
    7: ["G", "Z", "N", "C", "V", "Q", "L", "S"],
    8: ["L", "G", "J", "M", "D", "N", "V"],
    9: ["T", "P", "M", "F", "Z", "C", "G"],
}


def parse_input():
    with open(PUZZLE_INPUT, "r") as f:
        lines = f.readlines()
    return lines


def parse_directions(input_diagram):

    # find empty line
    stack_lines = []
    stack = {}
    moves = []
    for _, line in enumerate(input_diagram):
        if line.isspace():
            stack_lines = input_diagram[: _ - 1]  # get all lines before empty line
            break
    moves = input_diagram[_ + 1 :]  # get all lines after empty line
    logger.info("stack defined\n" + pformat(stack_lines))

    # sanitize stack
    # for _, line in enumerate(stack_lines):
    #     stack_lines[_] = list(line.replace("\n", "").replace("[", "").replace("]", ""))
    # logger.debug(
    #     "stack lines sanitized\n" + pformat(stack_lines, compact=True, width=130)
    # )

    # # initialize stack dict
    # for i in range(0, len(stack_lines) + 1):
    #     stack[i] = [i[0] for i in stack_lines]
    # logger.debug("stack dict parsed\n" + pformat(stack))
    parsed_moves = []
    for move in moves:
        parsed_moves.append(
            [
                int(x)
                for x in (
                    move.replace("move", "")
                    .replace("from", "")
                    .replace("to", "")
                    .replace("\n", "")
                    .split("  ")
                )
            ]
        )
    logger.info("moves parsed:" + pformat(len(parsed_moves)))
    logger.debug("moves parsed:" + pformat(parsed_moves))

    return stack, parsed_moves


existing_stack, moves = parse_directions(parse_input())


def execute_moves(stacks, moves, simultaneous=True):
    tmp_stacks = deepcopy(stacks)
    logger.debug("starting stacks\n:" + pformat(tmp_stacks))
    for move in moves:
        number_of_crates = move[0]
        src_stack = move[1]
        dst_stack = move[2]
        logger.debug(f"moving {number_of_crates} from {src_stack} to {dst_stack}")
        logger.debug(
            "before:\n"
            + pformat(
                {
                    f"src_{src_stack}": tmp_stacks[src_stack],
                    f"dst_{dst_stack}": tmp_stacks[dst_stack],
                }
            )
        )
        if simultaneous:
            crates = []
            crates = tmp_stacks[src_stack][-number_of_crates:]
            tmp_stacks[src_stack] = tmp_stacks[src_stack][:-number_of_crates]
            tmp_stacks[dst_stack] += crates
        else:
            for i in range(0, number_of_crates):
                logger.debug(tmp_stacks[src_stack])
                tmp_stacks[dst_stack].append(tmp_stacks[src_stack].pop())
        logger.debug(
            "after:\n"
            + pformat(
                {
                    f"src_{src_stack}": tmp_stacks[src_stack],
                    f"dst_{dst_stack}": tmp_stacks[dst_stack],
                }
            )
        )
    return tmp_stacks


# crate_stacks = execute_moves(ORIGINAL_CRATE_STACKS, moves, simultaneous=False)
# top_crates = []
# for x, y in crate_stacks.items():
#     top_crates.append(y[-1])
# logger.info("one-at-a-time moves: top crates in each stack:" + "".join(top_crates))


# --- Part Two ---
# As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

# Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

# The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

# Again considering the example above, the crates begin in the same configuration:

#     [D]
# [N] [C]
# [Z] [M] [P]
#  1   2   3
# Moving a single crate from stack 2 to stack 1 behaves the same as before:

# [D]
# [N] [C]
# [Z] [M] [P]
#  1   2   3
# However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same order, resulting in this new configuration:

#         [D]
#         [N]
#     [C] [Z]
#     [M] [P]
#  1   2   3
# Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

#         [D]
#         [N]
# [C]     [Z]
# [M]     [P]
#  1   2   3
# Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

#         [D]
#         [N]
#         [Z]
# [M] [C] [P]
#  1   2   3
# In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

# Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each stack?

crate_stacks = execute_moves(ORIGINAL_CRATE_STACKS, moves)
logger.debug("final stacks\n:" + pformat(crate_stacks))
top_crates = []
for stack in crate_stacks.values():
    top_crates.append(stack[-1])
logger.info(
    "simultaneous moves: top crates in each stack:" + pformat("".join(top_crates))
)
