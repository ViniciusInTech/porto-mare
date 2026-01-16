from datetime import datetime, timedelta, timezone
from typing import List
from zoneinfo import ZoneInfo
import httpx
from app.domain.models.tide import Tide
from app.domain.ports.tide_provider import TideProvider
from app.config.settings import settings

BRAZIL_TZ = ZoneInfo("America/Sao_Paulo")


def _parse_tides(payload: dict) -> List[Tide]:
    tides: List[Tide] = []

    port_data = payload["data"][0]
    year = port_data["year"]

    for month_data in port_data["months"]:
        month = month_data["month"]

        for day_data in month_data["days"]:
            day = day_data["day"]

            for hour_data in day_data["hours"]:
                time_str = hour_data["hour"]
                level = float(hour_data["level"])

                tide_time = datetime.fromisoformat(
                    f"{year}-{month:02d}-{day:02d} {time_str}"
                ).replace(tzinfo=BRAZIL_TZ)

                tides.append(
                    Tide(
                        time=tide_time,
                        level=level,
                        type=""
                    )
                )

    return sorted(tides, key=lambda t: t.time)


class TideApiProvider(TideProvider):

    def __init__(self):
        self.base_url = f"{settings.tide_api_base_url}/api/{settings.tide_api_version}"
        self.ttl = timedelta(minutes=settings.tide_api_cache_ttl_minutes)
        self.timeout = settings.tide_api_timeout
        self.cache: dict[str, tuple[List[Tide], datetime]] = {}

    def get_tides(self, harbor_id: str, month: int, days: str) -> List[Tide]:
        response = httpx.get(
            f"{self.base_url}/tabua-mare/{harbor_id}/{month}/{days}",
            timeout=10
        )
        response.raise_for_status()
        payload = response.json()

        return _parse_tides(payload)
