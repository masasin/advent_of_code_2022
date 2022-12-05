from copy import deepcopy
import functools as ft
from pathlib import Path
import re
from typing import Generator, Iterable, NamedTuple

import simplematch as sm


class Move(NamedTuple):
    amount: int
    start: int
    end: int


Configuration = list[list[str]]


def parse_start_config(text: str) -> Configuration:
    stacks_line, *box_lines = reversed(text.splitlines())
    indices = [stacks_line.index(i) for i in re.findall(r"\d", stacks_line)]
    return [
        [
            box
            for line in box_lines
            if index <= len(line.rstrip()) and (box := line[index]) != " "
        ]
        for index in indices
    ]


def parse_instructions(text: str) -> Generator[Move, None, None]:
    pattern = "move {amount:int} from {start:int} to {end:int}"
    for line in text.splitlines():
        yield Move(**sm.match(pattern, line))


def parse(text: str) -> tuple[Configuration, list[Move]]:
    start_config_str, instructions_str = text.split("\n\n")
    start_config = parse_start_config(start_config_str)
    instructions = list(parse_instructions(instructions_str))
    return start_config, instructions


def apply_move(config: Configuration, move: Move) -> Configuration:
    config = deepcopy(config)
    for _ in range(move.amount):
        config[move.end - 1].append(config[move.start - 1].pop())
    return config


def top_of_stacks(config: Configuration) -> str:
    return "".join([stack[-1] for stack in config])


def solve_part_1(config: Configuration, instructions: Iterable[Move]) -> str:
    for move in instructions:
        config = apply_move(config, move)
    return top_of_stacks(config)


def solve_part_2(config: Configuration, instructions: Iterable[Move]) -> str:
    ...


def main():
    text = Path("../inputs/day_05.txt").read_text()
    start_config, instructions = parse(text)
    print(f"Part 1: {solve_part_1(start_config, instructions)}")
    print(f"Part 2: {solve_part_2(start_config, instructions)}")


if __name__ == "__main__":
    main()
