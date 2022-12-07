from pathlib import Path
from textwrap import dedent

import pytest

from solutions.day_07 import (
    dirs_smaller_than,
    parse,
    dir_size,
    solve_part_1,
    walk_dir,
    get_dirs,
    move_dir,
    solve_part_2,
)


@pytest.fixture
def text():
    return dedent(
        """\
        $ cd /
        $ ls
        dir a
        14848514 b.txt
        8504156 c.dat
        dir d
        $ cd a
        $ ls
        dir e
        29116 f
        2557 g
        62596 h.lst
        $ cd e
        $ ls
        584 i
        $ cd ..
        $ cd ..
        $ cd d
        $ ls
        4060174 j
        8033020 d.log
        5626152 d.ext
        7214296 k
        """
    )


@pytest.fixture
def data():
    return {
        "/": {
            "a": {
                "e": {
                    "i": 584,
                },
                "f": 29_116,
                "g": 2557,
                "h.lst": 62_596,
            },
            "b.txt": 14_848_514,
            "c.dat": 8_504_156,
            "d": {
                "j": 4_060_174,
                "d.log": 8_033_020,
                "d.ext": 5_626_152,
                "k": 7_214_296,
            },
        }
    }


def test_walk_dir(data):
    assert set(walk_dir(Path("/a"), data)) == {
        (Path("/a/e/i"), 584),
        (Path("/a/f"), 29_116),
        (Path("/a/g"), 2557),
        (Path("/a/h.lst"), 62_596),
    }


def test_get_dirs(data):
    assert get_dirs(data) == {Path("/"), Path("/a"), Path("/a/e"), Path("/d")}


def test_get_dirs_can_handle_dirs_with_only_subdirs(data):
    data["/"]["l"] = {
        "m": {"n": 100, "o": 1000},
        "p": {"q": 200, "r": 2000, "s": 20_000},
    }
    assert get_dirs(data) == {
        Path("/"),
        Path("/a"),
        Path("/a/e"),
        Path("/d"),
        Path("/l"),
        Path("/l/m"),
        Path("/l/p"),
    }


@pytest.mark.parametrize(
    ["folder", "size"],
    [
        (Path("/a/e"), 584),
        (Path("/a"), 94_853),
        (Path("/d"), 24_933_642),
        (Path("/"), 48_381_165),
    ],
)
def test_dir_size(data, folder, size):
    assert dir_size(folder, data) == size


def test_dirs_smaller_than(data):
    assert set(dirs_smaller_than(100_000, data)) == {
        (Path("/a/e"), 584),
        (Path("/a"), 94_853),
    }


@pytest.mark.parametrize(
    ["target", "path", "expected"],
    [
        ("/", Path(), Path("/")),
        ("a", Path("/"), Path("/a")),
        ("e", Path("/a"), Path("/a/e")),
        ("..", Path("/a/e"), Path("/a")),
        ("..", Path("/"), Path("/")),
        ("d", Path("/"), Path("/d")),
    ],
)
def test_move_dir(target, path, expected):
    assert move_dir(target, path) == expected


def test_parse(text, data):
    assert parse(text) == data


def test_solve_part_1(data):
    assert solve_part_1(data) == 95_437


def test_solve_part_2(data):
    assert solve_part_2(data) == 24_933_642
