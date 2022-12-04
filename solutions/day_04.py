from pathlib import Path
from typing import Generator, Iterable, NamedTuple


class Range(NamedTuple):
    start: int
    end: int


def parse_line(line: str) -> tuple[Range, Range]:
    left, right = line.split(",")
    return Range(*map(int, left.split("-"))), Range(*map(int, right.split("-")))


def _overlap_from_right(left: Range, right: Range) -> bool:
    return left.start <= right.end and right.start <= left.end


def ranges_overlap(left: Range, right: Range) -> bool:
    return _overlap_from_right(left, right) or _overlap_from_right(right, left)


def _right_in_left(left: Range, right: Range) -> bool:
    return left.start <= right.start and right.end <= left.end


def ranges_completely_overlap(left: Range, right: Range) -> bool:
    return _right_in_left(left, right) or _right_in_left(right, left)


def parse_part_1(text: str) -> Generator[bool, None, None]:
    yield from (
        ranges_completely_overlap(*parse_line(line)) for line in text.splitlines()
    )


def parse_part_2(text: str) -> Generator[bool, None, None]:
    yield from (ranges_overlap(*parse_line(line)) for line in text.splitlines())


def main():
    text = Path("../inputs/day_04.txt").read_text()
    print(f"Part 1: {sum(parse_part_1(text))}")
    print(f"Part 2: {sum(parse_part_2(text))}")


if __name__ == "__main__":
    main()
