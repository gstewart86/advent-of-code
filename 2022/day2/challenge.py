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


from dataclasses import dataclass


@dataclass
class RpsResult:
    condition: str
    points: int


@dataclass
class RpsOption:
    type: str
    opposite: str
    value: int = 0


RPS_ROUND = {"win": 6, "draw": 3, "loss": 0}


class Tournament:
    RPS = {
        "A": RpsOption("rock", "Y"),
        "B": RpsOption("paper", "X"),
        "C": RpsOption("scissors", "Z"),
        "X": RpsOption("rock", "Y", 1),
        "Y": RpsOption("paper", "A", 2),
        "Z": RpsOption("scissors", "C", 3),
    }

    def __init__(self):
        with open(PUZZLE_INPUT) as f:
            self.rounds = [line.strip().split(" ") for line in f.readlines()]

        self.total_points = 0
        for players in self.rounds:
            self.total_points += self.round(players)

    def rock_paper_scissors(self, player1_choice: str, player2_choice: str):
        if player1_choice == "rock":
            match player2_choice:
                case "rock":
                    return "draw"
                case "paper":
                    return "loss"
                case "scissors":
                    return "win"
        if player1_choice == "paper":
            match player2_choice:
                case "rock":
                    return "win"
                case "paper":
                    return "draw"
                case "scissors":
                    return "loss"
        if player1_choice == "scissors":
            match player2_choice:
                case "rock":
                    return "loss"
                case "paper":
                    return "win"
                case "scissors":
                    return "draw"

    def round(self, plays: list) -> int:
        total = 0
        total += self.RPS[plays[-1]].value
        total += RPS_ROUND[
            self.rock_paper_scissors(self.RPS[plays[-1]].type, self.RPS[plays[0]].type)
        ]
        return total


tourney = Tournament()
print(tourney.total_points)
print(tourney.rock_paper_scissors("rock", "scissors"))


# ==============================================================================
class RockPaperScissors:
    loses_against = {
        "rock": ["scissors"],
        "paper": ["rock"],
        "scissors": ["paper"],
    }
    wins_against = {
        "rock": ["paper"],
        "paper": ["scissors"],
        "scissors": ["rock"],
    }
    guide_direction_1 = {"X": "rock", "Y": "paper", "Z": "scissors"}
    guide_direction_2 = {"X": "loss", "Y": "draw", "Z": "win"}
    choice_map = {"A": "rock", "B": "paper", "C": "scissors"}
    choice_values = {"rock": 1, "paper": 2, "scissors": 3}
    result_values = {"win": 6, "draw": 3, "loss": 0}

    total_points = 0

    def play(self, player1_choice, player2_choice):
        if player2_choice in self.loses_against[player1_choice]:
            return f"{player1_choice} win"
        if player1_choice in self.loses_against[player2_choice]:
            return f"{player1_choice} loss"
        return "draw"

    def __init__(self):
        with open(PUZZLE_INPUT) as f:
            self.rounds = [line.strip().split(" ") for line in f.readlines()]

        for round in self.rounds:
            player1_choice = self.choice_map[round[0]]
            match self.guide_direction_2[round[1]]:
                case "draw":
                    player2_choice = player1_choice
                case "loss":
                    player2_choice = self.loses_against[player1_choice]
                case "win":
                    player2_choice = self.wins_against[player1_choice]

            if isinstance(player2_choice, (list, set)):
                player2_choice = next(
                    iter(player2_choice)
                )  # resolve first item from returned set
            round_result = self.play(player1_choice, player2_choice)
            round.append(round_result)
            round_points = (
                self.choice_values[player2_choice]
                + self.result_values[self.guide_direction_2[round[1]]]
            )
            round.append(round_points)
            self.total_points += round_points


rps = RockPaperScissors()
pprint(rps.total_points)
