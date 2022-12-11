from pathlib import Path
from typing import Generator, Iterable


def parse_part_1(text: str) -> Generator:
    ...


def solve_part_1(data: Iterable):
    ...


def parse_part_2(text: str) -> Generator:
    ...


def solve_part_2(data: Iterable):
    ...


def main():
    text = Path("../inputs/day_11.txt").read_text()
    print(f"Part 1: {solve_part_1(parse_part_1(text))}")
    print(f"Part 2: {solve_part_2(parse_part_2(text))}")


if __name__ == "__main__":
    main()
