from hypothesis import given
from hypothesis import strategies as st

from fit3155.wk04.src.NaiveSuffixTree import NaiveSuffixTree
from fit3155.wk04.src.Ukkonen01Naive import UkkonenNaive
from fit3155.wk04.src.Ukkonen02SuffixLinks import UkkonenSuffixLinks
from fit3155.wk04.src.Ukkonen03SkipCount import UkkonenSkipCount
from fit3155.wk04.src.Ukkonen04ShowStopper import UkkonenShowStopper
from fit3155.wk04.src.Ukkonen05RapidLeafExtension import (
    UkkonenRapidLeafExtension,
)
from fit3155.wk04.src._suffix_tree_rendering import render_suffix_tree
from fit3155.wk04.tests._serialize import _serialize

# --- Helpers ---


def _is_rule_1(extension_point) -> bool:
    """Rule 1 iff extension point is AtNode at a leaf."""
    return hasattr(extension_point, "node") and extension_point.node.is_leaf


class _RecordingShowStopper(UkkonenShowStopper):
    """ShowStopper that logs whether each extension was a Rule 1.
    Used as the oracle for what rapid should be skipping."""

    def __init__(self, S: str):
        self.log: list[tuple[int, int, bool]] = []  # (i, j, was_rule_1)
        super().__init__(S)

    def _apply_extension(self, extension_point, j, i):
        is_r1 = _is_rule_1(extension_point)
        rule_3 = super()._apply_extension(extension_point, j, i)
        self.log.append((i, j, is_r1))
        return rule_3


class _RecordingRapid(UkkonenRapidLeafExtension):
    """Rapid that logs (i, j) per explicit extension, plus snapshots
    of global_end and last_j around each extension for invariant checks."""

    def __init__(self, S: str):
        self.log: list[tuple[int, int]] = []
        self.global_end_at_apply: list[tuple[int, int]] = []
        self.last_j_progression: list[int] = []
        super().__init__(S)

    def _apply_extension(self, extension_point, j, i):
        self.global_end_at_apply.append((i, self.global_end))
        rule_3 = super()._apply_extension(extension_point, j, i)
        self.last_j_progression.append(self.last_j)
        self.log.append((i, j))
        return rule_3


class _RenderableRapid(UkkonenRapidLeafExtension):
    def __repr__(self) -> str:
        return render_suffix_tree(
            name=type(self).__name__,
            S=self.S,
            root=self.r,
            resolve_end=self._end,
        )


# --- Tests ---


# Tree structural correctness across all implementations
@given(st.text(alphabet="abc", max_size=100))
def test_tree_structure_matches_upto_05(S):
    S = S + "$"
    stnaive = NaiveSuffixTree(S)
    uknaive = UkkonenNaive(S)
    uksuff = UkkonenSuffixLinks(S)
    ukskipcount = UkkonenSkipCount(S)
    ukshowstopper = UkkonenShowStopper(S)
    ukrapid = UkkonenRapidLeafExtension(S)

    # All pre-rapid implementations store edge.end as a concrete int, so
    # the default resolver works. Rapid uses _end() to handle leaf edges.
    assert (
        _serialize(uknaive.r, S)
        == _serialize(uksuff.r, S)
        == _serialize(stnaive.r, S)
        == _serialize(ukskipcount.r, S)
        == _serialize(ukshowstopper.r, S)
        == _serialize(ukrapid.r, S, ukrapid._end)
    )


# Behavioral cross-check: rapid's per-phase explicit-extension log must
# equal showstopper's per-phase log with all Rule 1 entries removed.
# This proves rapid skips *exactly* the Rule 1 extensions and nothing more.
@given(st.text(alphabet="abc", max_size=50))
def test_rapid_skips_exactly_the_rule_1_extensions(S):
    S = S + "$"
    rapid = _RecordingRapid(S)
    ss = _RecordingShowStopper(S)

    # Group showstopper by phase, dropping Rule 1 entries
    ss_non_rule_1: dict[int, list[int]] = {}
    for i, j, r1 in ss.log:
        if not r1:
            ss_non_rule_1.setdefault(i, []).append(j)

    rapid_by_phase: dict[int, list[int]] = {}
    for i, j in rapid.log:
        rapid_by_phase.setdefault(i, []).append(j)

    for i in range(len(S)):
        rapid_js = rapid_by_phase.get(i, [])
        ss_js = ss_non_rule_1.get(i, [])
        assert rapid_js == ss_js, (
            f"phase {i}: rapid did {rapid_js}, "
            f"showstopper (non-Rule-1) did {ss_js}"
        )


# Optimization fires on known inputs (guards against a silent no-op
# where rapid just runs every extension explicitly).
def test_rapid_does_strictly_fewer_extensions_than_showstopper():
    for S in ["abcabc$", "ababab$", "aaaa$", "mississippi$"]:
        rapid = _RecordingRapid(S)
        ss = _RecordingShowStopper(S)
        assert len(rapid.log) < len(ss.log), (
            f"S={S!r}: rapid did {len(rapid.log)} extensions, "
            f"showstopper did {len(ss.log)} - rapid optimization "
            f"not firing"
        )


# globalEnd must equal the current phase index at every extension apply.
# This is the heart of the implicit Rule 1 trick: leaf edges read globalEnd,
# and globalEnd is set to i at the start of phase i.
@given(st.text(alphabet="abc", min_size=1, max_size=50))
def test_global_end_equals_i_during_phase_i(S):
    S = S + "$"
    rapid = _RecordingRapid(S)

    for i, ge in rapid.global_end_at_apply:
        assert ge == i, f"phase {i}: global_end was {ge}, expected {i}"


# last_j is monotonically non-decreasing across all extensions.
@given(st.text(alphabet="abc", min_size=1, max_size=50))
def test_last_j_monotonic_non_decreasing(S):
    S = S + "$"
    rapid = _RecordingRapid(S)

    progression = rapid.last_j_progression
    for prev, curr in zip(progression, progression[1:]):
        assert curr >= prev, f"last_j decreased: {prev} -> {curr}"


# By the end of construction, every suffix has been created by some
# Rule 2, so last_j must equal n - 1 (zero-indexed: the last j).
@given(st.text(alphabet="abc", min_size=1, max_size=50))
def test_last_j_reaches_n_minus_1(S):
    S = S + "$"
    rapid = UkkonenRapidLeafExtension(S)

    assert rapid.last_j == len(S) - 1, (
        f"last_j={rapid.last_j}, expected {len(S) - 1} "
        f"(every suffix should have been created via Rule 2)"
    )


def test_repr_resolves_rapid_leaf_global_end():
    rapid = _RenderableRapid("abac$")
    rendered = repr(rapid)

    assert "unreachable (tree malformed)" not in rendered
    assert "S[4..-1]" not in rendered
    assert "S[4..4]" in rendered


def test_rapid_algorithm_still_uses_leaf_end_sentinel():
    rapid = UkkonenRapidLeafExtension("abac$")
    leaf_edges = [
        edge
        for node in [
            rapid.r,
            *(edge.child for edge in rapid.r.outgoing if edge),
        ]
        for edge in node.outgoing
        if edge is not None and edge.child.is_leaf
    ]

    assert any(edge.end == -1 for edge in leaf_edges)
