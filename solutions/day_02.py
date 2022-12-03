from pathlib import Path
from typing import Generator


import numpy as np


SHAPE_SCORES = np.array(
    [
        [1, 1, 1],
        [2, 2, 2],
        [3, 3, 3],
    ]
)

OUTCOMES = np.array(
    [
        [0, -1, 1],
        [1, 0, -1],
        [-1, 1, 0],
    ]
)

OUTCOME_SCORES = (OUTCOMES + 1) * 3
TOTAL_SCORES = SHAPE_SCORES + OUTCOME_SCORES

REVERSE = np.array(
    [
        [2, 0, 1],
        [0, 1, 2],
        [1, 2, 0],
    ]
)

MOVE = "ABC"
COMPLEMENT = "XYZ"


def pair_score(opponent: str, player: str) -> int:
    player_index = MOVE.index(player)
    opponent_index = MOVE.index(opponent)
    return TOTAL_SCORES[player_index, opponent_index]


def parse_part_1(text: str) -> Generator[int, None, None]:
    for line in text.splitlines():
        opponent, player = line.split()
        yield pair_score(opponent, MOVE[COMPLEMENT.index(player)])


def reverse_solve(opponent: str, outcome: str) -> str:
    opponent_index = MOVE.index(opponent)
    outcome_index = COMPLEMENT.index(outcome)
    return MOVE[REVERSE[opponent_index, outcome_index]]


def parse_part_2(text: str) -> Generator[int, None, None]:
    for line in text.splitlines():
        opponent, outcome = line.split()
        player = reverse_solve(opponent, outcome)
        yield pair_score(opponent, player)


def main():
    text = Path("../inputs/day_02.txt").read_text()
    print(f"Part 1: {sum(parse_part_1(text))}")
    print(f"Part 2: {sum(parse_part_2(text))}")


if __name__ == "__main__":
    main()
