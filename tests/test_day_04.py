from textwrap import dedent

import pytest

from solutions.day_04 import (
    Range,
    parse_line,
    ranges_overlap,
    ranges_completely_overlap,
    parse_part_1,
    parse_part_2,
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
def data_part_1():
    return [False, False, False, True, True, False]


@pytest.fixture
def data_part_2():
    return [False, False, True, True, True, True]


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


def test_parse_part_1(text, data_part_1):
    assert list(parse_part_1(text)) == data_part_1


def test_parse_part_2(text, data_part_2):
    assert list(parse_part_2(text)) == data_part_2
