from typing import List
import httpx
from app.domain.models.state import State
from app.domain.models.port import Port
from app.domain.ports.location_provider import LocationProvider
from app.config.settings import settings

class ApiLocationProvider(LocationProvider):

    def __init__(self):
        self.base_url = f"{settings.tide_api_base_url}/api/{settings.tide_api_version}"

    def list_states(self) -> List[State]:
        response = httpx.get(f"{self.base_url}/states", timeout=10)
        response.raise_for_status()
        payload = response.json()

        return [
            State(code=code.lower(), name="")
            for code in payload["data"]
        ]

    def list_ports_by_state(self, state_code: str):
        response = httpx.get(
            f"{self.base_url}/harbor_names/{state_code.lower()}",
            timeout=10
        )
        response.raise_for_status()
        payload = response.json()

        return [
            Port(
                id=item["id"],
                name=item["harbor_name"],
                state_code=state_code.lower()
            )
            for item in payload["data"]
        ]

    def state_exists(self, state_code: str) -> bool:
        return any(
            state.code == state_code.lower()
            for state in self.list_states()
        )

    def port_exists(self, state_code: str, port_code: str) -> bool:
        return any(
            port.code == port_code.lower()
            for port in self.list_ports_by_state(state_code)
        )
