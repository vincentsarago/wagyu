from typing import (List,
                    Optional)

from reprit.base import generate_repr

from .edge import Edge
from .enums import (EdgeSide,
                    PolygonKind)
from .point import Point
from .ring import Ring


class Bound:
    __slots__ = ('edges', 'last_point', 'ring', 'current_x', 'position',
                 'winding_count', 'opposite_winding_count', 'winding_delta',
                 'polygon_kind', 'side', 'maximum_bound')

    def __init__(self,
                 edges: Optional[List[Edge]] = None,
                 last_point: Point = Point(0, 0),
                 ring: Optional[Ring] = None,
                 current_x: float = 0.,
                 position: int = 0,
                 winding_count: int = 0,
                 opposite_winding_count: int = 0,
                 winding_delta: int = 0,
                 polygon_kind: PolygonKind = PolygonKind.SUBJECT,
                 side: EdgeSide = EdgeSide.LEFT) -> None:
        self.edges = edges or []
        self.last_point = last_point
        self.ring = ring
        self.current_x = current_x
        self.position = position
        self.winding_count = winding_count
        self.opposite_winding_count = opposite_winding_count
        self.winding_delta = winding_delta
        self.polygon_kind = polygon_kind
        self.side = side
        self.maximum_bound = None  # type: Optional[Bound]

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Bound') -> bool:
        return (self.edges == other.edges
                and self.last_point == other.last_point
                and self.ring == other.ring
                and self.current_x == other.current_x
                and self.position == other.position
                and self.winding_count == other.winding_count
                and self.opposite_winding_count == other.opposite_winding_count
                and self.winding_delta == other.winding_delta
                and self.polygon_kind is other.polygon_kind
                and self.side is other.side
                if isinstance(other, Bound)
                else NotImplemented)

    def fix_horizontals(self) -> None:
        edge_index = 0
        next_index = 1
        edges = self.edges
        if next_index == len(edges):
            return
        edge = edges[edge_index]
        if edge.is_horizontal and edges[next_index].bottom != edge.top:
            edge.reverse_horizontal()
        prev_edge = edge
        edge_index += 1
        while edge_index < len(edges):
            edge = edges[edge_index]
            if edge.is_horizontal and prev_edge.top != edge.bottom:
                edge.reverse_horizontal()
            prev_edge = edge
            edge_index += 1

    def move_horizontals(self, other: 'Bound') -> None:
        index = 0
        edges = self.edges
        while index < len(edges):
            edge = edges[index]
            if not edge.is_horizontal:
                break
            edge.reverse_horizontal()
            index += 1
        if not index:
            return
        other_edges = other.edges
        other_edges.extend(reversed(edges[:index]))
        del edges[:index]
        other_edges[:] = other_edges[-index:] + other_edges[:-index]
