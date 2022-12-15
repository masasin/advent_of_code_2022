import itertools as it
from pathlib import Path
from typing import Generator


Point = complex
Points = tuple[Point, Point]
RockPath = list[Point]
RockPaths = Generator[RockPath, None, None]
State = set[Point]


SAND_START_POINT = 500 + 0j


def parse_paths(text: str) -> RockPaths:
    for path_str in text.splitlines():
        yield [
            int((p := point.split(","))[0]) + int(p[1]) * 1j
            for point in path_str.split(" -> ")
        ]


def add_line(point_1: Point, point_2: Point, state: State) -> None:
    x1, y1 = int(point_1.real), int(point_1.imag)
    x2, y2 = int(point_2.real), int(point_2.imag)
    if x1 == x2:
        y_start, y_end = sorted([y1, y2])
        for y in range(y_start, y_end + 1):
            state.add(x1 + y * 1j)
    else:
        x_start, x_end = sorted([x1, x2])
        for x in range(x_start, x_end + 1):
            state.add(x + y1 * 1j)


def add_path(path, state) -> None:
    for point_1, point_2 in zip(path, path[1:]):
        add_line(point_1, point_2, state)


def get_max_depth(state: State) -> int:
    return int(max(point.imag for point in state))


def parse_part_1(text: str) -> State:
    state = set()
    for path in parse_paths(text):
        add_path(path, state)
    return state


def get_next_sand_point(state: State, y_max: int) -> Point | None:
    position = SAND_START_POINT
    while position.imag < y_max and SAND_START_POINT not in state:
        for movement in [1j, -1 + 1j, 1 + 1j]:
            if position + movement not in state:
                position += movement
                break
        else:
            return position


def add_floor(state: State, y_max: int) -> None:
    sand_start_x = int(SAND_START_POINT.real)
    add_line(
        sand_start_x - y_max + y_max * 1j,
        sand_start_x + y_max + y_max * 1j,
        state,
    )


def solve(state: State, y_offset=0) -> int:
    y_max = get_max_depth(state) + y_offset
    if y_offset:
        add_floor(state, y_max)
    for i in it.count():
        next_point = get_next_sand_point(state, y_max)
        if next_point is None:
            return i
        state.add(next_point)


def main():
    text = Path("../inputs/day_14.txt").read_text()
    state = parse_part_1(text)
    print(f"Part 1: {solve(state.copy(), y_offset=0)}")
    print(f"Part 2: {solve(state.copy(), y_offset=2)}")


if __name__ == "__main__":
    main()
