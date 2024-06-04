import pytest
from flatworld.tests.tests_functions.graham import calculate_hull
from flatworld.functions.models import Point


@pytest.mark.parametrize(
    "points, expected",
    [
        (
            [
                Point(0, 3),
                Point(1, 1),
                Point(2, 2),
                Point(4, 4),
                Point(0, 0),
                Point(1, 2),
                Point(3, 1),
                Point(3, 3),
            ],
            [Point(0, 3), Point(4, 4), Point(3, 1), Point(0, 0)],
        ),
        (
            [
                Point(1, 2),
                Point(3, 4),
                Point(5, 1),
                Point(6, 5),
                Point(7, 3),
                Point(2, 6),
                Point(8, 8),
                Point(9, 7),
                Point(0, 0),
                Point(4, 7),
                Point(3, 1),
                Point(6, 3),
                Point(2, 3),
                Point(8, 1),
                Point(1, 7),
            ],
            [
                Point(1, 7),
                Point(8, 8),
                Point(9, 7),
                Point(8, 1),
                Point(0, 0),
            ],
        ),
        (
            [
                Point(2, 2),
                Point(0, 3),
                Point(-2, 2),
                Point(-2, -2),
                Point(2, -2),
                Point(0, -1),
                Point(1, -1),
            ],
            [
                Point(-2, 2),
                Point(0, 3),
                Point(2, 2),
                Point(2, -2),
                Point(-2, -2),
            ],
        ),
    ],
)
def test_graham_scan(points, expected):
    graham = calculate_hull(points)
    assert graham == expected
