from textwrap import dedent

import pytest

from solutions.day_05 import (
    Move,
    parse_start_config,
    parse_instructions,
    parse,
    apply_move,
    top_of_stacks,
    solve_part_1,
)


@pytest.fixture
def start_config_str():
    return dedent(
        """\
            [D]    
        [N] [C]    
        [Z] [M] [P]
         1   2   3
        """
    )


@pytest.fixture
def instructions_str():
    return dedent(
        """\
        move 1 from 2 to 1
        move 3 from 1 to 3
        move 2 from 2 to 1
        move 1 from 1 to 2
        """
    )


@pytest.fixture
def text():
    return dedent(
        """\
            [D]    
        [N] [C]    
        [Z] [M] [P]
         1   2   3
         
        move 1 from 2 to 1
        move 3 from 1 to 3
        move 2 from 2 to 1
        move 1 from 1 to 2
        """
    )


@pytest.fixture
def start_config():
    return [
        ["Z", "N"],
        ["M", "C", "D"],
        ["P"],
    ]


@pytest.fixture
def instructions():
    return [
        Move(1, 2, 1),
        Move(3, 1, 3),
        Move(2, 2, 1),
        Move(1, 1, 2),
    ]


def test_parse_start_config(start_config_str, start_config):
    assert parse_start_config(start_config_str) == start_config


def test_parse_instructions(instructions_str, instructions):
    assert list(parse_instructions(instructions_str)) == instructions


def test_parse(text, start_config, instructions):
    assert parse(text) == (start_config, instructions)


@pytest.mark.parametrize(
    ["move", "result"],
    [
        (Move(1, 2, 1), [["Z", "N", "D"], ["M", "C"], ["P"]]),
        (Move(2, 2, 1), [["Z", "N", "D", "C"], ["M"], ["P"]]),
    ],
)
def test_apply_move(start_config, move, result):
    assert apply_move(start_config, move) == result


def test_top_of_stacks(start_config):
    assert top_of_stacks(start_config) == "NDP"


def test_solve_part_1(start_config, instructions):
    assert solve_part_1(start_config, instructions) == "CMZ"
