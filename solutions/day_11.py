from pathlib import Path
from typing import Deque, Generator, Iterable

import numpy as np
from pydantic import BaseModel


class Item(BaseModel):
    worry: int
    part_1: bool = True

    def apply_operation(self, operation: str):
        match operation.split()[1:]:
            case ["+", number]:
                self.worry += int(number)
            case ["*", "old"]:
                self.worry **= 2
            case ["*", number]:
                self.worry *= int(number)

    def lower_worry(self, lcm: int = 1):
        if self.part_1:
            self.worry //= 3
        else:
            self.worry %= lcm


class Monkey(BaseModel):
    items: Deque[Item]
    operation: str
    divisor: int
    if_true: int
    if_false: int
    n_inspected: int = 0
    lcm: int = 1

    def inspect_one(self) -> tuple[int, Item]:
        self.n_inspected += 1
        item = self.items.popleft()
        item.apply_operation(self.operation)
        item.lower_worry(self.lcm)
        if item.worry % self.divisor == 0:
            return self.if_true, item
        else:
            return self.if_false, item

    def inspect_all(self) -> Generator[tuple[int, Item], None, None]:
        yield from (self.inspect_one() for _ in range(len(self.items)))


class Sim:
    def __init__(self, *monkeys):
        self.monkeys = monkeys
        lcm = np.prod([monkey.divisor for monkey in self.monkeys])
        for monkey in self.monkeys:
            monkey.lcm = lcm
        self._n_rounds = 0

    def step(self, monkey):
        for next_monkey_id, item in monkey.inspect_all():
            self.monkeys[next_monkey_id].items.append(item)

    def play_round(self):
        for monkey in self.monkeys:
            self.step(monkey)
        self._n_rounds += 1


def _create_monkey(block: str, part_1: bool) -> Monkey:
    _, starting, operation, test, if_true, if_false = block.splitlines()
    return Monkey(
        items=[
            Item(worry=i, part_1=part_1) for i in starting.split(": ")[1].split(", ")
        ],
        operation=operation.split(" = ")[1],
        divisor=test.rsplit(" ")[-1],
        if_true=if_true.rsplit(" ")[-1],
        if_false=if_false.rsplit(" ")[-1],
    )


def parse(text: str, part_1: bool) -> Generator[Monkey, None, None]:
    for block in text.split("\n\n"):
        yield _create_monkey(block, part_1=part_1)


def solve(monkeys: Iterable[Monkey], n_rounds: int) -> int:
    sim = Sim(*monkeys)
    for _ in range(n_rounds):
        sim.play_round()
    *_, second, first = sorted([monkey.n_inspected for monkey in sim.monkeys])
    return first * second


def main():
    text = Path("../inputs/day_11.txt").read_text()
    print(f"Part 1: {solve(parse(text, part_1=True), n_rounds=20)}")
    print(f"Part 2: {solve(parse(text, part_1=False), n_rounds=10_000)}")


if __name__ == "__main__":
    main()
