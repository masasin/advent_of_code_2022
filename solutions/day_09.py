from pathlib import Path
from typing import Generator, Iterable, NamedTuple

import numpy as np


directions = {
    "R": np.array([1, 0]),
    "L": np.array([-1, 0]),
    "U": np.array([0, 1]),
    "D": np.array([0, -1]),
}


class Sim:
    def __init__(self, length: int):
        self.positions = np.zeros((length, 2))
        self.tail_visited = {(0, 0)}

    def step(self, direction: np.ndarray):
        self.positions[0] += direction
        for index, position in enumerate(self.positions[1:], start=1):
            position += self._move_next(index)
        self.tail_visited.add(tuple(self.positions[-1]))

    def _move_next(self, index: int) -> np.ndarray:
        distance = self.positions[index - 1] - self.positions[index]
        if (abs(distance) <= 1).all():
            return np.array([0, 0])
        distance[abs(distance) == 2] //= 2
        return distance


def parse(text: str) -> Generator[np.ndarray, None, None]:
    for line in text.splitlines():
        direction, count = line.split()
        yield from (directions[direction] for _ in range(int(count)))


def solve_part_1(data: list[np.ndarray]) -> int:
    sim = Sim(length=2)
    for direction in data:
        sim.step(direction)
    return len(sim.tail_visited)


def solve_part_2(data: list[np.ndarray]) -> int:
    sim = Sim(length=10)
    for direction in data:
        sim.step(direction)
    return len(sim.tail_visited)


def main():
    text = Path("../inputs/day_09.txt").read_text()
    data = list(parse(text))
    print(f"Part 1: {solve_part_1(data)}")
    print(f"Part 2: {solve_part_2(data)}")


if __name__ == "__main__":
    main()
