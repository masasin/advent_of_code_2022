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


def parse(text: str) -> Generator[tuple[Range, Range], None, None]:
    yield from (parse_line(line) for line in text.splitlines())


def solve_part_1(ranges: Iterable[tuple[Range, Range]]) -> int:
    return sum(ranges_completely_overlap(left, right) for left, right in ranges)


def solve_part_2(ranges: Iterable[tuple[Range, Range]]) -> int:
    return sum(ranges_overlap(left, right) for left, right in ranges)


def main():
    text = Path("../inputs/day_04.txt").read_text()
    ranges = list(parse(text))
    print(f"Part 1: {solve_part_1(ranges)}")
    print(f"Part 2: {solve_part_2(ranges)}")


if __name__ == "__main__":
    main()
