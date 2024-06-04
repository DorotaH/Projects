import pytest
from flatworld.functions.algorithm_rabinkarp import rabinkarp


@pytest.mark.parametrize(
    "text, pattern, expected",
    [
        (
            "kot ma Ale, a Ala ma kota",
            "Ala",
            [14],
        ),
        (
            "Rybka musi plywac, kotek pije mleczko",
            "pije",
            [25],
        ),
    ],
)
def test_rabinkarp(text, pattern, expected):
    indexes, _, _, _ = rabinkarp(pattern, text)
    assert indexes == expected
