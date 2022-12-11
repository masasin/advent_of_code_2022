from collections import deque
from textwrap import dedent

import pytest

from solutions.day_11 import (
    Monkey,
    parse_part_1,
    Item,
    Sim,
    solve_part_1,
    parse_part_2,
    solve_part_2,
)


@pytest.fixture
def text():
    return dedent(
        """\
        Monkey 0:
          Starting items: 79, 98
          Operation: new = old * 19
          Test: divisible by 23
            If true: throw to monkey 2
            If false: throw to monkey 3

        Monkey 1:
          Starting items: 54, 65, 75, 74
          Operation: new = old + 6
          Test: divisible by 19
            If true: throw to monkey 2
            If false: throw to monkey 0

        Monkey 2:
          Starting items: 79, 60, 97
          Operation: new = old * old
          Test: divisible by 13
            If true: throw to monkey 1
            If false: throw to monkey 3

        Monkey 3:
          Starting items: 74
          Operation: new = old + 3
          Test: divisible by 17
            If true: throw to monkey 0
            If false: throw to monkey 1
        """
    )


@pytest.fixture
def data_part_1():
    return [
        Monkey(
            items=[
                Item(worry=79),
                Item(worry=98),
            ],
            operation="old * 19",
            divisor=23,
            if_true=2,
            if_false=3,
        ),
        Monkey(
            items=[
                Item(worry=54),
                Item(worry=65),
                Item(worry=75),
                Item(worry=74),
            ],
            operation="old + 6",
            divisor=19,
            if_true=2,
            if_false=0,
        ),
        Monkey(
            items=[
                Item(worry=79),
                Item(worry=60),
                Item(worry=97),
            ],
            operation="old * old",
            divisor=13,
            if_true=1,
            if_false=3,
        ),
        Monkey(
            items=[Item(worry=74)],
            operation="old + 3",
            divisor=17,
            if_true=0,
            if_false=1,
        ),
    ]


def test_parse_part_1(text, data_part_1):
    assert list(parse_part_1(text)) == data_part_1


@pytest.mark.parametrize(
    ["operation", "worry"],
    [
        ("old * 19", 95),
        ("old + 6", 11),
        ("old * old", 25),
    ],
)
def test_apply_operation(operation, worry):
    item = Item(worry=5)
    item.apply_operation(operation)
    assert item.worry == worry


def test_play_round(data_part_1):
    sim = Sim(*data_part_1)
    sim.play_round()
    assert [[item.worry for item in monkey.items] for monkey in sim.monkeys] == [
        [20, 23, 27, 26],
        [2080, 25, 167, 207, 401, 1046],
        [],
        [],
    ]


def test_n_inspected_calculated_correctly(data_part_1):
    sim = Sim(*data_part_1)
    for _ in range(20):
        sim.play_round()
    assert [monkey.n_inspected for monkey in sim.monkeys] == [101, 95, 7, 105]


def test_solve_part_1(data_part_1):
    assert solve_part_1(data_part_1) == 10605


@pytest.fixture
def data_part_2():
    return [
        Monkey(
            items=[
                Item(worry=79, part_1=False),
                Item(worry=98, part_1=False),
            ],
            operation="old * 19",
            divisor=23,
            if_true=2,
            if_false=3,
        ),
        Monkey(
            items=[
                Item(worry=54, part_1=False),
                Item(worry=65, part_1=False),
                Item(worry=75, part_1=False),
                Item(worry=74, part_1=False),
            ],
            operation="old + 6",
            divisor=19,
            if_true=2,
            if_false=0,
        ),
        Monkey(
            items=[
                Item(worry=79, part_1=False),
                Item(worry=60, part_1=False),
                Item(worry=97, part_1=False),
            ],
            operation="old * old",
            divisor=13,
            if_true=1,
            if_false=3,
        ),
        Monkey(
            items=[Item(worry=74, part_1=False)],
            operation="old + 3",
            divisor=17,
            if_true=0,
            if_false=1,
        ),
    ]


def test_parse_part_2(text, data_part_2):
    assert list(parse_part_2(text)) == data_part_2


def test_solve_part_2(data_part_2):
    assert solve_part_2(data_part_2) == 2713310158
