from textwrap import dedent

import pytest

from solutions.day_04 import (
    Range,
    parse_line,
    ranges_overlap,
    ranges_completely_overlap,
    parse,
    solve_part_1,
    solve_part_2,
)


@pytest.fixture
def text():
    return dedent(
        """\
        2-4,6-8
        2-3,4-5
        5-7,7-9
        2-8,3-7
        6-6,4-6
        2-6,4-8
        """
    )


@pytest.fixture
def data():
    return [
        (Range(2, 4), Range(6, 8)),
        (Range(2, 3), Range(4, 5)),
        (Range(5, 7), Range(7, 9)),
        (Range(2, 8), Range(3, 7)),
        (Range(6, 6), Range(4, 6)),
        (Range(2, 6), Range(4, 8)),
    ]


@pytest.mark.parametrize(
    ["line", "ranges"],
    [
        ("2-4,6-8", (Range(2, 4), Range(6, 8))),
        ("2-3,4-5", (Range(2, 3), Range(4, 5))),
        ("5-7,7-9", (Range(5, 7), Range(7, 9))),
        ("2-8,3-7", (Range(2, 8), Range(3, 7))),
        ("6-6,4-6", (Range(6, 6), Range(4, 6))),
        ("2-6,4-8", (Range(2, 6), Range(4, 8))),
    ],
)
def test_parse_line(line, ranges):
    assert parse_line(line) == ranges


@pytest.mark.parametrize(
    ["left", "right", "overlap"],
    [
        (Range(2, 4), Range(6, 8), False),
        (Range(2, 3), Range(4, 5), False),
        (Range(5, 7), Range(7, 9), True),
        (Range(2, 8), Range(3, 7), True),
        (Range(6, 6), Range(4, 6), True),
        (Range(2, 6), Range(4, 8), True),
    ],
)
def test_ranges_overlap(left, right, overlap):
    assert ranges_overlap(left, right) == overlap


@pytest.mark.parametrize(
    ["left", "right", "overlap"],
    [
        (Range(2, 4), Range(6, 8), False),
        (Range(2, 3), Range(4, 5), False),
        (Range(5, 7), Range(7, 9), False),
        (Range(2, 8), Range(3, 7), True),
        (Range(6, 6), Range(4, 6), True),
        (Range(2, 6), Range(4, 8), False),
    ],
)
def test_ranges_completely_overlap(left, right, overlap):
    assert ranges_completely_overlap(left, right) == overlap


def test_parse(text, data):
    assert list(parse(text)) == data


def test_solve_part_1(data):
    assert solve_part_1(data) == 2


def test_solve_part_2(data):
    assert solve_part_2(data) == 4
