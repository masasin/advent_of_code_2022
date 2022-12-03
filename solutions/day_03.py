import functools as ft
from string import ascii_letters
from pathlib import Path
from typing import Generator


def letter_priority(letter: str) -> int:
    return ascii_letters.index(letter) + 1


def split_contents(contents: str) -> tuple[str, str]:
    split_point = len(contents) // 2
    return contents[:split_point], contents[split_point:]


def common_items(*items: str) -> str:
    return ft.reduce(set.intersection, (set(item) for item in items)).pop()  # noqa


def parse_part_1(text: str) -> Generator:
    for rucksack in text.splitlines():
        yield letter_priority(common_items(*split_contents(rucksack)))


def parse_part_2(text: str) -> Generator:
    lines = text.splitlines()
    for rucksacks in zip(*[iter(lines)] * 3):
        yield letter_priority(common_items(*rucksacks))


def main():
    text = Path("../inputs/day_03.txt").read_text()
    print(f"Part 1: {sum(parse_part_1(text))}")
    print(f"Part 2: {sum(parse_part_2(text))}")


if __name__ == "__main__":
    main()
