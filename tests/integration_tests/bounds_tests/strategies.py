from hypothesis import strategies
from hypothesis_geometry import planar

from tests.strategies import (coordinates,
                              floats,
                              integers_32,
                              sizes,
                              trits)
from tests.utils import (BoundPortedBoundsPair,
                         Strategy,
                         bound_edges_sides,
                         bound_polygons_kinds,
                         ported_edges_sides,
                         ported_polygons_kinds,
                         to_bound_with_ported_bounds_pair,
                         to_bound_with_ported_edges_lists,
                         to_bound_with_ported_linear_rings,
                         to_bound_with_ported_linear_rings_points,
                         to_bound_with_ported_points_pair,
                         to_bound_with_ported_rings_pair,
                         to_maybe_pairs,
                         transpose_pairs)

points_pairs = strategies.builds(to_bound_with_ported_points_pair, coordinates,
                                 coordinates)
booleans = strategies.booleans()
sizes = sizes
maybe_rings_pairs = to_maybe_pairs(strategies.deferred(lambda: rings_pairs))
maybe_rings_lists_pairs = (strategies.lists(maybe_rings_pairs)
                           .map(transpose_pairs))
rings_pairs = strategies.builds(to_bound_with_ported_rings_pair,
                                sizes, maybe_rings_lists_pairs, booleans)
linear_rings_points_pairs = (planar.contours(coordinates)
                             .map(to_bound_with_ported_linear_rings_points))
linear_rings_pairs = (linear_rings_points_pairs
                      .map(to_bound_with_ported_linear_rings))
edges_lists_pairs = linear_rings_pairs.map(to_bound_with_ported_edges_lists)
polygons_kinds_pairs = strategies.sampled_from(
        list(zip(bound_polygons_kinds, ported_polygons_kinds)))
edges_sides_pairs = strategies.sampled_from(list(zip(bound_edges_sides,
                                                     ported_edges_sides)))
bounds_pairs = strategies.builds(to_bound_with_ported_bounds_pair,
                                 edges_lists_pairs, points_pairs,
                                 maybe_rings_pairs, floats, sizes, integers_32,
                                 integers_32, trits, polygons_kinds_pairs,
                                 edges_sides_pairs)


def to_initialized_bounds_pairs(bounds_pair: BoundPortedBoundsPair
                                ) -> Strategy[BoundPortedBoundsPair]:
    bound, ported = bounds_pair
    return strategies.builds(initialize_bounds,
                             strategies.just(bounds_pair),
                             strategies.integers(0, len(ported.edges) - 1))


def initialize_bounds(bounds_pair: BoundPortedBoundsPair,
                      current_edge_index: int) -> BoundPortedBoundsPair:
    bound, ported = bounds_pair
    bound.current_edge_index = ported.current_edge_index = current_edge_index
    return bounds_pair


initialized_bounds_pairs = bounds_pairs.flatmap(to_initialized_bounds_pairs)
