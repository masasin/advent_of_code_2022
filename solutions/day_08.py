from pathlib import Path
from typing import Generator, Iterable


import numpy as np


HeightGrid = np.ndarray[int]


def parse(text: str) -> HeightGrid:
    return np.array([list(line) for line in text.splitlines()], dtype=int)


def visibility(row: int, col: int, grid: HeightGrid) -> int:
    height = grid[row, col]
    directions: list[np.ndarray] = [
        grid[row, :col],  # left
        grid[row, col + 1 :],  # right
        grid[:row, col],  # up
        grid[row + 1 :, col],  # down
    ]
    return sum((direction < height).all() for direction in directions)


def solve_part_1(grid: HeightGrid) -> int:
    n_rows, n_cols = grid.shape
    return np.array(
        [
            [bool(visibility(row, col, grid)) for col in range(n_cols)]
            for row in range(n_rows)
        ]
    ).sum()


def scenic_score(row: int, col: int, grid: HeightGrid) -> int:
    height = grid[row, col]
    directions: list[np.ndarray] = [
        grid[row, :col][::-1],  # left
        grid[row, col + 1 :],  # right
        grid[:row, col][::-1],  # up
        grid[row + 1 :, col],  # down
    ]
    return int(
        np.prod(
            [
                distances[0, 0] + 1
                if (distances := np.argwhere(direction >= height)).size > 0
                else len(direction)
                for direction in directions
            ]
        )
    )


def solve_part_2(grid: HeightGrid):
    n_rows, n_cols = grid.shape
    return np.array(
        [
            [scenic_score(row, col, grid) for col in range(n_cols)]
            for row in range(n_rows)
        ]
    ).max()


def main():
    text = Path("../inputs/day_08.txt").read_text()
    grid = parse(text)
    print(f"Part 1: {solve_part_1(grid)}")
    print(f"Part 2: {solve_part_2(grid)}")


if __name__ == "__main__":
    main()
