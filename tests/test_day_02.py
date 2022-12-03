from textwrap import dedent

import pytest

from solutions.day_02 import pair_score, reverse_solve, parse_part_1, parse_part_2


@pytest.fixture
def text():
    return dedent(
        """\
        A Y
        B X
        C Z
        """
    )


@pytest.fixture
def data_part_1():
    return [8, 1, 6]


@pytest.fixture
def data_part_2():
    return [4, 1, 7]


@pytest.mark.parametrize(
    ["opponent", "player", "score"],
    [
        ("A", "B", 8),
        ("B", "A", 1),
        ("C", "C", 6),
    ],
)
def test_pair_score(opponent, player, score):
    assert pair_score(opponent, player) == score


@pytest.mark.parametrize(
    ["opponent", "end_state", "selection"],
    [
        ("A", "Y", "A"),
        ("B", "X", "A"),
        ("C", "Z", "A"),
    ],
)
def test_reverse_solve(opponent, end_state, selection):
    assert reverse_solve(opponent, end_state) == selection


def test_parse_part_1(text, data_part_1):
    assert list(parse_part_1(text)) == data_part_1


def test_parse_part_2(text, data_part_2):
    assert list(parse_part_2(text)) == data_part_2
