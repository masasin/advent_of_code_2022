from pathlib import Path
from typing import Generator, Iterable

PacketPart = int | list["PacketPart"]
Packet = list[PacketPart]
PacketPair = tuple[Packet, Packet]


def parse_part_1(text: str) -> Generator[PacketPair, None, None]:
    parts = text.split("\n\n")
    for part in parts:
        left, right = map(eval, part.splitlines())
        yield left, right


def is_right_order(left: Packet, right: Packet) -> bool | None:
    match left, right:
        case int(), int():
            if left < right:
                return True
            elif left == right:
                return None
            else:
                return False
        case list(), list():
            for v1, v2 in zip(left, right):
                result = is_right_order(v1, v2)
                if result is None:
                    continue
                return result
            if len(left) < len(right):
                return True
            elif len(left) == len(right):
                return None
            else:
                return False
        case int(), list():
            return is_right_order([left], right)
        case list(), int():
            return is_right_order(left, [right])


def solve_part_1(pairs: Iterable[PacketPair]) -> int:
    return sum(i for i, pair in enumerate(pairs, start=1) if is_right_order(*pair))


def parse_part_2(text: str) -> Generator:
    ...


def solve_part_2(data: Iterable):
    ...


def main():
    text = Path("../inputs/day_13.txt").read_text()
    pairs = parse_part_1(text)
    print(f"Part 1: {solve_part_1(pairs)}")
    print(f"Part 2: {solve_part_2(parse_part_2(text))}")


if __name__ == "__main__":
    main()
