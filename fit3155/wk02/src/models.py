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

        matched_comparisons: Count of comparisons that matched in total.

        shifts: Count of shifts in total

        gs_shifts: Count of the shifts caused by the good suffix rule

        mp_shifts: Count of the shifts caused by the matched prefix rule

        bcr_shifts: Count of the shifts caused by the bad character rule

        z_suffix: Z suffix array

        goodsuffix: Good suffix array

        galil_skips: How many times we skipped comparisons based on galil's
        optimisation rule
    """

    match_positions: list[int] = field(default_factory=list)
    matches: int = 0

    comparisons: int = 0
    matched_comparisons: int = 0

    total_shifts: int = 0
    gs_shifts: int = 0
    mp_shifts: int = 0
    bcr_shifts: int = 0

    z_suffix: list[int] = field(default_factory=list)
    goodsuffix: list[int] = field(default_factory=list)
    mp: list[int] = field(default_factory=list)

    galil_skips: int = 0
