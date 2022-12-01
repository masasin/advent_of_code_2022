from textwrap import dedent

import pytest

from day_01.main import parse, solve_part_1, solve_part_2


@pytest.fixture
def content():
    return dedent(
        """1000
        2000
        3000

        4000

        5000
        6000

        7000
        8000
        9000

        10000
        """
    )


@pytest.fixture
def data():
    return [6000, 4000, 11000, 24000, 10000]


def test_parse(content, data):
    assert list(parse(content)) == data


def test_solve_part_1(data):
    assert solve_part_1(data) == 24000


def test_solve_part_2(data):
    assert solve_part_2(data) == 45000
