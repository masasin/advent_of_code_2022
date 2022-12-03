from pathlib import Path
from typing import Generator, Iterable


def parse(text: str) -> Generator[int, None, None]:
    for elf in text.split("\n\n"):
        yield sum(map(int, elf.splitlines()))


def solve_part_1(data: Iterable[int]) -> int:
    return max(data)


def solve_part_2(data: Iterable[int]) -> int:
    return sum(sorted(data)[-3:])


def main():
    text = Path("../inputs/day_01.txt").read_text()
    data = list(parse(text))
    print(f"Part 1: {solve_part_1(data)}")
    print(f"Part 2: {solve_part_2(data)}")


if __name__ == "__main__":
    main()
