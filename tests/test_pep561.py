"""PEP 561: package must ship py.typed for type checker discovery."""

from pathlib import Path

import range_key_dict


def test_py_typed_marker_present() -> None:
    """Installed package includes py.typed (see PEP 561)."""
    py_typed = Path(range_key_dict.__file__).parent / "py.typed"
    assert py_typed.is_file(), "range_key_dict must include py.typed for inline types"
