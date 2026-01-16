from dataclasses import dataclass

@dataclass(frozen=True)
class State:
    code: str
    name: str
