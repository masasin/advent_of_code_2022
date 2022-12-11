import itertools as it
from pathlib import Path
from typing import Generator, Iterable


class Sim:
    def __init__(self, start: int = 20, stride: int = 40):
        self.sprite_position: int = 1
        self.interesting_numbers = it.count(start=start, step=stride)
        self.pixel_position = 0

    def run_part_1(self, values: Iterable[int]) -> Generator[int, None, None]:
        next_interesting = next(self.interesting_numbers)
        for i, value in enumerate(values, start=1):
            if i == next_interesting:
                yield i * self.sprite_position
                next_interesting = next(self.interesting_numbers)
            self.step(value)

    def run_part_2(self, values: Iterable[int]) -> Generator[str, None, None]:
        for value in values:
            line_end = "\n" if self.pixel_position == 39 else ""
            if abs(self.pixel_position - self.sprite_position) <= 1:
                yield "#" + line_end
            else:
                yield "." + line_end
            self.step(value)

    def step(self, value):
        self.sprite_position += value
        self.pixel_position = (self.pixel_position + 1) % 40


def parse(text: str) -> Generator[int, None, None]:
    for line in text.splitlines():
        match line.split():
            case ["noop"]:
                yield 0
            case ["addx", number]:
                yield 0
                yield int(number)


def solve_part_1(data: Iterable[int]) -> int:
    sim = Sim()
    return sum(sim.run_part_1(data))


def solve_part_2(data: Iterable[int]) -> str:
    sim = Sim()
    return "\n" + "".join(sim.run_part_2(data))


def main():
    text = Path("../inputs/day_10.txt").read_text()
    data = list(parse(text))
    print(f"Part 1: {solve_part_1(data)}")
    print(f"Part 2: {solve_part_2(data)}")


if __name__ == "__main__":
    main()
