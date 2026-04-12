from dataclasses import dataclass, field


@dataclass
class BMOutput:
    """
    Boyer Moore Algorithm Output
    
    Attributes:
        match_positions: Array of positions where matches were made in the 
        original string

        matches: Count of pattern matches to the given string

        comparisons: Count of comparisons made in total

        shifts: Count of bad character shifts
    """
    match_positions: list[int] = field(default_factory=list)
    matches: int = 0
    comparisons: int = 0
    shifts: int = 0
    goodsuffix_array: list[int] = field(default_factory=list)
