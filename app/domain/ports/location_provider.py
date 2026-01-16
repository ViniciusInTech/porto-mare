from abc import ABC, abstractmethod
from typing import List
from app.domain.models.state import State
from app.domain.models.port import Port

class LocationProvider(ABC):

    @abstractmethod
    def list_states(self) -> List[State]:
        pass

    @abstractmethod
    def list_ports_by_state(self, state_code: str) -> List[Port]:
        pass

    @abstractmethod
    def state_exists(self, state_code: str) -> bool:
        pass

    @abstractmethod
    def port_exists(self, state_code: str, port_code: str) -> bool:
        pass
