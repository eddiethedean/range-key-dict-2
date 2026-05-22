# range-key-dict-2 Project Summary

## Overview

Modernized and enhanced fork of [range-key-dict](https://github.com/albertmenglongli/range-key-dict) by Albert Li. **range-key-dict-2** is a typed, dict-like mapping from numeric ranges to values, with open-ended bounds, overlap strategies, and fast lookups.

**Current version:** 2.1.0  
**Status:** Production-ready; published on PyPI as `range-key-dict-2`

## Core Capabilities

- `RangeKeyDict` with full dict-like API (`__getitem__`, `get`, `__setitem__`, `__delitem__`, `keys` / `values` / `items`, iteration, `__eq__`, etc.)
- Half-open range semantics `[start, end)`; **point ranges** `(n, n)` for exact values
- Open-ended ranges via `None` bounds
- Five **overlap strategies**: `error`, `first`, `last`, `shortest`, `longest`
- **O(log M + K)** lookups (binary search on sorted starts, then backward scan)
- **PEP 561** inline types (`py.typed`)
- Zero runtime dependencies; Python 3.8–3.13

## Test Suite

| Module | Focus |
|--------|--------|
| `test_backwards_compatibility.py` | v1 API parity |
| `test_dict_interface.py` | Dict-like operations and equality |
| `test_edge_cases.py` | Boundaries, types, edge values |
| `test_open_ended_ranges.py` | `None` bounds |
| `test_overlapping_ranges.py` | Overlap strategies |
| `test_point_ranges.py` | Point key `(n, n)` semantics |
| `test_performance.py` | Scale and bisect correctness |
| `test_pep561.py` | `py.typed` marker |
| `test_robustness.py` | Validation, brute-force parity, regressions |

**Metrics (current):** 200 tests, **98%** coverage on `range_key_dict`

## Tooling

- **Packaging:** `pyproject.toml` (setuptools)
- **CI:** GitHub Actions — pytest + coverage on 3.8–3.13; ruff, black, isort, mypy on 3.12
- **Local checks:** `ruff format`, `ruff check`, `mypy`, `ty check`, `pytest`
- **Pre-commit:** black, isort, ruff, mypy

## Documentation

| File | Purpose |
|------|---------|
| [README.md](README.md) | Main user guide, API examples, performance, development |
| [CHANGELOG.md](CHANGELOG.md) | Version history (2.1.0, 2.0.1, 2.0.0) |
| [examples/README.md](examples/README.md) | Jupyter notebook guide |
| [examples_code/README.md](examples_code/README.md) | Runnable script guide |

## Project Layout

```
range-key-dict-2/
├── .github/workflows/ci.yml
├── range_key_dict/
│   ├── __init__.py          # exports, __version__
│   ├── range_key_dict.py    # RangeKeyDict, RangeEntry
│   └── py.typed
├── tests/                   # 9 test modules (200 tests)
├── examples/                # Jupyter notebooks
├── examples_code/           # Runnable .py scripts + run_all.sh
├── CHANGELOG.md
├── README.md
├── pyproject.toml
└── LICENSE
```

## Release Highlights

### 2.1.0

- Bisect-accelerated lookup; accurate O(log M + K) documentation
- Fixes: `__eq__` value comparison, `overlap_strategy` validation, bound/lookup validation
- Expanded tests (`test_robustness.py`, bisect parity, 200 tests total)

### 2.0.1

- Point range lookup fix; PEP 561 `py.typed`; Python 3.8 typing compatibility

### 2.0.0

- Initial modernization: dict API, overlap strategies, open-ended ranges, CI/docs

## Credits

- **Original author:** Albert Li (menglong.li) — [range-key-dict](https://github.com/albertmenglongli/range-key-dict)
- **Maintainer (v2):** Matthew Odos
- **License:** MIT
