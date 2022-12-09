from textwrap import dedent

import numpy as np
import pytest

from solutions.day_09 import parse, solve_part_1, solve_part_2


@pytest.fixture
def text_part_1():
    return dedent(
        """\
        R 4
        U 4
        L 3
        D 1
        R 4
        D 1
        L 5
        R 2
        """
    )


@pytest.fixture
def text_part_2():
    return dedent(
        """\
        R 5
        U 8
        L 8
        D 3
        R 17
        D 10
        L 25
        U 20
        """
    )


@pytest.fixture
def data_part_1():
    return (
        [np.array([1, 0])] * 4
        + [np.array([0, 1])] * 4
        + [np.array([-1, 0])] * 3
        + [np.array([0, -1])]
        + [np.array([1, 0])] * 4
        + [np.array([0, -1])]
        + [np.array([-1, 0])] * 5
        + [np.array([1, 0])] * 2
    )


@pytest.fixture
def data_part_2(text_part_2):
    return list(parse(text_part_2))


def test_parse(text_part_1, data_part_1):
    assert (np.array(list(parse(text_part_1))) == data_part_1).all()


def test_solve_part_1(data_part_1):
    assert solve_part_1(data_part_1) == 13


def test_solve_part_2(data_part_2):
    assert solve_part_2(data_part_2) == 36
