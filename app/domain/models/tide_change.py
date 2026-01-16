from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TideChange:
    time: datetime
    level: float
    type: str
