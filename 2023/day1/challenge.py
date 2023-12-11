import re
from loguru import logger

example = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

def solve():
    total = 0
    for line in example:
        logger.debug(f"line: {line}")
        c = 0
        line_ints = re.findall(r'\d+', line)
        line_ints = [int(i) for i in line_ints]
        logger.debug(f"line_ints: {line_ints}")

        first_int = line_ints[0]
        last_int = line_ints[-1]
        logger.debug(f"ints: {first_int}, {last_int}")

        c = first_int * 10 + last_int
        logger.debug(f"c: {c}")

    total += c
