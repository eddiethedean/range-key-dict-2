"""Tests for point ranges (start == end) — single precise values."""

import math

import pytest

from range_key_dict import RangeEntry, RangeKeyDict


class TestRangeEntryPointSemantics:
    """Unit tests for RangeEntry point vs half-open behavior."""

    def test_is_point_true_for_equal_finite_bounds(self):
        assert RangeEntry(1, 1, "x").is_point()
        assert RangeEntry(3.5, 3.5, "x").is_point()
        assert RangeEntry(0.0, 0.0, "x").is_point()

    def test_is_point_false_for_intervals_and_unbounded(self):
        assert not RangeEntry(0, 10, "x").is_point()
        assert not RangeEntry(None, 10, "x").is_point()
        assert not RangeEntry(10, None, "x").is_point()
        assert not RangeEntry(None, None, "x").is_point()

    def test_contains_point_exact_equality_only(self):
        entry = RangeEntry(10, 10, "ten")
        assert entry.contains(10)
        assert entry.contains(10.0)
        assert not entry.contains(9)
        assert not entry.contains(11)
        assert not entry.contains(10.0000001)

    def test_contains_half_open_unchanged(self):
        entry = RangeEntry(10, 20, "interval")
        assert entry.contains(10)
        assert entry.contains(19.999)
        assert not entry.contains(20)
        assert not entry.contains(9)

    def test_point_length_is_zero(self):
        assert RangeEntry(42, 42, "x").length() == 0

    def test_point_overlaps_interval_that_contains_value(self):
        point = RangeEntry(50, 50, "p")
        interval = RangeEntry(0, 100, "i")
        assert point.overlaps(interval)
        assert interval.overlaps(point)

    def test_point_does_not_overlap_interval_excluding_value(self):
        point = RangeEntry(10, 10, "p")
        # [0, 10) does not include 10
        assert not point.overlaps(RangeEntry(0, 10, "a"))
        # (10, 20) is half-open but includes its start, so it contains 10
        assert point.overlaps(RangeEntry(10, 20, "b"))

    def test_point_overlaps_interval_with_inclusive_start_at_value(self):
        point = RangeEntry(10, 10, "p")
        assert point.overlaps(RangeEntry(10, 20, "c"))

    def test_disjoint_points_do_not_overlap(self):
        assert not RangeEntry(1, 1, "a").overlaps(RangeEntry(2, 2, "b"))

    def test_coincident_points_overlap(self):
        a = RangeEntry(7, 7, "a")
        b = RangeEntry(7, 7, "b")
        assert a.overlaps(b)


class TestPointRangeLookup:
    """Lookup and membership for point keys in RangeKeyDict."""

    @pytest.mark.parametrize(
        "key,lookup,expected_in",
        [
            ((0, 0), 0, True),
            ((0, 0), 0.0, True),
            ((1, 1), 1, True),
            ((1.5, 1.5), 1.5, True),
            ((-3, -3), -3, True),
            ((10, 10.0), 10, True),  # equal bounds via int/float
        ],
    )
    def test_lookup_hits_point(self, key, lookup, expected_in):
        rkd = RangeKeyDict({key: "hit"})
        assert (lookup in rkd) is expected_in
        assert rkd[lookup] == "hit"

    @pytest.mark.parametrize(
        "key,miss",
        [
            ((5, 5), 4),
            ((5, 5), 6),
            ((5, 5), 5.1),
            ((0, 0), -1),
        ],
    )
    def test_lookup_misses_nearby(self, key, miss):
        rkd = RangeKeyDict({key: "hit"})
        assert miss not in rkd
        assert rkd.get(miss, "default") == "default"
        with pytest.raises(KeyError):
            _ = rkd[miss]

    def test_multiple_disjoint_points(self):
        rkd = RangeKeyDict(
            {
                (1, 1): "one",
                (2, 2): "two",
                (100, 100): "hundred",
            }
        )
        assert rkd[1] == "one"
        assert rkd[2] == "two"
        assert rkd[100] == "hundred"
        assert 50 not in rkd
        assert len(rkd) == 3

    def test_point_among_adjacent_half_open_ranges(self):
        """Point at 10 coexists with [0,10) and [10,20) when overlaps are allowed."""
        rkd = RangeKeyDict(
            {
                (0, 10): "low",
                (10, 10): "exact_ten",
                (10, 20): "high",
            },
            overlap_strategy="first",
        )
        assert rkd[9] == "low"
        assert rkd[10] == "exact_ten"  # point inserted before overlapping high range
        assert rkd[11] == "high"
        assert 10 in rkd

    def test_negative_zero_point(self):
        rkd = RangeKeyDict({(-0.0, -0.0): "zero"})
        assert rkd[0.0] == "zero"
        assert rkd[-0.0] == "zero"


