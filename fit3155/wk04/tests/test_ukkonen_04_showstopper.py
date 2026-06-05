from hypothesis import given
from hypothesis import strategies as st

from fit3155.wk04.src.NaiveSuffixTree import NaiveSuffixTree
from fit3155.wk04.src.Ukkonen01Naive import UkkonenNaive
from fit3155.wk04.src.Ukkonen02SuffixLinks import (
    UkkonenSuffixLinks,
)
from fit3155.wk04.src.Ukkonen03SkipCount import UkkonenSkipCount
from fit3155.wk04.src.Ukkonen04ShowStopper import (
    Edge,
    ExtensionPoint,
    Node,
    UkkonenShowStopper,
)
from fit3155.wk04.tests._serialize import _serialize


def _detect_rule_3(extension_point: ExtensionPoint, S: str, i: int) -> bool:
    """Definition-based detection: works on either implementation's
    AtNode/MidEdge (they're separate dataclasses but duck-compatible)."""
    if hasattr(extension_point, "node"):
        # AtNode: Rule 3 iff at an internal node that already has an
        # outgoing edge starting with S[i]
        u: Node = extension_point.node
        return (not u.is_leaf) and (u.find_edge(S[i]) is not None)
    # MidEdge: Rule 3 iff the next char on the edge equals S[i]
    edge: Edge = extension_point.edge
    return S[edge.start + extension_point.chars_into_edge] == S[i]


class _RecordingNaive(UkkonenNaive):
    def __init__(self, S: str):
        self.log: list[tuple[int, int, bool]] = []
        super().__init__(S)

    def _apply_extension(
        self, extension_point: ExtensionPoint, j: int, i: int
    ) -> bool:
        rule_3 = _detect_rule_3(extension_point, self.S, i)
        super()._apply_extension(extension_point, j, i)
        self.log.append((i, j, rule_3))


class _RecordingShowStopper(UkkonenShowStopper):
    def __init__(self, S: str):
        self.log: list[tuple[int, int, bool]] = []
        super().__init__(S)

    def _apply_extension(
        self, extension_point: ExtensionPoint, j: int, i: int
    ) -> bool:
        rule_3 = _detect_rule_3(extension_point, self.S, i)
        super()._apply_extension(extension_point, j, i)
        self.log.append((i, j, rule_3))
        return rule_3


# Tree correctness
@given(st.text(alphabet="abc", max_size=100))
def test_tree_structure_matches_upto_04(S):
    S = S + "$"
    stnaive = NaiveSuffixTree(S)
    uknaive = UkkonenNaive(S)
    uknaiver = _RecordingNaive(S)
    uksuff = UkkonenSuffixLinks(S)
    ukskipcount = UkkonenSkipCount(S)
    ukshowstopper = UkkonenShowStopper(S)
    ukshowstopperr = _RecordingShowStopper(S)
    assert (
        _serialize(uknaive.r, S)
        == _serialize(uksuff.r, S)
        == _serialize(stnaive.r, S)
        == _serialize(ukskipcount.r, S)
        == _serialize(ukshowstopper.r, S)
        == _serialize(uknaiver.r, S)
        == _serialize(ukshowstopperr.r, S)
    )


@given(st.text(alphabet="abc", max_size=50))
def test_showstopper_halts_phase_at_first_rule_3(S):
    S = S + "$"
    ST = _RecordingShowStopper(S)

    phases: dict[int, list[tuple[int, bool]]] = {}
    for i, j, r3 in ST.log:
        phases.setdefault(i, []).append((j, r3))

    for i in range(len(S)):
        entries = phases.get(i, [])
        assert entries, f"phase {i} ran zero extensions"

        js = [j for j, _ in entries]
        assert js == list(range(js[-1] + 1)), (
            f"phase {i} visited non-sequential extensions {js}"
        )

        first_r3 = next((j for j, r3 in entries if r3), None)

        if first_r3 is not None:
            assert js[-1] == first_r3, (
                f"phase {i}: Rule 3 fired at j={first_r3} but phase "
                f"ran to j={js[-1]} — showstopper didn't fire"
            )
        else:
            assert js[-1] == i, (
                f"phase {i}: no Rule 3 but stopped at j={js[-1]} "
                f"(expected j={i})"
            )


def test_showstopper_actually_skips_extensions():
    # "ababab$": phase 4 hits Rule 3 mid-edge at j=2, skipping j=3 and j=4.
    ST = _RecordingShowStopper("ababab$")

    last_j_per_phase: dict[int, int] = {}
    for i, j, _ in ST.log:
        last_j_per_phase[i] = max(last_j_per_phase.get(i, -1), j)

    saved_some = any(last_j < i for i, last_j in last_j_per_phase.items())
    assert saved_some, "showstopper never skipped any extensions"


def _group_by_phase(
    log: list[tuple[int, int, bool]],
) -> dict[int, list[tuple[int, bool]]]:
    by_phase: dict[int, list[tuple[int, bool]]] = {}
    for i, j, r3 in log:
        by_phase.setdefault(i, []).append((j, r3))
    return by_phase


@given(st.text(alphabet="abc", max_size=100))
def test_showstopper_stops_exactly_where_naive_first_sees_rule_3(S):
    S = S + "$"
    naive = _RecordingNaive(S)
    ss = _RecordingShowStopper(S)

    naive_phases = _group_by_phase(naive.log)
    ss_phases = _group_by_phase(ss.log)

    for i in range(len(S)):
        naive_entries = naive_phases.get(i, [])
        ss_entries = ss_phases.get(i, [])

        # Oracle: first Rule 3 Naive saw in this phase (None if never)
        first_r3 = next((j for j, r3 in naive_entries if r3), None)

        ss_js = [j for j, _ in ss_entries]
        expected = (
            list(range(first_r3 + 1))
            if first_r3 is not None
            else list(range(i + 1))
        )
        assert ss_js == expected, (
            f"phase {i}: Naive's first Rule 3 was j={first_r3}, "
            f"expected ShowStopper to visit {expected}, got {ss_js}"
        )
