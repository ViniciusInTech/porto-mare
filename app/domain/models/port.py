from dataclasses import dataclass

@dataclass(frozen=True)
class Port:
    id: int
    name: str
    state_code: str
