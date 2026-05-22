"""Robust regression tests for validation, lookup, equality, and overlap semantics."""

from __future__ import annotations

import random
from typing import Any, Dict, List, cast

import pytest

from range_key_dict import RangeEntry, RangeKey, RangeKeyDict
from range_key_dict.range_key_dict import _VALID_OVERLAP_STRATEGIES


def _brute_force_value(
    entries: List[RangeEntry],
    number: float,
    overlap_strategy: str,
) -> Any:
    """Linear-scan reference implementation mirroring public lookup semantics."""
    matches = [e for e in entries if e.contains(number)]
    if not matches:
        raise KeyError(number)
    if len(matches) == 1:
        return matches[0].value
    if overlap_strategy == "first":
        return min(matches, key=lambda e: e.insertion_order).value
    if overlap_strategy == "last":
        return max(matches, key=lambda e: e.insertion_order).value
    if overlap_strategy == "shortest":
        return min(matches, key=lambda e: (e.length(), e.insertion_order)).value
    if overlap_strategy == "longest":
        return max(matches, key=lambda e: (e.length(), e.insertion_order)).value
    raise ValueError(f"unexpected strategy {overlap_strategy!r}")


def _build_non_overlapping_ranges(rng: random.Random, count: int) -> Dict[RangeKey, str]:
    """Build gap-separated half-open ranges."""
    ranges: Dict[RangeKey, str] = {}
    cursor = 0
    for i in range(count):
        gap = rng.randint(0, 3)
        cursor += gap
        width = rng.randint(1, 25)
        ranges[(cursor, cursor + width)] = f"r{i}"
        cursor += width
    return ranges


class TestBoundAndKeyValidation:
    """Construction and mutation reject invalid bounds and keys early."""

    @pytest.mark.parametrize(
        "bad_key",
        [
            (True, 10),
            (0, False),
            (True, True),
        ],
    )
    def test_bool_bounds_rejected_on_init(self, bad_key: object) -> None:
        with pytest.raises(TypeError, match="bool"):
            RangeKeyDict(cast(Any, {bad_key: "x"}))

    @pytest.mark.parametrize(
        "bad_key",
        [
            (True, 10),
            (0, False),
        ],
    )
    def test_bool_bounds_rejected_on_setitem(self, bad_key: object) -> None:
        rkd = RangeKeyDict()
        with pytest.raises(TypeError, match="bool"):
            rkd[cast(Any, bad_key)] = "x"

    @pytest.mark.parametrize(
        "bad_end",
        [float("inf"), float("-inf"), float("nan")],
    )
    def test_non_finite_bounds_rejected(self, bad_end: float) -> None:
        with pytest.raises(ValueError, match="finite"):
            RangeKeyDict({(0, bad_end): "x"})

    @pytest.mark.parametrize(
        "invalid_key,match",
        [
            (42, "2-tuple"),
            ((0, 100, 200), "2-tuple"),
            ((0,), "2-tuple"),
        ],
    )
    def test_non_tuple_keys_rejected(self, invalid_key: object, match: str) -> None:
        with pytest.raises(TypeError, match=match):
            RangeKeyDict(cast(Any, {invalid_key: "x"}))

    def test_list_key_rejected_at_construction(self) -> None:
        with pytest.raises(TypeError):
            RangeKeyDict(cast(Any, {[0, 100]: "x"}))

    def test_setitem_rejects_string_end_bound(self) -> None:
        rkd = RangeKeyDict()
        with pytest.raises(TypeError, match="Range end"):
            rkd[cast(Any, (0, "ten"))] = "x"


