#!/usr/bin/env python3
"""
Direction module for the "botwar ship" game.
"""
from enum import Enum, auto


class Direction(Enum):
    """
    Direction enum representing all possible movement directions in a hexagonal grid.

    Directions:
    - O: Origin (0, 0, 0)
    - E: East (1, 0, -1)
    - SE: Southeast (0, 1, -1)
    - SW: Southwest (-1, 1, 0)
    - W: West (-1, 0, 1)
    - NW: Northwest (0, -1, 1)
    - NE: Northeast (1, -1, 0)
    """
    O = auto()
    E = auto()
    SE = auto()
    SW = auto()
    W = auto()
    NW = auto()
    NE = auto()

    @staticmethod
    def all_non_origin():
        """
        Get a list of all directions except the origin.

        Returns:
            List of all directions except the origin
        """
        return [Direction.E, Direction.SE, Direction.SW, Direction.W, Direction.NW, Direction.NE]

    def to_coordinate(self):
        """
        Convert the direction to a coordinate offset.

        Returns:
            Tuple of (q, r, s) coordinate offset
        """
        direction_to_coordinate = {
            Direction.O: (0, 0, 0),
            Direction.E: (1, 0, -1),
            Direction.SE: (0, 1, -1),
            Direction.SW: (-1, 1, 0),
            Direction.W: (-1, 0, 1),
            Direction.NW: (0, -1, 1),
            Direction.NE: (1, -1, 0),
        }
        return direction_to_coordinate[self]
