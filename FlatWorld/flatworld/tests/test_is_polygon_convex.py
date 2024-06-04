import pytest
from flatworld.tests.tests_functions.is_polygon_convex import is_polygon_convex
import math
from flatworld.functions.models import Point


@pytest.mark.parametrize(
    "points, expected",
    [
        (
            [Point(0, 0), Point(1, 0), Point(0, 1)],
            True,
        ),
        (
            [
                Point(
                    math.cos(2 * math.pi * i / 5),
                    math.sin(2 * math.pi * i / 5),
                )
                for i in range(5)
            ],
            True,
        ),
        (
            [
                Point(0, 0),
                Point(1, 0),
                Point(1, 1),
                Point(1, 2),
                Point(0.75, 1),
                Point(0.5, 1.5),
                Point(0, 1),
            ],
            False,
        ),
    ],
)
def test_graham_scan(points, expected):
    Polygon = is_polygon_convex(points)
    assert Polygon == expected
