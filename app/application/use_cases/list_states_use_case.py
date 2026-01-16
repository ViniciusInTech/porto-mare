from typing import List

from app.domain.models.brazilian_state import BrazilianState
from app.domain.models.state import State
from app.domain.ports.location_provider import LocationProvider

class ListStatesUseCase:

    def __init__(self, location_provider: LocationProvider):
        self.location_provider = location_provider

    def execute(self) -> List[State]:
        states = self.location_provider.list_states()

        return [
            State(
                code=state.code,
                name=BrazilianState.name_from_code(state.code)
            )
            for state in states
        ]
