from datetime import datetime, timedelta, timezone
from typing import List, Optional
from app.domain.models.state import State
from app.domain.models.port import Port
from app.domain.ports.location_provider import LocationProvider

class CachedLocationProvider(LocationProvider):

    def __init__(self, source: LocationProvider, ttl_minutes: int = 30):
        self.source = source
        self.ttl = timedelta(minutes=ttl_minutes)
        self.states_cache: Optional[List[State]] = None
        self.states_cache_time: Optional[datetime] = None
        self.ports_cache: dict[str, tuple[List[Port], datetime]] = {}

    def list_states(self) -> List[State]:
        now = datetime.now(timezone.utc)

        if (
            self.states_cache
            and self.states_cache_time
            and now - self.states_cache_time < self.ttl
        ):
            return self.states_cache

        states = self.source.list_states()
        self.states_cache = states
        self.states_cache_time = now
        return states

    def list_ports_by_state(self, state_code: str) -> List[Port]:
        now = datetime.now(timezone.utc)
        cached = self.ports_cache.get(state_code)

        if cached and now - cached[1] < self.ttl:
            return cached[0]

        ports = self.source.list_ports_by_state(state_code)
        self.ports_cache[state_code] = (ports, now)
        return ports

    def state_exists(self, state_code: str) -> bool:
        return any(
            state.code == state_code.lower()
            for state in self.list_states()
        )

    def port_exists(self, state_code: str, port_code: str) -> bool:
        return any(
            port.id == port_code.lower()
            for port in self.list_ports_by_state(state_code)
        )
