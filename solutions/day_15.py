import functools as ft
from pathlib import Path
from typing import Generator, Iterable, NamedTuple

import simplematch as sm


Point = complex
Distance = int


class SensorReading(NamedTuple):
    position: Point
    beacon: Point

    @property
    @ft.lru_cache
    def range(self) -> Distance:
        return manhattan_distance(self.position, self.beacon)


def manhattan_distance(point_1: Point, point_2: Point) -> Distance:
    return int(abs(point_1.real - point_2.real) + abs(point_1.imag - point_2.imag))


def parse_part_1(text: str) -> Generator[SensorReading, None, None]:
    pattern = "*x={sensor_x:int}, y={sensor_y:int}*x={beacon_x:int}, y={beacon_y:int}"
    for line in text.splitlines():
        match = sm.match(pattern, line)
        sensor = match["sensor_x"] + match["sensor_y"] * 1j
        beacon = match["beacon_x"] + match["beacon_y"] * 1j
        yield SensorReading(sensor, beacon)


def bounds(data: Iterable[SensorReading]) -> tuple[int, int, int, int]:
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


def within_range(point: Point, sensor: SensorReading) -> bool:
    return manhattan_distance(point, sensor.position) <= sensor.range


def solve_part_1(data: Iterable[SensorReading], row: int) -> int:
    min_x, min_y, max_x, max_y = bounds(data)
    beacons = set(sensor.beacon for sensor in data)
    n_sensors_on_row = sum(sensor.position.imag == row for sensor in data)
    n_beacons_on_row = sum(beacon.imag == row for beacon in beacons)
    return (
        sum(
            any(within_range(col + row * 1j, sensor) for sensor in data)
            for col in range(min_x, max_x + 1)
        )
        - n_sensors_on_row
        - n_beacons_on_row
    )


def parse_part_2(text: str) -> Generator:
    ...


def solve_part_2(data: Iterable):
    ...


def main():
    text = Path("../inputs/day_15.txt").read_text()
    data = list(parse_part_1(text))
    print(f"Part 1: {solve_part_1(data, row=2_000_000)}")
    print(f"Part 2: {solve_part_2(parse_part_2(text))}")


if __name__ == "__main__":
    main()
