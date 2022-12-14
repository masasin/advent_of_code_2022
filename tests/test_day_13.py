from textwrap import dedent

import pytest

from solutions.day_13 import (
    parse,
    is_right_order,
    solve_part_1,
    reorder_packets,
    solve_part_2,
)


@pytest.fixture
def text():
    return dedent(
        """\
        [1,1,3,1,1]
        [1,1,5,1,1]

        [[1],[2,3,4]]
        [[1],4]

        [9]
        [[8,7,6]]

        [[4,4],4,4]
        [[4,4],4,4,4]

        [7,7,7,7]
        [7,7,7]

        []
        [3]

        [[[]]]
        [[]]

        [1,[2,[3,[4,[5,6,7]]]],8,9]
        [1,[2,[3,[4,[5,6,0]]]],8,9]
        """
    )


@pytest.fixture
def data():
    return [
        ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]),
        ([[1], [2, 3, 4]], [[1], 4]),
        ([9], [[8, 7, 6]]),
        ([[4, 4], 4, 4], [[4, 4], 4, 4, 4]),
        ([7, 7, 7, 7], [7, 7, 7]),
        ([], [3]),
        ([[[]]], [[]]),
        (
            [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
            [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
        ),
    ]


@pytest.fixture
def reordered():
    return [
        [],
        [[]],
        [[[]]],
        [1, 1, 3, 1, 1],
        [1, 1, 5, 1, 1],
        [[1], [2, 3, 4]],
        [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
        [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
        [[1], 4],
        [[2]],
        [3],
        [[4, 4], 4, 4],
        [[4, 4], 4, 4, 4],
        [[6]],
        [7, 7, 7],
        [7, 7, 7, 7],
        [[8, 7, 6]],
        [9],
    ]


def test_parse(text, data):
    assert list(parse(text)) == data


@pytest.mark.parametrize(
    ["left", "right", "expected"],
    [
        (
            [1, 1, 3, 1, 1],
            [1, 1, 5, 1, 1],
            True,
        ),
        (
            [[1], [2, 3, 4]],
            [[1], 4],
            True,
        ),
        (
            [9],
            [[8, 7, 6]],
            False,
        ),
        (
            [[4, 4], 4, 4],
            [[4, 4], 4, 4, 4],
            True,
        ),
        (
            [7, 7, 7, 7],
            [7, 7, 7],
            False,
        ),
        (
            [],
            [3],
            True,
        ),
        (
            [[[]]],
            [[]],
            False,
        ),
        (
            [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
            [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
            False,
        ),
    ],
)
def test_right_order(left, right, expected):
    assert is_right_order(left, right) == expected


def test_solve_part_1(data):
    assert solve_part_1(data) == 13


def test_reorder_packets(data, reordered):
    assert reorder_packets(data) == reordered


def test_solve_part_2(data):
    assert solve_part_2(data) == 140