class TestLookupValidation:
    """Lookup keys must be int or float, not bool or other types."""

    @pytest.mark.parametrize(
        "bad_query",
        [float("nan"), float("inf"), float("-inf")],
    )
    def test_non_finite_lookup_rejected(self, bad_query: float) -> None:
        rkd = RangeKeyDict({(0, 100): "x"})
        with pytest.raises(ValueError, match="finite"):
            _ = rkd[bad_query]

    @pytest.mark.parametrize(
        "bad_query",
        [float("nan"), float("inf"), float("-inf")],
    )
    def test_non_finite_lookup_rejected_for_contains(self, bad_query: float) -> None:
        rkd = RangeKeyDict({(0, 100): "x"})
        with pytest.raises(ValueError, match="finite"):
            _ = bad_query in rkd

    def test_non_finite_lookup_rejected_for_get(self) -> None:
        rkd = RangeKeyDict({(0, 100): "x"})
        with pytest.raises(ValueError, match="finite"):
            rkd.get(float("nan"))

    @pytest.mark.parametrize(
        "bad_query",
        ["50", None, [], {}, object()],
    )
    def test_invalid_lookup_type_rejected(self, bad_query: object) -> None:
        rkd = RangeKeyDict({(0, 100): "x"})
        with pytest.raises(TypeError, match="int or float"):
            _ = rkd[cast(Any, bad_query)]

    @pytest.mark.parametrize(
        "bad_query",
        ["50", None],
    )
    def test_invalid_lookup_type_rejected_for_contains(self, bad_query: object) -> None:
        rkd = RangeKeyDict({(0, 100): "x"})
        with pytest.raises(TypeError, match="int or float"):
            _ = cast(Any, bad_query) in rkd

    def test_keyerror_uses_query_value(self) -> None:
        rkd = RangeKeyDict({(0, 10): "x"})
        with pytest.raises(KeyError) as exc_info:
            _ = rkd[99]
        assert exc_info.value.args[0] == 99


class TestGetAndNoneValues:
    """get() behavior with stored None vs missing keys."""

    def test_get_returns_stored_none(self) -> None:
        rkd = RangeKeyDict({(0, 10): None})
        assert rkd.get(5) is None

    def test_get_default_used_when_missing(self) -> None:
        rkd = RangeKeyDict({(0, 10): "a"})
        sentinel = object()
        assert rkd.get(50, sentinel) is sentinel

    def test_get_default_none_distinct_from_missing(self) -> None:
        rkd = RangeKeyDict({(0, 10): "a"})
        assert rkd.get(50, None) is None
        assert rkd.get(50) is None


class TestEqualityRobustness:
    """__eq__ compares values and overlap strategy, not insertion order."""

    def test_eq_false_when_overlap_strategy_differs(self) -> None:
        a = RangeKeyDict({(0, 100): "A"}, overlap_strategy="error")
        b = RangeKeyDict({(0, 100): "A"}, overlap_strategy="first")
        assert a != b

    def test_eq_false_when_values_differ(self) -> None:
        assert RangeKeyDict({(0, 100): "A"}) != RangeKeyDict({(0, 100): "B"})

    def test_eq_true_regardless_of_insertion_order(self) -> None:
        a = RangeKeyDict()
        a[(200, 300)] = "C"
        a[(0, 100)] = "A"
        b = RangeKeyDict({(0, 100): "A", (200, 300): "C"})
        assert a == b

    def test_eq_reflexive_and_notimplemented(self) -> None:
        rkd = RangeKeyDict({(0, 1): 0})
        assert rkd == rkd
        assert rkd.__eq__(3) is NotImplemented
        assert rkd != 3


