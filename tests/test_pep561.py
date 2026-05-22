"""PEP 561: package must ship py.typed for type checker discovery."""

from pathlib import Path

import range_key_dict


def test_py_typed_marker_present() -> None:
    """Installed package includes py.typed (see PEP 561)."""
    py_typed = Path(range_key_dict.__file__).parent / "py.typed"
    assert py_typed.is_file(), "range_key_dict must include py.typed for inline types"


def test_version_matches_release() -> None:
    """Package version matches pyproject.toml release."""
    assert range_key_dict.__version__ == "2.1.0"
