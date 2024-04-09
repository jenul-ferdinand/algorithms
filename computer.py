from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Computer:

    name: str
    hacking_difficulty: int
    hacked_value: int
    risk_factor: float
