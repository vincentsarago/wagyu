from _wagyu import Point
from hypothesis import given

from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.points)
def test_reflexivity(point: Point) -> None:
    assert point == point


@given(strategies.points, strategies.points)
def test_symmetry(first_point: Point,
                  second_point: Point) -> None:
    assert equivalence(first_point == second_point,
                       second_point == first_point)


@given(strategies.points, strategies.points, strategies.points)
def test_transitivity(first_point: Point, second_point: Point,
                      third_point: Point) -> None:
    assert implication(first_point == second_point
                       and second_point == third_point,
                       first_point == third_point)


@given(strategies.points, strategies.points)
def test_connection_with_inequality(first_point: Point,
                                    second_point: Point) -> None:
    assert equivalence(not first_point == second_point,
                       first_point != second_point)
