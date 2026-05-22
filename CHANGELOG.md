# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-05-22

### Added

- **Bisect-accelerated lookup**: Find candidate ranges in O(log M + K) via binary search on sorted starts, then backward scan for matches

### Fixed

- **`__eq__`**: Compare stored values with `==` instead of `repr()` (e.g. `1` and `1.0` now compare equal)
- **`overlap_strategy`**: Invalid strategies raise `ValueError` at construction instead of silently using undefined behavior
- **Range bounds**: Non-numeric and non-finite bounds raise clear errors at construction; bool bounds rejected
- **Lookup keys**: `bool` is not accepted as a lookup key (avoids `True` matching integer `1`)
- **Lookup validation**: Non-finite lookup values (`nan`, `inf`) raise `ValueError`, consistent with range bounds
- **Large integers**: Integer lookups are no longer widened to `float`, preserving exact matches above 2^53
- **`shortest`/`longest` ties**: Equal-length matches resolve by insertion order (earliest / latest)

### Changed

- Performance and API documentation now describe O(log M + K) lookup cost accurately
- Test suite expanded to 215 tests (~98% coverage), including `test_robustness.py`
- CI: matrix tests without duplicate coverage runs; Codecov upload is optional and non-blocking
- PyPI metadata: production/stable classifier, maintainer email corrected

## [2.0.1] - 2026-05-22

### Fixed

- **Point ranges**: Keys where `start == end` (e.g. `(1, 1)`) now match that single value on lookup ([#1](https://github.com/eddiethedean/range-key-dict-2/issues/1))

### Changed

- **Typing**: Annotations use Python 3.8–compatible `typing` forms (`Union`, `Optional`, `Dict`, `List`); exported `RangeBound` alias

## [2.0.0] - 2025-10-21

> **Note:** Metrics in this section (93 tests, O(M) lookup, flake8, Python 3.8–3.12) describe the initial 2.0.0 release. See [2.1.0](#210---2026-05-22) for current behavior.

### 🎉 Initial Release

Complete modernization and enhancement of the original [range-key-dict](https://github.com/albertmenglongli/range-key-dict) by Albert Li.

### Added

#### Core Features
- **Full Dictionary Interface**: Complete dict-like API with `keys()`, `values()`, `items()`, `__len__`, `__contains__`, `__iter__`, `__setitem__`, `__delitem__`, `__repr__`, `__str__`, and `__eq__`
- **Type Hints**: Comprehensive type annotations throughout the codebase with mypy strict mode compliance
- **Modern Python**: Updated to Python 3.8+ with modern syntax and features

#### Advanced Capabilities
- **Open-ended Ranges**: Support for infinite bounds using `None` (e.g., `(None, 100)` for negative infinity to 100)
- **Overlap Strategies**: Five strategies for handling overlapping ranges:
  - `'error'`: Raise `ValueError` on overlaps (default, backwards compatible)
  - `'first'`: Return first inserted matching range
  - `'last'`: Return last inserted matching range
  - `'shortest'`: Return shortest matching range
  - `'longest'`: Return longest matching range
- **Mutable Operations**: Add, update, and delete ranges after creation using `__setitem__` and `__delitem__`
- **Insertion Order Tracking**: Maintain insertion order for 'first' and 'last' overlap strategies

#### Testing & Quality
- **Comprehensive Test Suite**: 93 tests covering:
  - Backwards compatibility with v1
  - Dict interface operations
  - Overlapping range strategies
  - Open-ended ranges
  - Edge cases
  - Performance validation
- **98% Test Coverage**: Near-complete code coverage
- **Type Safety**: Passes mypy strict mode
- **Linting**: Configured with black, isort, and flake8

#### Developer Experience
- **Modern Packaging**: Using `pyproject.toml` (PEP 517/518)
- **Pre-commit Hooks**: Automated code formatting and linting
- **CI/CD**: GitHub Actions workflow for multi-version Python testing (3.8-3.12)
- **Documentation**: Comprehensive README with examples, migration guide, and API reference
- **Changelog**: Standardized changelog following Keep a Changelog format

### Changed
- **Python Version**: Dropped Python 2.7 support, now requires Python 3.8+
- **Packaging**: Migrated from `setup.py` to modern `pyproject.toml`
- **License**: Clarified MIT license with attribution to original author

### Maintained
- **100% Backwards Compatible**: All v1 APIs work identically in v2
- **Original Behavior**: Default behavior matches v1 exactly (overlap strategy='error')
- **Same Import Path**: `from range_key_dict import RangeKeyDict`

### Performance Notes
- Current implementation maintains O(M) linear search (same as v1)
- Added TODO for future O(log M) binary search optimization
- Performance is excellent for typical use cases (< 1000 ranges)

### Technical Details
- **Dependencies**: Zero runtime dependencies
- **Data Structure**: Sorted list of `RangeEntry` dataclasses with binary search preparation
- **Test Framework**: pytest with coverage reporting
- **Documentation**: Comprehensive docstrings following Google style

### Credits
- Original concept and v1 implementation by **Albert Li (menglong.li)**
- V2 modernization and enhancements by **Matthew Odos**

## [1.1.0] - (Original Project)

See [original repository](https://github.com/albertmenglongli/range-key-dict) for v1.x changelog.

---

[2.1.0]: https://github.com/eddiethedean/range-key-dict-2/releases/tag/v2.1.0
[2.0.1]: https://github.com/eddiethedean/range-key-dict-2/releases/tag/v2.0.1
[2.0.0]: https://github.com/eddiethedean/range-key-dict-2/releases/tag/v2.0.0

