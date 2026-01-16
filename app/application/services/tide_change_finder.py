from datetime import datetime
from typing import List
from app.domain.models.tide import Tide
from app.domain.models.tide_change import TideChange


def _calculate_type(previous: Tide, current: Tide) -> str:
    if current.level > previous.level:
        return "high"
    return "low"


class TideChangeFinder:

    @staticmethod
    def find_next(tides: List[Tide], now: datetime) -> TideChange:
        if len(tides) < 2:
            raise ValueError("Not enough tide data")

        sorted_tides = sorted(tides, key=lambda t: t.time)

        for index in range(1, len(sorted_tides)):
            previous_tide = sorted_tides[index - 1]
            current_tide = sorted_tides[index]

            if current_tide.time > now:
                tide_type = _calculate_type(previous_tide, current_tide)

                return TideChange(
                    time=current_tide.time,
                    level=current_tide.level,
                    type=tide_type
                )

        raise ValueError("No future tide found")
