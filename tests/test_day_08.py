from textwrap import dedent

import numpy as np
import pytest

from solutions.day_08 import parse, visibility, solve_part_1, scenic_score, solve_part_2


@pytest.fixture
def text():
    return dedent(
        """\
        30373
        25512
        65332
        33549
        35390
        """
    )


@pytest.fixture
def data():
    return np.array(
        [
            [3, 0, 3, 7, 3],
            [2, 5, 5, 1, 2],
            [6, 5, 3, 3, 2],
            [3, 3, 5, 4, 9],
            [3, 5, 3, 9, 0],
        ]
    )


def test_parse(text, data):
    assert (parse(text) == data).all()


@pytest.mark.parametrize(
    ["row", "col", "visible"],
    [
        (0, 0, 2),
        (0, 2, 1),
        (0, 4, 2),
        (2, 0, 4),
        (2, 4, 1),
        (4, 0, 2),
        (4, 2, 1),
        (4, 4, 2),
        (1, 1, 2),
        (1, 2, 2),
        (1, 3, 0),
        (2, 1, 1),
        (2, 2, 0),
        (2, 3, 1),
        (3, 1, 0),
        (3, 2, 2),
        (3, 3, 0),
    ],
)
def test_visibility(data, row, col, visible):
    assert visibility(row, col, data) == visible


def test_solve_part_1(data):
    assert solve_part_1(data) == 21


@pytest.mark.parametrize(
    ["row", "col", "score"],
    [
        (1, 2, 4),
        (3, 2, 8),
    ],
)
def test_scenic_score(data, row, col, score):
    assert scenic_score(row, col, data) == score


def test_solve_part_2(data):
    assert solve_part_2(data) == 8