class TestPointRangeDictInterface:
    """Mutable operations and dict API with point keys."""

    def test_setitem_and_update_point(self):
        rkd = RangeKeyDict()
        rkd[(3, 3)] = "three"
        assert rkd[3] == "three"
        rkd[(3, 3)] = "updated"
        assert rkd[3] == "updated"
        assert len(rkd) == 1
        assert rkd.keys() == [(3, 3)]

    def test_delitem_point(self):
        rkd = RangeKeyDict({(4, 4): "four"})
        del rkd[(4, 4)]
        assert len(rkd) == 0
        assert 4 not in rkd
        with pytest.raises(KeyError):
            del rkd[(4, 4)]

    def test_iter_and_items_include_point(self):
        rkd = RangeKeyDict({(1, 1): "a", (2, 3): "b"})
        assert list(rkd) == [(1, 1), (2, 3)]
        assert rkd.items() == [((1, 1), "a"), ((2, 3), "b")]

    def test_equality_with_points(self):
        a = RangeKeyDict({(1, 1): "x", (10, 20): "y"})
        b = RangeKeyDict({(10, 20): "y", (1, 1): "x"})
        assert a == b

    def test_repr_contains_point_key(self):
        rkd = RangeKeyDict({(7, 7): "lucky"})
        assert "(7, 7)" in repr(rkd)
        assert "lucky" in repr(rkd)


class TestPointRangeOverlaps:
    """Overlap detection and strategies involving point keys."""

    def test_error_strategy_rejects_point_inside_interval(self):
        with pytest.raises(ValueError, match="overlaps"):
            RangeKeyDict(
                {
                    (0, 100): "wide",
                    (50, 50): "midpoint",
                }
            )

    def test_error_strategy_rejects_interval_covering_point_on_setitem(self):
        rkd = RangeKeyDict({(0, 100): "wide"}, overlap_strategy="error")
        with pytest.raises(ValueError, match="overlaps"):
            rkd[(50, 50)] = "midpoint"

    def test_error_strategy_allows_point_outside_interval(self):
        rkd = RangeKeyDict(
            {
                (0, 10): "a",
                (20, 20): "b",
            }
        )
        assert rkd[20] == "b"
        assert 15 not in rkd

    def test_error_strategy_point_at_half_open_upper_bound_no_conflict(self):
        """(0, 10) and point 10 do not overlap under half-open semantics."""
        rkd = RangeKeyDict(
            {
                (0, 10): "a",
                (10, 10): "ten",
            }
        )
        assert rkd[9] == "a"
        assert rkd[10] == "ten"

    def test_error_strategy_rejects_point_at_interval_start(self):
        """Point 10 overlaps [10, 20) because half-open intervals include start."""
        with pytest.raises(ValueError, match="overlaps"):
            RangeKeyDict(
                {
                    (10, 10): "ten",
                    (10, 20): "high",
                }
            )

    def test_first_strategy_prefers_earlier_insertion_at_overlap(self):
        rkd = RangeKeyDict(
            {
                (0, 100): "wide",
                (50, 50): "point",
            },
            overlap_strategy="first",
        )
        assert rkd[50] == "wide"

        rkd_point_first = RangeKeyDict({(50, 50): "point"}, overlap_strategy="first")
        rkd_point_first[(0, 100)] = "wide"
        assert rkd_point_first[50] == "point"

    def test_last_strategy_prefers_later_inserted_at_overlap(self):
        rkd = RangeKeyDict({(0, 100): "wide"}, overlap_strategy="last")
        rkd[(50, 50)] = "point"
        assert rkd[50] == "point"

    def test_shortest_strategy_prefers_point_over_interval(self):
        rkd = RangeKeyDict(
            {
                (0, 100): "wide",
                (50, 50): "point",
            },
            overlap_strategy="shortest",
        )
        assert rkd[50] == "point"

    def test_longest_strategy_prefers_interval_over_point(self):
        rkd = RangeKeyDict(
            {
                (0, 100): "wide",
                (50, 50): "point",
            },
            overlap_strategy="longest",
        )
        assert rkd[50] == "wide"

    def test_shortest_among_point_and_nested_intervals(self):
        rkd = RangeKeyDict(
            {
                (0, 200): "outer",
                (40, 60): "inner",
                (50, 50): "needle",
            },
            overlap_strategy="shortest",
        )
        assert rkd[50] == "needle"
        assert rkd[25] == "outer"
        assert rkd[45] == "inner"

    def test_point_with_open_ended_range(self):
        rkd = RangeKeyDict(
            {
                (None, 100): "below",
                (100, 100): "exact",
                (100, None): "above",
            },
            overlap_strategy="first",
        )
        assert rkd[50] == "below"
        assert rkd[100] == "exact"
        assert rkd[150] == "above"

    def test_setitem_replaces_same_point_key_without_duplicate_entries(self):
        rkd = RangeKeyDict(overlap_strategy="first")
        rkd[(1, 1)] = "first"
        rkd[(1, 1)] = "second"
        assert rkd[1] == "second"
        assert len(rkd) == 1
        assert rkd.keys() == [(1, 1)]


class TestPointRangeConstruction:
    """Initialization and validation with point keys."""

    def test_from_initial_dict_issue_1_reproduction(self):
        rng = RangeKeyDict()
        rng[(1, 1)] = "one"
        assert rng[1] == "one"

    def test_initial_dict_with_only_points(self):
        rkd = RangeKeyDict({(i, i): str(i) for i in range(5)})
        for i in range(5):
            assert rkd[i] == str(i)
        assert 5 not in rkd

    def test_start_greater_than_end_still_rejected_for_points(self):
        with pytest.raises(ValueError, match="start.*must be.*end"):
            RangeKeyDict({(10, 5): "invalid"})

    def test_non_finite_bounds_rejected(self):
        """Non-finite float bounds are rejected at construction."""
        with pytest.raises(ValueError, match="finite"):
            RangeKeyDict({(math.inf, math.inf): "inf"})
        with pytest.raises(ValueError, match="finite"):
            RangeKeyDict({(float("nan"), 10): "n"})
