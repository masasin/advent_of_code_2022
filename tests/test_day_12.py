from textwrap import dedent

import numpy as np
import pytest

from solutions.day_12 import (
    parse_part_1,
    movement_options,
    reachable_from,
    distance_from,
    solve_part_1,
    solve_part_2,
)


@pytest.fixture
def text():
    return dedent(
        """\
        Sabqponm
        abcryxxl
        accszExk
        acctuvwj
        abdefghi
        """
    )


@pytest.fixture
def data():
    return (
        np.array(
            [
                [0, 0, 1, 16, 15, 14, 13, 12],
                [0, 1, 2, 17, 24, 23, 23, 11],
                [0, 2, 2, 18, 25, 25, 23, 10],
                [0, 2, 2, 19, 20, 21, 22, 9],
                [0, 1, 3, 4, 5, 6, 7, 8],
            ]
        ),
        (0, 0),
        (2, 5),
    )


@pytest.fixture
def options():
    return np.array(
        [
            [  # up
                [False, False, False, False, False, False, False, False],
                [True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True],
                [True, True, True, True, False, False, True, True],
                [True, True, True, False, False, False, False, True],
            ],
            [  # down
                [True, True, True, True, False, False, False, True],
                [True, True, True, True, True, False, True, True],
                [True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True],
                [False, False, False, False, False, False, False, False],
            ],
            [  # left
                [False, True, True, True, True, True, True, True],
                [False, True, True, True, True, True, True, False],
                [False, True, True, True, True, True, False, False],
                [False, True, True, True, True, True, True, False],
                [False, True, True, True, True, True, True, True],
            ],
            [  # right
                [True, True, False, True, True, True, True, False],
                [True, True, False, False, True, True, True, False],
                [False, True, False, False, True, True, True, False],
                [False, True, False, True, True, True, True, False],
                [True, False, True, True, True, True, True, False],
            ],
        ]
    )


@pytest.fixture
def reachable():
    return np.array(
        [
            [  # up
                [False, False, False, False, False, False, False, False],
                [True, True, True, True, False, False, False, True],
                [True, True, True, True, True, False, True, True],
                [True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True],
            ],
            [  # down
                [True, True, True, True, True, True, True, True],
                [True, True, True, True, True, True, True, True],
                [True, True, True, True, False, False, True, True],
                [True, True, True, False, False, False, False, True],
                [False, False, False, False, False, False, False, False],
            ],
            [  # left
                [False, True, True, False, True, True, True, True],
                [False, True, True, False, False, True, True, True],
                [False, False, True, False, False, True, True, True],
                [False, False, True, False, True, True, True, True],
                [False, True, False, True, True, True, True, True],
            ],
            [  # right
                [True, True, True, True, True, True, True, False],
                [True, True, True, True, True, True, False, False],
                [True, True, True, True, True, False, False, False],
                [True, True, True, True, True, True, False, False],
                [True, True, True, True, True, True, True, False],
            ],
        ]
    )


@pytest.fixture
def distances_from_end():
    return np.array(
        [
            [
                [31, 30, 29, 12, 13, 14, 15, 16],
                [30, 29, 28, 11, 2, 3, 4, 17],
                [31, 28, 27, 10, 1, 0, 5, 18],
                [30, 27, 26, 9, 8, 7, 6, 19],
                [29, 28, 25, 24, 23, 22, 21, 20],
            ],
        ]
    )


def test_movement_options(data, options):
    assert (movement_options(data[0]) == options).all()


def test_reachable_from(options, reachable):
    assert (reachable_from(options) == reachable).all()


def test_distance_from(reachable, distances_from_end):
    assert (distance_from(reachable, (2, 5)) == distances_from_end).all()


def test_parse_part_1(text, data):
    layout, start, end = data
    parsed = parse_part_1(text)
    assert (parsed[0] == layout).all()
    assert parsed[1] == start
    assert parsed[2] == end


def test_solve_part_1(reachable, data):
    layout, start, end = data
    assert solve_part_1(reachable, start, end) == 31


def test_solve_part_2(reachable, data):
    layout, start, end = data
    assert solve_part_2(layout, reachable, end) == 29
