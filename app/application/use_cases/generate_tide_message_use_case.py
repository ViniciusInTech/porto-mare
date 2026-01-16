from datetime import datetime
from zoneinfo import ZoneInfo
from app.application.services.tide_change_finder import TideChangeFinder
from app.domain.ports.ai_provider import AIProvider
from app.domain.ports.location_provider import LocationProvider
from app.domain.ports.tide_provider import TideProvider

class GenerateTideMessageUseCase:

    def __init__(
        self,
        location_provider: LocationProvider,
        tide_provider: TideProvider,
        ai_provider: AIProvider
    ):
        self.location_provider = location_provider
        self.tide_provider = tide_provider
        self.ai_provider = ai_provider
        self.tide_finder = TideChangeFinder()

    def execute(self, state_code: str, port_id: str) -> dict:
        if not self.location_provider.state_exists(state_code):
            raise ValueError("State not supported")

        if not self.location_provider.port_exists(state_code, port_id):
            raise ValueError("Port not supported")

        brazil_tz = ZoneInfo("America/Sao_Paulo")
        now = datetime.now(brazil_tz)

        tides = self.tide_provider.get_tides(
            harbor_id=port_id,
            month=now.month,
            days=f"{now.day}-{now.day + 1}"
        )

        next_change = self.tide_finder.find_next(tides, now)
        normalized_level = round(next_change.level, 1)

        message = self.ai_provider.generate_tide_message(
            tide_type=next_change.type,
            level=normalized_level,
            time=next_change.time.strftime("%H:%M")
        )

        return {
            "state": state_code.lower(),
            "port_id": port_id,
            "current_time": now.strftime("%H:%M"),
            "next_tide_change": {
                "time": next_change.time.strftime("%H:%M"),
                "level": next_change.level,
                "type": next_change.type
            },
            "message": message
        }