class TestBisectLookupExhaustive:
    """Bisect path matches brute-force reference on varied layouts."""

    def test_empty_dict_never_matches(self) -> None:
        rkd = RangeKeyDict()
        assert 0 not in rkd
        assert rkd.get(0, "missing") == "missing"

    @pytest.mark.parametrize("query", [0, 50, 99, 100, 199, 200, 201])
    def test_adjacent_range_boundary_queries(self, query: float) -> None:
        rkd = RangeKeyDict({(0, 100): "A", (100, 200): "B"})
        entries = list(rkd._entries)  # noqa: SLF001 — reference parity
        try:
            expected = _brute_force_value(entries, query, "error")
        except KeyError:
            assert query not in rkd
            with pytest.raises(KeyError):
                _ = rkd[query]
        else:
            assert rkd[query] == expected

    def test_open_ended_lower_bound_matches_many_starts(self) -> None:
        """Many ranges share (-inf, end); all should match deep negative queries."""
        rkd = RangeKeyDict(
            {
                (None, -100): "a",
                (None, 0): "b",
                (None, 100): "c",
            },
            overlap_strategy="first",
        )
        assert rkd[-1000] == "a"
        entries = list(rkd._entries)  # noqa: SLF001
        assert _brute_force_value(entries, -50, "first") == rkd[-50]

    def test_random_non_overlapping_lookups_match_brute_force(self) -> None:
        rng = random.Random(20260522)
        for _trial in range(40):
            raw = _build_non_overlapping_ranges(rng, rng.randint(1, 40))
            rkd = RangeKeyDict(raw)
            entries = list(rkd._entries)  # noqa: SLF001
            min_start = min(float("-inf") if e.start is None else e.start for e in entries)
            max_end = max(float("inf") if e.end is None else e.end for e in entries)
            for _ in range(30):
                if rng.random() < 0.15:
                    query = rng.uniform(min_start - 50, max_end + 50)
                else:
                    pick = rng.choice(entries)
                    lo = float("-inf") if pick.start is None else pick.start
                    hi = float("inf") if pick.end is None else pick.end
                    if pick.is_point():
                        assert pick.start is not None
                        query = float(pick.start)
                    else:
                        query = rng.uniform(lo, hi - 1e-9 if hi != float("inf") else hi)

                try:
                    expected = _brute_force_value(entries, query, "error")
                except KeyError:
                    assert query not in rkd
                else:
                    assert rkd[query] == expected

    @pytest.mark.parametrize("strategy", list(_VALID_OVERLAP_STRATEGIES[1:]))
    def test_overlapping_random_queries_match_brute_force(self, strategy: str) -> None:
        rng = random.Random(strategy.__hash__() & 0xFFFF)
        ranges: Dict[RangeKey, str] = {
            (0, 200): "outer",
            (rng.randint(20, 80), rng.randint(120, 180)): "inner",
            (50, 50): "point",
        }
        rkd = RangeKeyDict(ranges, overlap_strategy=cast(Any, strategy))
        entries = list(rkd._entries)  # noqa: SLF001
        for query in [0, 25, 50, 75, 100, 150, 199]:
            assert rkd[query] == _brute_force_value(entries, query, strategy)


class TestLargeIntegerLookups:
    """Integer lookups above 2**53 must not lose precision."""

    def test_point_range_above_float53_exact_match(self) -> None:
        n = 9007199254740993  # 2**53 + 1
        rkd = RangeKeyDict({(n, n): "hit"})
        assert rkd[n] == "hit"
        assert n in rkd

    def test_adjacent_ranges_above_float53(self) -> None:
        a = 9007199254740992  # 2**53
        b = 9007199254740993  # 2**53 + 1
        rkd = RangeKeyDict({(a, a + 1): "first", (b, b + 1): "second"})
        assert rkd[a] == "first"
        assert rkd[b] == "second"


class TestOverlapTieBreaking:
    """Equal-length overlaps resolve by insertion_order for shortest/longest."""

    def test_shortest_tie_uses_earlier_insertion(self) -> None:
        rkd = RangeKeyDict(
            {
                (0, 100): "wide",
                (25, 75): "narrow_a",
                (30, 80): "narrow_b",
            },
            overlap_strategy="shortest",
        )
        assert rkd[50] == "narrow_a"

    def test_longest_tie_uses_later_insertion(self) -> None:
        rkd = RangeKeyDict(
            {
                (0, 100): "wide",
                (25, 75): "narrow_a",
                (30, 80): "narrow_b",
            },
            overlap_strategy="longest",
        )
        assert rkd[50] == "wide"

    def test_equal_width_pair_shortest_prefers_first_inserted(self) -> None:
        rkd = RangeKeyDict(overlap_strategy="shortest")
        rkd[(0, 50)] = "first"
        rkd[(10, 60)] = "second"
        assert rkd[25] == "first"

    def test_equal_width_pair_longest_prefers_last_inserted(self) -> None:
        rkd = RangeKeyDict(overlap_strategy="longest")
        rkd[(0, 50)] = "first"
        rkd[(10, 60)] = "second"
        assert rkd[25] == "second"


