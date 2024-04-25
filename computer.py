from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Computer:

    name: str
    hacking_difficulty: int
    hacked_value: int
    risk_factor: float

    def __eq__(self, other: Computer) -> bool:
        return (self.hacking_difficulty, self.risk_factor, self.name) == (other.hacking_difficulty, other.risk_factor, other.name)
    
    def __gt__(self, other: Computer) -> bool:
        return (self.hacking_difficulty, self.risk_factor, self.name) > (other.hacking_difficulty, other.risk_factor, other.name)
    
    def __lt__(self, other: Computer) -> bool:
        return (self.hacking_difficulty, self.risk_factor, self.name) < (other.hacking_difficulty, other.risk_factor, other.name)
        
    def __le__(self, other: Computer) -> bool:
        return (self.hacking_difficulty, self.risk_factor, self.name) <= (other.hacking_difficulty, other.risk_factor, other.name)

    def __ge__(self, other: Computer) -> bool:
        return (self.hacking_difficulty, self.risk_factor, self.name) >= (other.hacking_difficulty, other.risk_factor, other.name)