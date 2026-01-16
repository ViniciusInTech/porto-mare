from typing import List
from app.domain.models.port import Port
from app.domain.ports.location_provider import LocationProvider

class ListPortsUseCase:

    def __init__(self, location_provider: LocationProvider):
        self.location_provider = location_provider

    def execute(self, state_code: str) -> List[Port]:
        if not self.location_provider.state_exists(state_code):
            raise ValueError("State not supported")

        return self.location_provider.list_ports_by_state(state_code)
