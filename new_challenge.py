import os
from datetime import date
from argparse import ArgumentParser
import requests
from bs4 import BeautifulSoup

CHALLENGE_FILENAME = "challenge.py"
INPUT_FILENAME = "puzzle_input.txt"

parser = ArgumentParser()
parser.add_argument("day", type=int, help="The day of the challenge")
args = parser.parse_args()

THIS_YEAR = date.today().year
ADVENT_OF_CODE_DAY_URL = f"https://adventofcode.com/{THIS_YEAR}/day/{args.day}"
if args.day:
    DAY_DIR = f"day{args.day}"


def parse_html(url):
    """Parse the HTML page to extract the challenge description and input/output examples"""
    print(f"Getting {url}")
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    # Extract the challenge description
    description = soup.find("article", class_="day-desc").extract().text

    # Find the input
    input = requests.get(url + "/input").text

    return description, input


# Parse the HTML page to extract the challenge description and input/output examples
description, puzzle_input = parse_html(ADVENT_OF_CODE_DAY_URL)

# Check to see if the directory for the year exists
if not os.path.exists(f"{THIS_YEAR}"):
    os.mkdir(f"{THIS_YEAR}")

# Check to see if the directory for the day exists
if not os.path.exists(f"{THIS_YEAR}/{DAY_DIR}"):
    os.mkdir(f"{THIS_YEAR}/{DAY_DIR}")
else:
    print("Day already exists!")

# Create the Python file
challenge_path = f"{THIS_YEAR}/{DAY_DIR}/{CHALLENGE_FILENAME}"
if not os.path.exists(challenge_path):
    print("writing challenge file: ", challenge_path)
    with open(challenge_path, "w") as f:
        # Write the challenge description to the file
        f.write(f'"""\n{description}"""')

        # Define a logger
        f.write(
            """
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
    """
        )
else:
    print("Challenge file already exists!")

puzzle_input_path = f"{THIS_YEAR}/{DAY_DIR}/{INPUT_FILENAME}"
if not os.path.exists(puzzle_input_path):
    print("writing input file: ", puzzle_input_path)
    with open(puzzle_input_path, "w") as f:
        # Write puzzle input to file
        f.write(puzzle_input)
else:
    print("Input file already exists!")
