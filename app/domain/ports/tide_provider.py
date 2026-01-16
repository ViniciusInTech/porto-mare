from abc import ABC, abstractmethod
from typing import List
from app.domain.models.tide import Tide

class TideProvider(ABC):

    @abstractmethod
    def get_tides(
        self,
        harbor_id: str,
        month: int,
        days: str
    ) -> List[Tide]:
        pass
