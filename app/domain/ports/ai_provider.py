from abc import ABC, abstractmethod

class AIProvider(ABC):

    @abstractmethod
    def generate_tide_message(
        self,
        tide_type: str,
        level: float,
        time: str
    ) -> str:
        pass
