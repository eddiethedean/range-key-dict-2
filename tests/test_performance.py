"""Basic performance and scalability tests."""

from typing import Any, Dict, List, Tuple

import pytest

from range_key_dict import RangeKey, RangeKeyDict


def _lookup_cases() -> List[Tuple[RangeKeyDict, List[Tuple[float, Any]]]]:
    """Representative dicts and expected (query, value) pairs."""
    return [
        (
            RangeKeyDict({(0, 100): "A", (100, 200): "B", (200, 300): "C"}),
            [(50, "A"), (150, "B"), (250, "C"), (300, KeyError)],
        ),
        (
            RangeKeyDict({(None, 0): "neg", (0, 100): "mid", (100, None): "pos"}),
            [(-5, "neg"), (50, "mid"), (200, "pos")],
        ),
        (
            RangeKeyDict({(10, 10): "ten", (0, 20): "wide"}, overlap_strategy="first"),
            [(10, "ten"), (5, "wide")],
        ),
        (
            RangeKeyDict(
                {(0, 200): "long", (50, 150): "med", (80, 90): "short"},
                overlap_strategy="shortest",
            ),
            [(85, "short"), (25, "long")],
        ),
    ]


@pytest.mark.parametrize("rkd,queries", _lookup_cases())
def test_bisect_lookup_correctness(rkd: RangeKeyDict, queries: List[Tuple[float, Any]]) -> None:
    """Bisect-backed lookup matches expected values across scenarios."""
    for query, expected in queries:
        if expected is KeyError:
            with pytest.raises(KeyError):
                _ = rkd[query]
        else:
            assert rkd[query] == expected
            assert query in rkd


def test_moderate_number_of_ranges():
    """Test that the dict can handle a moderate number of ranges."""
    # Create dict with 1,000 non-overlapping ranges
    ranges: Dict[RangeKey, Any] = {(i * 100, (i + 1) * 100): f"range_{i}" for i in range(1000)}
    rkd = RangeKeyDict(ranges)

    assert len(rkd) == 1000

    # Test lookups across the range
    assert rkd[50] == "range_0"
    assert rkd[50050] == "range_500"
    assert rkd[99950] == "range_999"


def test_many_overlapping_ranges():
    """Test with overlapping ranges."""
    # Create ranges that all overlap at point 500
    ranges: Dict[RangeKey, Any] = {(i, 1000): f"range_{i}" for i in range(0, 100, 10)}
    rkd = RangeKeyDict(ranges, overlap_strategy="first")

    assert len(rkd) == 10
    # This point is in all ranges
    assert rkd[500] == "range_0"


def test_repeated_lookups():
    """Test that repeated lookups work correctly."""
    rkd = RangeKeyDict({(i * 10, (i + 1) * 10): f"range_{i}" for i in range(100)})

    # Do many lookups - just verify correctness
    for _ in range(100):
        assert rkd[505] == "range_50"


@pytest.mark.parametrize("size", [10, 100, 500])
def test_scalability(size):
    """Test that the dict scales to different sizes."""
    ranges: Dict[RangeKey, Any] = {(i * 10, (i + 1) * 10): f"range_{i}" for i in range(size)}
    rkd = RangeKeyDict(ranges)

    assert len(rkd) == size

    # Test a few lookups
    assert rkd[5] == "range_0"
    if size >= 10:
        assert rkd[size * 5] == f"range_{size // 2}"


def test_large_non_overlapping_boundaries():
    """Sanity check bisect path on many adjacent ranges."""
    ranges: Dict[RangeKey, Any] = {(i * 100, (i + 1) * 100): f"range_{i}" for i in range(10_000)}
    rkd = RangeKeyDict(ranges)
    assert rkd[0] == "range_0"
    assert rkd[99] == "range_0"
    assert rkd[100] == "range_1"
    assert rkd[999_950] == "range_9999"
    assert 1_000_000 not in rkd


def test_basic_operations_correctness():
    """Test correctness of basic operations with reasonable size."""
    rkd = RangeKeyDict()

    # Add ranges
    for i in range(100):
        rkd[(i * 10, (i + 1) * 10)] = f"range_{i}"

    # Lookups
    for i in range(10):
        assert rkd[i * 100 + 5] == f"range_{i * 10}"

    # Contains checks
    for i in range(10):
        assert i * 100 + 5 in rkd

    # Get with defaults
    for i in range(10):
        assert rkd.get(i * 100 + 5, "default") == f"range_{i * 10}"

    # Iteration
    keys = list(rkd.keys())
    assert len(keys) == 100
