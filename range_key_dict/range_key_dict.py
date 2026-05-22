"""
A modern dictionary implementation that uses ranges as keys.

This module provides RangeKeyDict, which allows you to map numeric ranges to values
and perform O(log M + K) lookups (K = ranges with start <= query) to find matches.

Original concept by Albert Li (menglong.li): https://github.com/albertmenglongli/range-key-dict
Modernized and enhanced for Python 3.8+ with improved performance and additional features.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Literal, Optional, Tuple, Union, cast

# Type aliases (int bounds are valid; floats and None for open-ended ranges)
RangeBound = Union[int, float]
RangeKey = Tuple[Optional[RangeBound], Optional[RangeBound]]
OverlapStrategy = Literal["error", "first", "last", "shortest", "longest"]
LookupNumber = Union[int, float]

_VALID_OVERLAP_STRATEGIES: Tuple[str, ...] = (
    "error",
    "first",
    "last",
    "shortest",
    "longest",
)


def _validate_overlap_strategy(strategy: str) -> OverlapStrategy:
    if strategy not in _VALID_OVERLAP_STRATEGIES:
        raise ValueError(
            f"Invalid overlap_strategy {strategy!r}; "
            f"must be one of: {', '.join(_VALID_OVERLAP_STRATEGIES)}"
        )
    return cast(OverlapStrategy, strategy)


def _validate_bound(bound: object, name: str) -> Optional[RangeBound]:
    if bound is None:
        return None
    if isinstance(bound, bool):
        raise TypeError(f"Range {name} must be int, float, or None, not bool")
    if isinstance(bound, int):
        return bound
    if isinstance(bound, float):
        if not math.isfinite(bound):
            raise ValueError(f"Range {name} must be finite, got {bound!r}")
        return bound
    raise TypeError(f"Range {name} must be int, float, or None, got {type(bound).__name__}")


def _validate_lookup_number(number: object) -> LookupNumber:
    if isinstance(number, bool):
        raise TypeError("Lookup key must be int or float, not bool")
    if isinstance(number, int):
        return number
    if isinstance(number, float):
        if not math.isfinite(number):
            raise ValueError(f"Lookup key must be finite, got {number!r}")
        return number
    raise TypeError(f"Lookup key must be int or float, got {type(number).__name__}")


def _numeric_le(a: Union[int, float], b: Union[int, float]) -> bool:
    if isinstance(a, int) and isinstance(b, int):
        return a <= b
    return float(a) <= float(b)


def _numeric_lt(a: Union[int, float], b: Union[int, float]) -> bool:
    if isinstance(a, int) and isinstance(b, int):
        return a < b
    return float(a) < float(b)


def _numeric_eq(a: Union[int, float], b: Union[int, float]) -> bool:
    if isinstance(a, int) and isinstance(b, int):
        return a == b
    return float(a) == float(b)


def _parse_range_key(key: object) -> Tuple[Optional[RangeBound], Optional[RangeBound]]:
    if not isinstance(key, tuple) or len(key) != 2:
        raise TypeError(f"Range key must be a 2-tuple, got {type(key)}")
    start, end = key
    start = _validate_bound(start, "start")
    end = _validate_bound(end, "end")
    if start is not None and end is not None and start > end:
        raise ValueError(f"Range start ({start}) must be <= end ({end})")
    return start, end


def _sort_key(entry: RangeEntry) -> Tuple[Union[float, int], Union[float, int]]:
    start = float("-inf") if entry.start is None else entry.start
    end = float("inf") if entry.end is None else entry.end
    return (start, end)


def _start_le_query(entry: RangeEntry, query: LookupNumber) -> bool:
    if entry.start is None:
        return True
    return _numeric_le(entry.start, query)


def _start_gt_query(entry: RangeEntry, query: LookupNumber) -> bool:
    if entry.start is None:
        return False
    return _numeric_lt(query, entry.start)


@dataclass(frozen=True)
class RangeEntry:
    """Internal representation of a range-value pair."""

    start: Optional[RangeBound]
    end: Optional[RangeBound]
    value: Any
    insertion_order: int = 0  # Track insertion order for 'first'/'last' strategies

    def is_point(self) -> bool:
        """True when start and end are equal (a single precise value)."""
        return self.start is not None and self.end is not None and self.start == self.end

    def contains(self, number: LookupNumber) -> bool:
        """Check if this range contains the given number."""
        if self.is_point():
            assert self.start is not None
            return _numeric_eq(number, self.start)
        start_ok = self.start is None or _numeric_le(self.start, number)
        end_ok = self.end is None or _numeric_lt(number, self.end)
        return start_ok and end_ok

    def overlaps(self, other: "RangeEntry") -> bool:
        """Check if this range overlaps with another range."""
        if self.is_point():
            if self.start is None:
                return False
            return other.contains(self.start)
        if other.is_point():
            if other.start is None:
                return False
            return self.contains(other.start)

        # Handle None bounds (infinity)
        self_start = float("-inf") if self.start is None else self.start
        self_end = float("inf") if self.end is None else self.end
        other_start = float("-inf") if other.start is None else other.start
        other_end = float("inf") if other.end is None else other.end

        # Two ranges overlap if one starts before the other ends
        return self_start < other_end and other_start < self_end

    def length(self) -> float:
        """Calculate the length of the range. Returns inf for unbounded ranges."""
        if self.start is None or self.end is None:
            return float("inf")
        return float(self.end) - float(self.start)

    @property
    def key(self) -> RangeKey:
        """Return the range as a tuple (start, end)."""
        return (self.start, self.end)


class RangeKeyDict:
    """
    A dictionary that uses numeric ranges as keys.

    This class allows you to map ranges of numbers to values and efficiently
    look up which range contains a given number. Lookups are performed in
    O(log M + K) time where M is the number of ranges and K is how many
    ranges have a start less than or equal to the query (K is 1 for typical
    non-overlapping layouts; K can approach M when many ranges overlap).

    Args:
        initial_dict: Optional dictionary with (start, end) tuples as keys
        overlap_strategy: How to handle overlapping ranges:
            - 'error': Raise ValueError on overlaps (default for backwards compatibility)
            - 'first': Return the first matching range (by insertion order)
            - 'last': Return the last matching range (by insertion order)
            - 'shortest': Return the shortest matching range; ties use earliest insertion
            - 'longest': Return the longest matching range; ties use latest insertion

    Examples:
        >>> rkd = RangeKeyDict({(0, 100): 'A', (100, 200): 'B'})
        >>> rkd[50]
        'A'
        >>> rkd[150]
        'B'
        >>> rkd.get(250, 'default')
        'default'

        # Open-ended ranges
        >>> rkd = RangeKeyDict({(None, 0): 'negative', (0, None): 'non-negative'})
        >>> rkd[-100]
        'negative'
        >>> rkd[1000]
        'non-negative'
    """

    def __init__(
        self,
        initial_dict: Optional[Dict[RangeKey, Any]] = None,
        overlap_strategy: OverlapStrategy = "error",
    ) -> None:
        """Initialize a RangeKeyDict."""
        self._entries: List[RangeEntry] = []
        self._overlap_strategy: OverlapStrategy = _validate_overlap_strategy(overlap_strategy)
        self._next_insertion_order = 0

        if initial_dict is not None:
            for key, value in initial_dict.items():
                start, end = _parse_range_key(key)

                entry = RangeEntry(start, end, value, self._next_insertion_order)
                self._next_insertion_order += 1
                self._add_entry(entry)

            self._sort_entries()

    def _sort_entries(self) -> None:
        """Sort entries by start (None/-inf first), then by end."""
        self._entries.sort(key=_sort_key)

    def _add_entry(self, entry: RangeEntry) -> None:
        """Add an entry, checking for overlaps based on strategy."""
        if self._overlap_strategy == "error":
            # Check for overlaps with existing entries
            for existing in self._entries:
                if entry.overlaps(existing):
                    raise ValueError(
                        f"Range {entry.key} overlaps with existing range {existing.key}"
                    )

        self._entries.append(entry)

    def _find_matching_entries(self, number: object) -> List[RangeEntry]:
        """Find all entries that contain the given number (O(log M + K))."""
        query = _validate_lookup_number(number)
        if not self._entries:
            return []

        # Binary search for first index with start > query (Python 3.8 compatible).
        lo = 0
        hi = len(self._entries)
        while lo < hi:
            mid = (lo + hi) // 2
            if _start_le_query(self._entries[mid], query):
                lo = mid + 1
            else:
                hi = mid
        idx = lo

        matches: List[RangeEntry] = []
        i = idx - 1
        while i >= 0:
            entry = self._entries[i]
            if _start_gt_query(entry, query):
                break
            if entry.contains(query):
                matches.append(entry)
            i -= 1

        return matches

    def _select_entry(self, matches: List[RangeEntry]) -> RangeEntry:
        """Select the appropriate entry based on overlap strategy."""
        if len(matches) == 1:
            return matches[0]

        # Multiple matches - apply overlap strategy
        if self._overlap_strategy == "first":
            return min(matches, key=lambda e: e.insertion_order)
        if self._overlap_strategy == "last":
            return max(matches, key=lambda e: e.insertion_order)
        if self._overlap_strategy == "shortest":
            return min(matches, key=lambda e: (e.length(), e.insertion_order))
        if self._overlap_strategy == "longest":
            return max(matches, key=lambda e: (e.length(), e.insertion_order))
        raise ValueError(
            f"Multiple ranges match but overlap_strategy is {self._overlap_strategy!r}"
        )

    def __getitem__(self, number: LookupNumber) -> Any:
        """
        Look up which range contains the number and return its value.

        Args:
            number: The number to look up

        Returns:
            The value associated with the range containing the number

        Raises:
            KeyError: If no range contains the number
        """
        matches = self._find_matching_entries(number)
        if not matches:
            raise KeyError(number)
        return self._select_entry(matches).value

    def get(self, number: LookupNumber, default: Any = None) -> Any:
        """
        Get the value for a number, returning default if not found.

        Args:
            number: The number to look up
            default: Value to return if number is not in any range

        Returns:
            The value associated with the range, or default
        """
        try:
            return self[number]
        except KeyError:
            return default

    def __contains__(self, number: LookupNumber) -> bool:
        """Check if the number falls within any range."""
        return len(self._find_matching_entries(number)) > 0

    def __len__(self) -> int:
        """Return the number of ranges in the dict."""
        return len(self._entries)

    def __iter__(self) -> Iterator[RangeKey]:
        """Iterate over the range keys."""
        for entry in self._entries:
            yield entry.key

    def keys(self) -> List[RangeKey]:
        """Return a list of all range keys."""
        return [entry.key for entry in self._entries]

    def values(self) -> List[Any]:
        """Return a list of all values."""
        return [entry.value for entry in self._entries]

    def items(self) -> List[Tuple[RangeKey, Any]]:
        """Return a list of (range, value) pairs."""
        return [(entry.key, entry.value) for entry in self._entries]

    def __setitem__(self, key: RangeKey, value: Any) -> None:
        """
        Add or update a range-value pair.

        Args:
            key: A tuple (start, end) representing the range
            value: The value to associate with the range

        Raises:
            TypeError: If key is not a 2-tuple
            ValueError: If the range is invalid or overlaps with existing ranges
        """
        start, end = _parse_range_key(key)

        # Remove existing entry with this exact key if it exists
        self._entries = [e for e in self._entries if e.key != key]

        # Add new entry
        entry = RangeEntry(start, end, value, self._next_insertion_order)
        self._next_insertion_order += 1
        self._add_entry(entry)

        self._sort_entries()

    def __delitem__(self, key: RangeKey) -> None:
        """
        Remove a range from the dict.

        Args:
            key: A tuple (start, end) representing the range to remove

        Raises:
            KeyError: If the range is not in the dict
        """
        original_len = len(self._entries)
        self._entries = [e for e in self._entries if e.key != key]

        if len(self._entries) == original_len:
            raise KeyError(key)

    def __repr__(self) -> str:
        """Return a string representation of the RangeKeyDict."""
        items = ", ".join(f"{entry.key}: {entry.value!r}" for entry in self._entries)
        return f"RangeKeyDict({{{items}}})"

    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return repr(self)

    def __eq__(self, other: object) -> bool:
        """Check equality with another RangeKeyDict."""
        if not isinstance(other, RangeKeyDict):
            return NotImplemented

        # Compare based on content, not insertion order
        if len(self._entries) != len(other._entries):
            return False

        if self._overlap_strategy != other._overlap_strategy:
            return False

        self_pairs = sorted((e.key, e.value) for e in self._entries)
        other_pairs = sorted((e.key, e.value) for e in other._entries)
        return self_pairs == other_pairs


# Backwards compatibility: allow imports from module level
__all__ = [
    "RangeKeyDict",
    "RangeEntry",
    "RangeKey",
    "RangeBound",
    "OverlapStrategy",
    "LookupNumber",
]
