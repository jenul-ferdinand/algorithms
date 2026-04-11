from dataclasses import dataclass, field


@dataclass
class BMOutput:
    match_positions: list[int] = field(default_factory=list)
    matches: int = 0
    compares: int = 0
    shifts: int = 0
