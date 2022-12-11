from pathlib import Path
from typing import Deque, Generator, Iterable

from pydantic import BaseModel


class Item(BaseModel):
    worry: int

    def apply_operation(self, operation: str):
        match operation.split()[1:]:
            case ["+", number]:
                self.worry += int(number)
            case ["*", "old"]:
                self.worry **= 2
            case ["*", number]:
                self.worry *= int(number)


class Monkey(BaseModel):
    items: Deque[Item]
    operation: str
    divisor: int
    if_true: int
    if_false: int
    n_inspected: int = 0

    def inspect_one(self) -> tuple[int, Item]:
        self.n_inspected += 1
        item = self.items.popleft()
        item.apply_operation(self.operation)
        item.worry //= 3
        if item.worry % self.divisor == 0:
            return self.if_true, item
        else:
            return self.if_false, item

    def inspect_all(self) -> Generator[tuple[int, Item], None, None]:
        yield from (self.inspect_one() for _ in range(len(self.items)))


class Sim:
    def __init__(self, *monkeys):
        self.monkeys = monkeys
        self._n_rounds = 0

    def step(self, monkey):
        for next_monkey_id, item in monkey.inspect_all():
            self.monkeys[next_monkey_id].items.append(item)

    def play_round(self):
        for monkey in self.monkeys:
            self.step(monkey)
        self._n_rounds += 1


def parse_part_1(text: str) -> Generator[Monkey, None, None]:
    for block in text.split("\n\n"):
        _, starting, operation, test, if_true, if_false = block.splitlines()
        yield Monkey(
            items=[Item(worry=i) for i in starting.split(": ")[1].split(", ")],
            operation=operation.split(" = ")[1],
            divisor=test.rsplit(" ")[-1],
            if_true=if_true.rsplit(" ")[-1],
            if_false=if_false.rsplit(" ")[-1],
        )


def solve_part_1(monkeys: Iterable[Monkey]) -> int:
    sim = Sim(*monkeys)
    for _ in range(20):
        sim.play_round()
    *_, second, first = sorted([monkey.n_inspected for monkey in sim.monkeys])
    return first * second


def solve_part_2(data: Iterable[Monkey]) -> int:
    ...


def main():
    text = Path("../inputs/day_11.txt").read_text()
    data = list(parse_part_1(text))
    print(f"Part 1: {solve_part_1(data)}")
    print(f"Part 2: {solve_part_2(data)}")


if __name__ == "__main__":
    main()
