import functools as ft
import itertools as it
import operator as op
from pathlib import Path
import pprint as pp
from typing import Generator, Union


Tree = dict[str, Union[int, "Tree"]]


def _node(path: Path, tree: Tree) -> Tree | int:
    return ft.reduce(op.getitem, path.parts, tree)  # noqa


def walk_dir(path: Path | str, tree: Tree) -> Generator[tuple[Path, int], None, None]:
    path = Path(path)
    value = _node(path, tree)
    match value:
        case dict():
            for key in value.keys():
                yield from walk_dir(path / key, tree)
        case int():
            yield path, value


def dir_size(path: Path, tree: Tree) -> int:
    return sum(size for file, size in walk_dir(path, tree))


def get_dirs(tree: Tree) -> set[Path]:
    return set(
        it.chain.from_iterable(file.parents for file, size in walk_dir("/", tree))
    )


def dirs_smaller_than(
    max_size: int, tree: Tree
) -> Generator[tuple[Path, int], None, None]:
    for dir_ in get_dirs(tree):
        if (size := dir_size(dir_, tree)) <= max_size:
            yield dir_, size


def move_dir(target: str, path: Path) -> Path:
    match target:
        case "/":
            return Path("/")
        case "..":
            return path.parent
        case other:
            return path / other


def parse(text: str) -> Tree:
    tree: Tree = {"/": {}}
    path = Path("/")
    for line in text.splitlines():
        match line.split():
            case ["$", "cd", target]:
                path = move_dir(target, path)
            case ["$", *_]:
                pass
            case ["dir", name]:
                _node(path, tree)[name] = {}
            case [size, name]:
                _node(path, tree)[name] = int(size)
    return tree


def solve_part_1(data: Tree) -> int:
    return sum(size for dir_, size in dirs_smaller_than(100_000, data))


def solve_part_2(data: Tree) -> int:
    ...


def main():
    text = Path("../inputs/day_07.txt").read_text()
    data = parse(text)
    print(f"Part 1: {solve_part_1(data)}")
    print(f"Part 2: {solve_part_2(data)}")


if __name__ == "__main__":
    main()
