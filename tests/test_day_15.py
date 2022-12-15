from textwrap import dedent
import pytest

from solutions.day_15 import parse_part_1, solve_part_1, SensorReading


@pytest.fixture
def text():
    return dedent(
        """\
        Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        Sensor at x=9, y=16: closest beacon is at x=10, y=16
        Sensor at x=13, y=2: closest beacon is at x=15, y=3
        Sensor at x=12, y=14: closest beacon is at x=10, y=16
        Sensor at x=10, y=20: closest beacon is at x=10, y=16
        Sensor at x=14, y=17: closest beacon is at x=10, y=16
        Sensor at x=8, y=7: closest beacon is at x=2, y=10
        Sensor at x=2, y=0: closest beacon is at x=2, y=10
        Sensor at x=0, y=11: closest beacon is at x=2, y=10
        Sensor at x=20, y=14: closest beacon is at x=25, y=17
        Sensor at x=17, y=20: closest beacon is at x=21, y=22
        Sensor at x=16, y=7: closest beacon is at x=15, y=3
        Sensor at x=14, y=3: closest beacon is at x=15, y=3
        Sensor at x=20, y=1: closest beacon is at x=15, y=3
        """
    )


@pytest.fixture
def data():
    return [
        SensorReading(2 + 18j, -2 + 15j),
        SensorReading(9 + 16j, 10 + 16j),
        SensorReading(13 + 2j, 15 + 3j),
        SensorReading(12 + 14j, 10 + 16j),
        SensorReading(10 + 20j, 10 + 16j),
        SensorReading(14 + 17j, 10 + 16j),
        SensorReading(8 + 7j, 2 + 10j),
        SensorReading(2 + 0j, 2 + 10j),
        SensorReading(0 + 11j, 2 + 10j),
        SensorReading(20 + 14j, 25 + 17j),
        SensorReading(17 + 20j, 21 + 22j),
        SensorReading(16 + 7j, 15 + 3j),
        SensorReading(14 + 3j, 15 + 3j),
        SensorReading(20 + 1j, 15 + 3j),
    ]


def test_parse_part_1(text, data):
    assert list(parse_part_1(text)) == data


def test_solve_part_1(data):
    assert solve_part_1(data, 10) == 26
