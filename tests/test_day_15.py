from textwrap import dedent
import pytest

from solutions.day_15 import (
    parse,
    solve_part_1,
    Sensor,
    ranges_on_row,
    count_elements,
    solve_part_2,
    point_within_some_sensor_range,
)


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
    return frozenset(
        [
            Sensor(2 + 18j, -2 + 15j),
            Sensor(9 + 16j, 10 + 16j),
            Sensor(13 + 2j, 15 + 3j),
            Sensor(12 + 14j, 10 + 16j),
            Sensor(10 + 20j, 10 + 16j),
            Sensor(14 + 17j, 10 + 16j),
            Sensor(8 + 7j, 2 + 10j),
            Sensor(2 + 0j, 2 + 10j),
            Sensor(0 + 11j, 2 + 10j),
            Sensor(20 + 14j, 25 + 17j),
            Sensor(17 + 20j, 21 + 22j),
            Sensor(16 + 7j, 15 + 3j),
            Sensor(14 + 3j, 15 + 3j),
            Sensor(20 + 1j, 15 + 3j),
        ]
    )


def test_parse(text, data):
    assert frozenset(parse(text)) == data


def test_solve_part_1(data):
    assert solve_part_1(data, 10) == 26


@pytest.mark.parametrize(
    ["sensor", "row", "limits"],
    [
        (Sensor(8 + 7j, 2 + 10j), 7, range(-1, 18)),
        (Sensor(8 + 7j, 2 + 10j), 10, range(2, 15)),
        (Sensor(8 + 7j, 2 + 10j), 4, range(2, 15)),
        (Sensor(8 + 7j, 2 + 10j), 20, None),
    ],
)
def test_col_limits_on_row(data, sensor, row, limits):
    assert sensor.row_range_limits(row) == limits


@pytest.mark.parametrize(
    ["row", "ranges"],
    [
        (10, [range(-2, 25)]),
        (11, [range(-3, 14), range(15, 26)]),
    ],
)
def test_ranges_on_row(data, row, ranges):
    assert ranges_on_row(data, row) == ranges


@pytest.mark.parametrize(
    ["ranges", "n_elements"],
    [
        ([range(-2, 25)], 27),
        ([range(-3, 14), range(15, 26)], 28),
    ],
)
def test_count_elements(ranges, n_elements):
    assert count_elements(ranges) == n_elements


def test_solve_part_2(data):
    assert solve_part_2(data, 20) == 56_000_011


@pytest.mark.parametrize(
    ["sensor", "perimeter"],
    [
        (
            Sensor(0 + 11j, 2 + 10j),
            {
                0 + 7j,
                1 + 8j,
                2 + 9j,
                3 + 10j,
                4 + 11j,
                3 + 12j,
                2 + 13j,
                1 + 14j,
                0 + 15j,
            },
        ),
        (
            Sensor(9 + 16j, 10 + 16j),
            {
                9 + 14j,
                10 + 15j,
                11 + 16j,
                10 + 17j,
                9 + 18j,
                8 + 17j,
                7 + 16j,
                8 + 15j,
            },
        ),
        (
            Sensor(8 + 7j, 2 + 10j),
            {
                5j,
                1 + 4j,
                2 + 3j,
                3 + 2j,
                4 + 1j,
                5 + 0j,
                11 + 0j,
                12 + 1j,
                13 + 2j,
                14 + 3j,
                15 + 4j,
                16 + 5j,
                17 + 6j,
                18 + 7j,
                17 + 8j,
                16 + 9j,
                15 + 10j,
                14 + 11j,
                13 + 12j,
                12 + 13j,
                11 + 14j,
                10 + 15j,
                9 + 16j,
                8 + 17j,
                7 + 16j,
                6 + 15j,
                5 + 14j,
                4 + 13j,
                3 + 12j,
                2 + 11j,
                1 + 10j,
                9j,
            },
        ),
    ],
)
def test_perimeter(sensor, perimeter):
    assert set(sensor.perimeter(20)) == perimeter


@pytest.mark.parametrize(
    ["point", "in_range"],
    [(10 + 9j, True), (20 + 9j, True), (11 + 10j, True), (14 + 11j, False)],
)
def test_point_within_some_sensor_range(data, point, in_range):
    sensors = frozenset(data)
    assert point_within_some_sensor_range(point, sensors) is in_range
