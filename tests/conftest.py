"""Shared pytest fixtures for range-key-dict tests."""

import pytest

from range_key_dict import RangeKeyDict


@pytest.fixture
def simple_dict():
    """A simple RangeKeyDict for testing."""
    return RangeKeyDict(
        {
            (0, 100): "A",
            (100, 200): "B",
            (200, 300): "C",
        }
    )


@pytest.fixture
def empty_dict():
    """An empty RangeKeyDict."""
    return RangeKeyDict()


@pytest.fixture
def open_ended_dict():
    """A RangeKeyDict with open-ended ranges."""
    return RangeKeyDict(
        {
            (None, 0): "negative",
            (0, 100): "small",
            (100, None): "large",
        }
    )


@pytest.fixture
def overlapping_dict_first():
    """A RangeKeyDict with overlapping ranges using 'first' strategy."""
    return RangeKeyDict(
        {
            (0, 100): "first",
            (50, 150): "second",
            (25, 75): "third",
        },
        overlap_strategy="first",
    )


@pytest.fixture
def overlapping_dict_last():
    """A RangeKeyDict with overlapping ranges using 'last' strategy."""
    return RangeKeyDict(
        {
            (0, 100): "first",
            (50, 150): "second",
            (25, 75): "third",
        },
        overlap_strategy="last",
    )


@pytest.fixture
def overlapping_dict_shortest():
    """A RangeKeyDict with overlapping ranges using 'shortest' strategy."""
    return RangeKeyDict(
        {
            (0, 200): "long",
            (50, 150): "medium",
            (80, 90): "short",
        },
        overlap_strategy="shortest",
    )


@pytest.fixture
def overlapping_dict_longest():
    """A RangeKeyDict with overlapping ranges using 'longest' strategy."""
    return RangeKeyDict(
        {
            (0, 200): "long",
            (50, 150): "medium",
            (80, 90): "short",
        },
        overlap_strategy="longest",
    )
