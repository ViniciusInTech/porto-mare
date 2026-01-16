from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Tide:
    time: datetime
    level: float
    type: str
