import itertools as it
from pathlib import Path
from typing import Generator, Iterable

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from nptyping import NDArray, Shape, Int

Point = NDArray[Shape["[x, y]"], Int]
Points = NDArray[Shape["Point, Point"], Int]
RockPath = NDArray[Shape["*, Point"], Int]
RockPaths = Generator[RockPath, None, None]
State = NDArray[Shape["*, *"], Int]


SAND_START_COL = 500


def parse_paths(text: str) -> RockPaths:
    for path_str in text.splitlines():
        yield np.array(
            [
                [int(v) for v in point.split(",")[::-1]]
                for point in path_str.split(" -> ")
            ]
        )


def find_bounds(paths: RockPaths) -> Points:
    points = np.vstack(paths)
    # noinspection PyArgumentList
    return np.array([points.min(axis=0), points.max(axis=0)])


def draw_line(endpoints: Points, state: State) -> None:
    endpoints = endpoints.copy()
    endpoints.sort(axis=0)
    ((row_start, col_start), (row_end, col_end)) = endpoints
    state[row_start : row_end + 1, col_start : col_end + 1] = 1


def draw_path(path, state) -> None:
    for endpoints in sliding_window_view(path, window_shape=[2, 2]):
        draw_line(endpoints[0], state)


def parse_part_1(text: str) -> State:
    paths = list(parse_paths(text))
    min_point, max_point = find_bounds(paths)
    size = np.array([max_point[0], max_point[1] - min_point[1]]) + 1
    state = np.zeros(size)

    col_offset = min_point[1]
    state[0, SAND_START_COL - col_offset] = -1

    for path in paths:
        path[:, 1] -= col_offset
        draw_path(path, state)

    return state


def get_next_sand_point(state: State) -> Point | None:
    n_rows, n_cols = state.shape
    prev_point: Point = np.argwhere(state == -1)[0]
    while True:
        for next_movement in [0, -1, 1]:
            next_point = prev_point + [1, next_movement]
            next_row, next_col = next_point
            if not (0 <= next_col < n_cols):
                return None
            if state[*next_point] == 0:
                prev_point = next_point
                break
        else:
            next_point = prev_point
            break
    if state[*next_point] > 0:
        return None
    return next_point


def solve(state: State) -> int:
    for i in it.count():
        next_point = get_next_sand_point(state)
        if next_point is None:
            return i
        state[*next_point] = 2


def parse_part_2(text: str) -> Generator:
    ...


def solve_part_2(data: Iterable):
    ...


def main():
    text = Path("../inputs/day_14.txt").read_text()
    print(f"Part 1: {solve(parse_part_1(text))}")
    print(f"Part 2: {solve(parse_part_2(text))}")


if __name__ == "__main__":
    main()
