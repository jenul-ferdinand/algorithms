from dataclasses import dataclass, field


@dataclass
class ZalgOutput:
    """
    Output of the Z Algorithm

    Attributes:
        z_array: The resulting z array of length n.

        comparisons: Total character comparisons performed.

        zbox_updates: How many times the z-box (left, right) pointers was
        advanced (case 1 matches & case 2 extensions).

        case1_times: How many times Case 1 executed.

        case2_times: How many times Case 2 executed.

        reuse_times: How many times a z-value was reused from inside the current
        z-box (case 2a hits).

        clamp_times: How many times we use the remaining distance from k to R.

        extensions: How many times did we naively extend from R onwards, in
        general, not specific naive comparisons for each character.
    """

    z_array: list[int] = field(default_factory=list)
    comparisons: int = 0
    zbox_updates: int | None = 0
    case1_times: int = 0
    case2_times: int | None = 0
    reuse_times: int | None = 0
    clamp_times: int | None = 0
    extensions: int | None = 0
    extensions: int | None = 0
    extensions: int | None = 0
