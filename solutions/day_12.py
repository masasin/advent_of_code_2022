from pathlib import Path
from string import ascii_lowercase

import numpy as np


Point = tuple[int, int]

DIRECTIONS = [
    np.array([-1, 0]),
    np.array([1, 0]),
    np.array([0, -1]),
    np.array([0, 1]),
]


def parse(text: str) -> tuple[np.ndarray, Point, Point]:
    target = ascii_lowercase + "SE"
    layout = np.array(
        [[target.index(letter) for letter in line] for line in text.splitlines()]
    )
    start = tuple(np.argwhere(layout == 26)[0])
    end = tuple(np.argwhere(layout == 27)[0])
    layout[start] = 0
    layout[end] = 25
    return layout, start, end


def reachable_from(layout: np.ndarray) -> np.ndarray:
    layout_buffer = np.ones(layout.shape + np.array([2, 2])) * np.nan
    layout_buffer[1:-1, 1:-1] = layout
    diffs = np.array(
        [
            np.diff(layout_buffer, axis=0)[:-1, 1:-1],  # up
            np.diff(layout_buffer[::-1], axis=0)[-2::-1, 1:-1],  # down
            np.diff(layout_buffer, axis=1)[1:-1, :-1],  # left
            np.diff(layout_buffer[:, ::-1], axis=1)[1:-1, -2::-1],  # right
        ]
    )
    return diffs <= 1


def distance_from(reachability: np.ndarray, point: Point) -> np.ndarray:
    distances = np.ones_like(reachability[0]) * np.inf
    distances[point] = 0
    points = {point}

    while points:
        point = points.pop()
        for direction, reachable in zip(DIRECTIONS, reachability[:, *point]):
            if reachable:
                new_point = tuple(point + direction)
                old_distance = distances[new_point]
                new_distance = distances[point] + 1
                if new_distance < old_distance:
                    points.add(new_point)
                distances[new_point] = min(old_distance, new_distance)

    return distances


def solve_part_1(distances: np.ndarray, start: Point) -> int:
    return distances[*start]


def solve_part_2(layout: np.ndarray, distances: np.ndarray) -> int:
    return distances[layout == 0].min()


def main():
    text = Path("../inputs/day_12.txt").read_text()
    layout, start, end = parse(text)
    reachability = reachable_from(layout)
    distances_from_end = distance_from(reachability, end)
    print(f"Part 1: {solve_part_1(distances_from_end, start):.0f}")
    print(f"Part 2: {solve_part_2(layout, distances_from_end):.0f}")


if __name__ == "__main__":
    main()
