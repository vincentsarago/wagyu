from hypothesis import strategies

from tests.integration_tests.utils import (are_endpoints_non_degenerate,
                                           to_bound_with_ported_edges_pair,
                                           to_bound_with_ported_points_pair)
from tests.strategies import (coordinates,
                              floats)
from tests.utils import (pack,
                         to_pairs)

floats = floats
points_pairs = strategies.builds(to_bound_with_ported_points_pair, coordinates,
                                 coordinates)
points_pairs_pairs = (to_pairs(points_pairs)
                      .filter(are_endpoints_non_degenerate))
edges_pairs = points_pairs_pairs.map(pack(to_bound_with_ported_edges_pair))
