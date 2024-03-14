from __future__ import annotations

from typing import Optional
from shapely.geometry.polygon import Polygon
from shapely import distance

from .spot import Spot


class CellSpot(Spot):
    """
    Useful information for a detected cell.
    """

    def __init__(
        self,
        frame: int,
        x: int,
        y: int,
        id_number: int,
        rel_min_x: int,
        rel_max_x: int,
        rel_min_y: int,
        rel_max_y: int,
        spot_points: list[list[int]],
    ):
        super().__init__(frame, x, y)

        self.id = id_number
        self.rel_min_x = rel_min_x
        self.rel_max_x = rel_max_x
        self.rel_min_y = rel_min_y
        self.rel_max_y = rel_max_y
        self.spot_points = spot_points

        self.track_id: int = -1

        # Get min and max positions
        self.abs_min_x, self.abs_max_x = (
            int(self.x + self.rel_min_x),
            int(self.x + self.rel_max_x),
        )
        self.abs_min_y, self.abs_max_y = (
            int(self.y + self.rel_min_y),
            int(self.y + self.rel_max_y),
        )

        # Phase predicted by model
        self.predicted_phase: Optional[int] = None
        # Corresponding (closest) metaphase spot in track
        self.corresponding_metaphase_spot = None

    def is_stuck_to(self, other_spot: CellSpot, maximum_stuck_distance: float):
        """
        Distance between two spots hulls.
        """
        return (
            distance(
                Polygon(self.spot_points), Polygon(other_spot.spot_points)
            )
            < maximum_stuck_distance
        )