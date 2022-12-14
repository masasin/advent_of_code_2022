from textwrap import dedent

import numpy as np
import pytest

from solutions.day_14 import (
    parse_paths,
    find_bounds,
    draw_line,
    draw_path,
    parse_part_1,
    get_next_sand_point,
    solve,
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
        np.array([[4, 498], [6, 498], [6, 496]]),
        np.array([[4, 503], [4, 502], [9, 502], [9, 494]]),
    ]


@pytest.fixture
def offset_paths():
    return [
        np.array([[4, 4], [6, 4], [6, 2]]),
        np.array([[4, 9], [4, 8], [9, 8], [9, 0]]),
    ]


@pytest.fixture
def initial_state():
    return np.array(
        [
            [0, 0, 0, 0, 0, 0, -1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        ]
    )


@pytest.fixture
def initial_state_with_floor(initial_state):
    full_array = np.zeros((12, 1000))
    full_array[-1] = 1
    full_array[:-2, 494:504] = initial_state
    return full_array


@pytest.fixture
def blank_state(initial_state):
    return np.zeros_like(initial_state)


def test_parse_paths(text, paths):
    for actual, expected in zip(parse_paths(text), paths):
        assert (actual == expected).all()


def test_find_bounds(paths):
    expected = np.array([[4, 494], [9, 503]])
    assert (find_bounds(paths) == expected).all()


@pytest.mark.parametrize(
    ["endpoints", "end_state"],
    [
        (
            np.array([[4, 8], [4, 9]]),
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
        ),
        (
            np.array([[4, 8], [9, 8]]),
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                ]
            ),
        ),
        (
            np.array([[9, 8], [9, 0]]),
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                ]
            ),
        ),
    ],
)
def test_draw_line(blank_state, endpoints, end_state):
    draw_line(endpoints, blank_state)
    assert (blank_state == end_state).all()


@pytest.mark.parametrize(
    ["path", "end_state"],
    [
        (
            np.array([[4, 4], [6, 4], [6, 2]]),
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
        ),
        (
            np.array([[4, 9], [4, 8], [9, 8], [9, 0]]),
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                ]
            ),
        ),
    ],
)
def test_draw_path(blank_state, path, end_state):
    draw_path(path, blank_state)
    assert (blank_state == end_state).all()


def test_parse_part_1(text, initial_state):
    assert (parse_part_1(text) == initial_state).all()


@pytest.mark.parametrize(
    ["n_times", "expected"],
    [
        (1, np.array([8, 6])),
        (2, np.array([8, 5])),
        (5, np.array([8, 4])),
        (22, np.array([2, 6])),
        (24, np.array([8, 1])),
        (25, None),
    ],
)
def test_get_next_sand_point(initial_state, n_times, expected):
    for _ in range(n_times):
        next_point = get_next_sand_point(initial_state)
        if next_point is None:
            break
        initial_state[*next_point] = 2
    if expected is not None:
        assert (next_point == expected).all()
    else:
        assert next_point is expected


@pytest.mark.parametrize(
    ["state", "expected"],
    [
        (pytest.lazy_fixture("initial_state"), 24),
        (pytest.lazy_fixture("initial_state_with_floor"), 93),
    ],
)
def test_solve(state, expected):
    assert solve(state) == expected


def test_add_floor(initial_state, initial_state_with_floor):
    assert (add_floor(initial_state) == initial_state_with_floor).all()
