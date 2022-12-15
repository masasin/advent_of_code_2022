import functools as ft
from pathlib import Path
from typing import Generator, Iterable, NamedTuple

import simplematch as sm


Point = complex
Distance = int


class Sensor(NamedTuple):
    position: Point
    beacon: Point

    @staticmethod
    def manhattan_distance(point_1: Point, point_2: Point) -> Distance:
        return int(abs(point_1.real - point_2.real) + abs(point_1.imag - point_2.imag))

    @property
    @ft.lru_cache
    def range(self) -> Distance:
        return self.manhattan_distance(self.position, self.beacon)

    def row_range_limits(self, row) -> range:
        vertical_range = abs(row - self.position.imag)
        if vertical_range > self.range:
            return
        horizontal_range = abs(self.range - vertical_range)
        return range(
            int(self.position.real - horizontal_range),
            int(self.position.real + horizontal_range) + 1,
        )

    def contains(self, point: Point) -> bool:
        return self.manhattan_distance(point, self.position) <= self.range


def parse(text: str) -> Generator[Sensor, None, None]:
    pattern = "*x={sensor_x:int}, y={sensor_y:int}*x={beacon_x:int}, y={beacon_y:int}"
    for line in text.splitlines():
        match = sm.match(pattern, line)
        sensor = match["sensor_x"] + match["sensor_y"] * 1j
        beacon = match["beacon_x"] + match["beacon_y"] * 1j
        yield Sensor(sensor, beacon)


def bounds(data: Iterable[Sensor]) -> tuple[int, int, int, int]:
    min_x = float("inf")
    max_x = -float("inf")
    min_y = float("inf")
    max_y = -float("inf")

    for sensor in data:
        min_x = min(min_x, sensor.position.real - sensor.range)
        max_x = max(max_x, sensor.position.real + sensor.range)
        min_y = min(min_y, sensor.position.imag - sensor.range)
        max_y = max(max_y, sensor.position.imag + sensor.range)

    return int(min_x), int(min_y), int(max_x), int(max_y)


def range_overlapping(r1: range, r2: range) -> bool:
    return r1.start <= r2.stop and r2.start <= r1.stop


def range_overlap(r1: range, r2: range) -> range:
    if not range_overlapping(r1, r2):
        return r1, r2
    return range(min(r1.start, r2.start), max(r1.stop, r2.stop))


def ranges_on_row(data: Iterable[Sensor], row: int) -> list[range]:
    limits = sorted(
        [
            limit
            for sensor in data
            if (limit := sensor.row_range_limits(row)) is not None
        ],
        key=lambda r: r.start,
    )
    ranges = []

    r1, *rest = limits
    for r2 in rest:
        r1 = range_overlap(r1, r2)
        if isinstance(r1, tuple):
            ranges.append(r1[0])
            r1 = r1[1]
    ranges.append(r1)
    return ranges


def count_elements(ranges: list[range]) -> int:
    return sum(range.stop - range.start for range in ranges)


def solve_part_1(data: Iterable[Sensor], row: int) -> int:
    beacons = set(sensor.beacon for sensor in data)
    n_sensors_on_row = sum(sensor.position.imag == row for sensor in data)
    n_beacons_on_row = sum(beacon.imag == row for beacon in beacons)
    ranges = ranges_on_row(data, row)

    return count_elements(ranges) - n_sensors_on_row - n_beacons_on_row


def solve_part_2(data: Iterable[Sensor], max_coord: int) -> int:
    for row in range(max_coord + 1):
        ranges = ranges_on_row(data, row)
        if len(ranges) == 2:
            break
    col = ranges[0].stop  # noqa
    return col * 4_000_000 + row  # noqa


def main():
    text = Path("../inputs/day_15.txt").read_text()
    data = list(parse(text))
    print(f"Part 1: {solve_part_1(data, row=2_000_000)}")
    print(f"Part 2: {solve_part_2(data, max_coord=4_000_000)}")


if __name__ == "__main__":
    main()
