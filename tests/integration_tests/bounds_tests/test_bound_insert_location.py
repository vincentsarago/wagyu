from _wagyu import bound_insert_location as bound
from hypothesis import given

from tests.utils import (BoundPortedBoundsPair,
                         equivalence)
from wagyu.bound import bound_insert_location as ported
from . import strategies


@given(strategies.initialized_bounds_pairs,
       strategies.initialized_bounds_pairs)
def test_basic(first_pair: BoundPortedBoundsPair,
               second_pair: BoundPortedBoundsPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    first_bound.current_edge_index = first_ported.current_edge_index = 2
    second_bound.current_edge_index = second_ported.current_edge_index = 1

    assert equivalence(bound(first_bound, second_bound),
                       ported(first_ported, second_ported))