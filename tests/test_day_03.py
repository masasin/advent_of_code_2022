from textwrap import dedent

import pytest

from solutions.day_03 import (
    letter_priority,
    split_contents,
    common_items,
    parse_part_1,
    parse_part_2,
)


@pytest.fixture
def text():
    return dedent(
        """\
        vJrwpWtwJgWrhcsFMMfFFhFp
        jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
        PmmdzqPrVvPwwTWBwg
        wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
        ttgJtRGJQctTZtZT
        CrZsJsPPZsGzwwsLwLmpwMDw
        """
    )


@pytest.fixture
def data_part_1():
    return [16, 38, 42, 22, 20, 19]


@pytest.fixture
def data_part_2():
    return [18, 52]


@pytest.mark.parametrize(
    ("letter", "priority"),
    [
        ("p", 16),
        ("s", 19),
        ("t", 20),
        ("v", 22),
        ("L", 38),
        ("P", 42),
    ],
)
def test_letter_priority(letter, priority):
    assert letter_priority(letter) == priority


@pytest.mark.parametrize(
    ("rucksack", "split"),
    [
        ("vJrwpWtwJgWrhcsFMMfFFhFp", ("vJrwpWtwJgWr", "hcsFMMfFFhFp")),
        ("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", ("jqHRNqRjqzjGDLGL", "rsFMfFZSrLrFZsSL")),
        ("PmmdzqPrVvPwwTWBwg", ("PmmdzqPrV", "vPwwTWBwg")),
    ],
)
def test_split_contents(rucksack, split):
    assert split_contents(rucksack) == split


@pytest.mark.parametrize(
    ("items", "common"),
    [
        (["vJrwpWtwJgWr", "hcsFMMfFFhFp"], "p"),
        (["jqHRNqRjqzjGDLGL", "rsFMfFZSrLrFZsSL"], "L"),
        (["PmmdzqPrV", "vPwwTWBwg"], "P"),
        (
            [
                "vJrwpWtwJgWrhcsFMMfFFhFp",
                "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                "PmmdzqPrVvPwwTWBwg",
            ],
            "r",
        ),
        (
            [
                "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
                "ttgJtRGJQctTZtZT",
                "CrZsJsPPZsGzwwsLwLmpwMDw",
            ],
            "Z",
        ),
    ],
)
def test_common_items(items, common):
    assert common_items(*items) == common


def test_parse_part_1(text, data_part_1):
    assert list(parse_part_1(text)) == data_part_1


def test_parse_part_2(text, data_part_2):
    assert list(parse_part_2(text)) == data_part_2