class TestFirstLastAfterDeleteReadd:
    """Deleting and re-adding a range assigns a new insertion_order."""

    def test_last_strategy_changes_after_del_and_readd(self) -> None:
        rkd = RangeKeyDict({(0, 100): "outer"}, overlap_strategy="last")
        rkd[(40, 60)] = "inner"
        assert rkd[50] == "inner"
        del rkd[(40, 60)]
        rkd[(40, 60)] = "inner_again"
        assert rkd[50] == "inner_again"
        rkd[(45, 55)] = "newest"
        assert rkd[50] == "newest"


class TestOverlapStrategyMatrix:
    """Pinned expectations for all strategies at a single overlapping point."""

    @pytest.fixture
    def triple_overlap(self) -> RangeKeyDict:
        return RangeKeyDict(
            {
                (0, 100): "first",
                (25, 75): "second",
                (40, 60): "third",
            },
            overlap_strategy="first",
        )

    def test_first_last_shortest_longest_at_shared_point(
        self, triple_overlap: RangeKeyDict
    ) -> None:
        assert triple_overlap[50] == "first"

        last = RangeKeyDict(
            {
                (0, 100): "first",
                (25, 75): "second",
                (40, 60): "third",
            },
            overlap_strategy="last",
        )
        assert last[50] == "third"

        shortest = RangeKeyDict(
            {
                (0, 100): "first",
                (25, 75): "second",
                (40, 60): "third",
            },
            overlap_strategy="shortest",
        )
        assert shortest[50] == "third"

        longest = RangeKeyDict(
            {
                (0, 100): "first",
                (25, 75): "second",
                (40, 60): "third",
            },
            overlap_strategy="longest",
        )
        assert longest[50] == "first"


class TestMutableOperationsRobustness:
    """setitem/delitem preserve invariants and lookup correctness."""

    def test_setitem_rejects_overlap_under_error_strategy(self) -> None:
        rkd = RangeKeyDict({(0, 100): "A"})
        with pytest.raises(ValueError, match="overlaps"):
            rkd[(50, 150)] = "B"

    def test_setitem_allows_overlap_when_strategy_permits(self) -> None:
        rkd = RangeKeyDict({(0, 100): "A"}, overlap_strategy="last")
        rkd[(50, 150)] = "B"
        assert rkd[75] == "B"
        assert len(rkd) == 2

    def test_setitem_resort_maintains_lookup_after_out_of_order_adds(self) -> None:
        rkd = RangeKeyDict(overlap_strategy="first")
        rkd[(200, 300)] = "high"
        rkd[(0, 100)] = "low"
        assert list(rkd.keys()) == [(0, 100), (200, 300)]
        assert rkd[50] == "low"
        assert rkd[250] == "high"

    def test_delitem_removes_lookup_until_readded(self) -> None:
        rkd = RangeKeyDict({(0, 10): "a", (20, 30): "b"})
        del rkd[(0, 10)]
        assert 5 not in rkd
        rkd[(0, 10)] = "restored"
        assert rkd[5] == "restored"


class TestRangeEntryOverlapSemantics:
    """Direct RangeEntry tests for overlap detection edge cases."""

    def test_half_open_touching_ranges_do_not_overlap(self) -> None:
        a = RangeEntry(0, 10, "a")
        b = RangeEntry(10, 20, "b")
        assert not a.overlaps(b)
        assert not b.overlaps(a)

    def test_open_ended_ranges_overlap_finite_interval(self) -> None:
        unbounded = RangeEntry(None, None, "all")
        finite = RangeEntry(0, 10, "small")
        assert unbounded.overlaps(finite)
        assert finite.overlaps(unbounded)

    def test_point_on_half_open_upper_boundary_no_overlap(self) -> None:
        interval = RangeEntry(0, 10, "i")
        point = RangeEntry(10, 10, "p")
        assert not interval.overlaps(point)
        assert not point.overlaps(interval)
