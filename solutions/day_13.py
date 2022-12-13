import functools as ft
import itertools as it
import math
from pathlib import Path
from typing import Generator, Iterable

PacketPart = int | list["PacketPart"]
Packet = list[PacketPart]
PacketPair = tuple[Packet, Packet]


DECODER_PACKETS = [[[2]], [[6]]]


def parse(text: str) -> Generator[PacketPair, None, None]:
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


def reorder_packets(pairs: Iterable[PacketPair]) -> list:
    return sorted(
        list(it.chain.from_iterable(pairs)) + DECODER_PACKETS,
        key=ft.cmp_to_key(lambda left, right: -1 if is_right_order(left, right) else 1),
    )


def solve_part_2(pairs: Iterable[PacketPair]) -> int:
    reordered = reorder_packets(pairs)
    return math.prod(reordered.index(packet) + 1 for packet in DECODER_PACKETS)


def main():
    text = Path("../inputs/day_13.txt").read_text()
    pairs = list(parse(text))
    print(f"Part 1: {solve_part_1(pairs)}")
    print(f"Part 2: {solve_part_2(pairs)}")


if __name__ == "__main__":
    main()
