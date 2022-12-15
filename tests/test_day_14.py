from textwrap import dedent

import pytest

from solutions.day_14 import (
    parse_paths,
    add_line,
    add_path,
    parse,
    get_next_sand_point,
    solve,
    get_max_depth,
    add_floor,
)


@pytest.fixture
def text():
    return dedent(
        """\
        498,4 -> 498,6 -> 496,6
        503,4 -> 502,4 -> 502,9 -> 494,9
        """
    )


@pytest.fixture
def paths():
    return [
        [498 + 4j, 498 + 6j, 496 + 6j],
        [503 + 4j, 502 + 4j, 502 + 9j, 494 + 9j],
    ]


@pytest.fixture
def initial_state():
    return {
        498 + 4j,
        498 + 5j,
        498 + 6j,
        497 + 6j,
        496 + 6j,
        503 + 4j,
        502 + 4j,
        502 + 5j,
        502 + 6j,
        502 + 7j,
        502 + 8j,
        502 + 9j,
        501 + 9j,
        500 + 9j,
        499 + 9j,
        498 + 9j,
        497 + 9j,
        496 + 9j,
        495 + 9j,
        494 + 9j,
    }


@pytest.fixture
def initial_state_with_floor():
    return {
        498 + 4j,
        498 + 5j,
        498 + 6j,
        497 + 6j,
        496 + 6j,
        503 + 4j,
        502 + 4j,
        502 + 5j,
        502 + 6j,
        502 + 7j,
        502 + 8j,
        502 + 9j,
        501 + 9j,
        500 + 9j,
        499 + 9j,
        498 + 9j,
        497 + 9j,
        496 + 9j,
        495 + 9j,
        494 + 9j,
        489 + 11j,
        490 + 11j,
        491 + 11j,
        492 + 11j,
        493 + 11j,
        494 + 11j,
        495 + 11j,
        496 + 11j,
        497 + 11j,
        498 + 11j,
        499 + 11j,
        500 + 11j,
        501 + 11j,
        502 + 11j,
        503 + 11j,
        504 + 11j,
        505 + 11j,
        506 + 11j,
        507 + 11j,
        508 + 11j,
        509 + 11j,
        510 + 11j,
        511 + 11j,
    }


def test_parse_paths(text, paths):
    for actual, expected in zip(parse_paths(text), paths):
        assert actual == expected


@pytest.mark.parametrize(
    ["point_1", "point_2", "end_state"],
    [
        (
            498 + 4j,
            498 + 5j,
            {498 + 4j, 498 + 5j},
        ),
        (
            502 + 4j,
            502 + 9j,
            {
                502 + 4j,
                502 + 5j,
                502 + 6j,
                502 + 7j,
                502 + 8j,
                502 + 9j,
            },
        ),
        (
            502 + 9j,
            494 + 9j,
            {
                502 + 9j,
                501 + 9j,
                500 + 9j,
                499 + 9j,
                498 + 9j,
                497 + 9j,
                496 + 9j,
                495 + 9j,
                494 + 9j,
            },
        ),
    ],
)
def test_add_line(point_1, point_2, end_state):
    state = set()
    add_line(point_1, point_2, state)  # noqa
    assert state == end_state


@pytest.mark.parametrize(
    ["path", "end_state"],
    [
        (
            [498 + 4j, 498 + 6j, 496 + 6j],
            {
                498 + 4j,
                498 + 5j,
                498 + 6j,
                497 + 6j,
                496 + 6j,
            },
        ),
        (
            [503 + 4j, 502 + 4j, 502 + 9j, 494 + 9j],
            {
                503 + 4j,
                502 + 4j,
                502 + 5j,
                502 + 6j,
                502 + 7j,
                502 + 8j,
                502 + 9j,
                501 + 9j,
                500 + 9j,
                499 + 9j,
                498 + 9j,
                497 + 9j,
                496 + 9j,
                495 + 9j,
                494 + 9j,
            },
        ),
    ],
)
def test_add_path(path, end_state):
    state = set()
    add_path(path, state)
    assert state == end_state


def test_parse(text, initial_state):
    assert parse(text) == initial_state


@pytest.mark.parametrize(
    ["offset", "n_times", "expected"],
    [
        (0, 1, 500 + 8j),
        (0, 2, 499 + 8j),
        (0, 5, 498 + 8j),
        (0, 22, 500 + 2j),
        (0, 24, 495 + 8j),
        (0, 25, None),
        (2, 25, 493 + 10j),
    ],
)
def test_get_next_sand_point(
    initial_state, initial_state_with_floor, offset, n_times, expected
):
    state = initial_state_with_floor if offset else initial_state
    for i in range(n_times):
        next_point = get_next_sand_point(state, 9 + offset)
        state.add(next_point)
    assert next_point == expected  # noqa


def test_solve_part_1(initial_state):
    assert solve(initial_state) == 24


def test_solve_part_2(initial_state):
    assert solve(initial_state, y_offset=2) == 93


def test_get_max_depth(initial_state):
    assert get_max_depth(initial_state) == 9


def test_add_floor(initial_state, initial_state_with_floor):
    add_floor(initial_state, 11)
    assert initial_state == initial_state_with_floor
