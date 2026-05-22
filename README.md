# range-key-dict-2

[![PyPI version](https://img.shields.io/pypi/v/range-key-dict-2.svg)](https://pypi.org/project/range-key-dict-2/)
[![Python versions](https://img.shields.io/pypi/pyversions/range-key-dict-2.svg)](https://pypi.org/project/range-key-dict-2/)
[![CI Status](https://github.com/eddiethedean/range-key-dict-2/actions/workflows/ci.yml/badge.svg)](https://github.com/eddiethedean/range-key-dict-2/actions)
[![coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/eddiethedean/range-key-dict-2/refs/heads/main/gh-badges/coverage.json)](https://codecov.io/gh/eddiethedean/range-key-dict-2)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, feature-rich Python dictionary that uses numeric ranges as keys. Perfect for mapping continuous ranges of numbers to values, with O(log M + K) lookup performance and full dict-like interface.

## 🎯 Credit & Inspiration

This project is directly inspired by and builds upon the excellent work of **Albert Li (menglong.li)** in the original [range-key-dict](https://github.com/albertmenglongli/range-key-dict) project. `range-key-dict-2` modernizes the concept with:

- Python 3.8+ features (type hints, modern syntax)
- Full dictionary-like interface
- Overlapping range strategies
- Open-ended ranges (infinite bounds)
- O(log M + K) lookups via binary search on sorted range starts
- Point ranges `(n, n)` for single-value keys
- 214 tests with 98% code coverage
- Modern tooling (ruff, mypy, ty) and CI/CD on Python 3.8–3.13

## ✨ Features

### Core Capabilities

- **Range-based Keys**: Use numeric ranges `(start, end)` as dictionary keys
- **Efficient Lookups**: Query which range contains a given number
- **Full Dict Interface**: Supports `keys()`, `values()`, `items()`, `len()`, `in`, iteration, and more
- **Mutable Operations**: Add, update, and delete ranges dynamically with `__setitem__` and `__delitem__`
- **Type Safety**: Fully typed with mypy strict mode support

### Advanced Features

- **Open-ended Ranges**: Use `None` for infinite bounds (e.g., `(None, 0)` for all negative numbers)
- **Overlap Strategies**: Control behavior when ranges overlap:
  - `'error'`: Raise exception (default, backwards compatible)
  - `'first'`: Return first matching range (by insertion order)
  - `'last'`: Return last matching range (by insertion order)
  - `'shortest'`: Return shortest matching range (ties: earliest insertion)
  - `'longest'`: Return longest matching range (ties: latest insertion)
- **Point Ranges**: Use `(n, n)` when a key should match exactly one number (not a half-open interval)
- **Flexible Types**: Works with integers, floats, and mixed types (bounds must be `int`, `float`, or `None`; `bool` is rejected)
- **Input Validation**: Invalid `overlap_strategy`, non-numeric bounds, and non-finite floats raise clear errors at construction and lookup
- **PEP 561**: Ships `py.typed` for type checker discovery
- **Backwards Compatible**: 100% compatible with original `range-key-dict` v1 API

### Range Semantics

- **Half-open intervals** (default): `[start, end)` — includes `start`, excludes `end`. Adjacent ranges such as `(0, 10)` and `(10, 20)` meet at `10` without overlapping.
- **Point ranges**: When `start == end`, only that exact value matches (e.g. `(42, 42)` matches `42` only).
- **Open-ended**: `None` as a bound means negative or positive infinity.
- **Insertion order**: `first`/`last` use monotonic insertion order; deleting and re-adding a range assigns a new order.

### Limitations

- Lookup keys must be finite `int` or `float` (`nan` and `inf` are rejected, consistent with range bounds).
- Integer lookups preserve exact precision (including values above 2^53); mixed int/float comparisons use float semantics when needed.
- `get()` cannot distinguish a missing key from a stored `None` without a sentinel default.

## 📦 Installation

```bash
pip install range-key-dict-2
```

## 🚀 Quick Start

### Basic Usage

```python
from range_key_dict import RangeKeyDict

# Create a range dictionary
grades = RangeKeyDict({
    (0, 60): 'F',
    (60, 70): 'D',
    (70, 80): 'C',
    (80, 90): 'B',
    (90, 100): 'A',
})

# Look up values
print(grades[85])  # 'B'
print(grades[92])  # 'A'
print(grades[58])  # 'F'

# Safe lookup with default
print(grades.get(105, 'Out of range'))  # 'Out of range'

# Check membership
print(75 in grades)  # True
print(105 in grades)  # False
```

### Dict-like Interface

```python
from range_key_dict import RangeKeyDict

rkd = RangeKeyDict()

# Add ranges
rkd[(0, 10)] = 'first'
rkd[(10, 20)] = 'second'
rkd[(20, 30)] = 'third'

# Update a range
rkd[(10, 20)] = 'updated second'

# Delete a range
del rkd[(20, 30)]

# Iterate
for range_key in rkd:
    print(f"Range {range_key} -> {rkd[range_key]}")

# Get all keys, values, items
print(rkd.keys())    # [(0, 10), (10, 20)]
print(rkd.values())  # ['first', 'updated second']
print(rkd.items())   # [((0, 10), 'first'), ((10, 20), 'updated second')]

# Length
print(len(rkd))  # 2
```

### Open-ended Ranges

Use `None` for infinite boundaries:

```python
from range_key_dict import RangeKeyDict

temperature = RangeKeyDict({
    (None, 0): 'freezing',      # (-∞, 0)
    (0, 20): 'cold',            # [0, 20)
    (20, 30): 'comfortable',    # [20, 30)
    (30, None): 'hot',          # [30, +∞)
})

print(temperature[-100])  # 'freezing'
print(temperature[25])    # 'comfortable'
print(temperature[50])    # 'hot'
```

### Overlapping Ranges

Control how overlapping ranges are handled:

```python
from range_key_dict import RangeKeyDict

# Allow overlaps, return first matching range
rkd = RangeKeyDict({
    (0, 100): 'wide',
    (25, 75): 'narrow',
}, overlap_strategy='first')

print(rkd[50])  # 'wide' (first defined range wins)

# Return shortest matching range
rkd = RangeKeyDict({
    (0, 100): 'wide',
    (25, 75): 'narrow',
}, overlap_strategy='shortest')

print(rkd[50])  # 'narrow' (shortest matching range)
```

Available strategies: `'error'`, `'first'`, `'last'`, `'shortest'`, `'longest'`

## 📖 Examples

Comprehensive examples available in **two formats**:

### 📓 Jupyter Notebooks (Recommended)
**[examples/](examples/)** - Interactive notebooks with pre-executed outputs

- `01_basic_usage.ipynb` - Get started with the basics (8 examples)
- `02_dict_interface.ipynb` - Master the dict-like API (10 examples)
- `03_open_ended_ranges.ipynb` - Work with infinity bounds (10 examples)
- `04_overlap_strategies.ipynb` - Handle overlapping ranges (10 examples)
- `05_real_world_use_cases.ipynb` - Production-ready examples (10 examples)

```bash
cd examples
jupyter notebook
```

### 🐍 Python Scripts
**[examples_code/](examples_code/)** - Runnable Python scripts

```bash
cd examples_code
python 01_basic_usage.py
# or
bash run_all.sh
```

## 📖 Real-World Examples

### Age Categories

```python
age_groups = RangeKeyDict({
    (None, 13): 'child',
    (13, 20): 'teenager',
    (20, 65): 'adult',
    (65, None): 'senior',
})

print(age_groups[8])   # 'child'
print(age_groups[16])  # 'teenager'
print(age_groups[45])  # 'adult'
print(age_groups[70])  # 'senior'
```

### Tax Brackets

```python
tax_brackets_2024 = RangeKeyDict({
    (0, 11000): 0.10,
    (11000, 44725): 0.12,
    (44725, 95375): 0.22,
    (95375, 182100): 0.24,
    (182100, 231250): 0.32,
    (231250, 578125): 0.35,
    (578125, None): 0.37,
})

income = 50000
tax_rate = tax_brackets_2024[income]
print(f"Tax rate for ${income}: {tax_rate:.0%}")  # Tax rate for $50000: 22%
```

### HTTP Status Code Categories

```python
http_categories = RangeKeyDict({
    (100, 200): 'Informational',
    (200, 300): 'Success',
    (300, 400): 'Redirection',
    (400, 500): 'Client Error',
    (500, 600): 'Server Error',
})

print(http_categories[200])  # 'Success'
print(http_categories[404])  # 'Client Error'
print(http_categories[500])  # 'Server Error'
```

## 🔄 Migration from v1

`range-key-dict-2` is 100% backwards compatible with `range-key-dict` v1:

```python
# This works exactly the same in v1 and v2
from range_key_dict import RangeKeyDict

rkd = RangeKeyDict({
    (0, 100): 'A',
    (100, 200): 'B',
    (200, 300): 'C',
})

assert rkd[70] == 'A'
assert rkd[170] == 'B'
assert rkd.get(1000, 'D') == 'D'
```

Simply change your dependency from `range-key-dict` to `range-key-dict-2` and enjoy the new features!

## ⚡ Performance

Lookups use binary search on sorted range starts, then scan backward over candidates whose start is at most the query value. Complexity is **O(log M + K)** where M is the number of ranges and K is how many ranges can still contain the query (typically K = 1 for non-overlapping adjacent ranges; K can approach M when many ranges overlap or share open lower bounds).

Performance is excellent for typical layouts with hundreds or thousands of ranges. For heavy overlap at a single point, consider fewer overlapping ranges or interval-tree libraries (see Related Projects).

## 🧪 Testing

The package includes comprehensive tests:

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=range_key_dict --cov-report=html

# Run specific test file
pytest tests/test_backwards_compatibility.py
```

The suite currently has **214 tests** and **98%** coverage on `range_key_dict`. Test modules include backwards compatibility, dict interface, edge cases, open-ended ranges, overlapping strategies, point ranges, performance/bisect correctness, PEP 561, and robustness/regression tests.

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/eddiethedean/range-key-dict-2.git
cd range-key-dict-2

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Run Quality Checks

```bash
# Format and lint (recommended)
ruff format range_key_dict tests
ruff check range_key_dict tests

# Type check
mypy range_key_dict

# Run tests with coverage
pytest --cov=range_key_dict --cov-report=term-missing

# Run all pre-commit hooks (black, isort, ruff, mypy)
pre-commit run --all-files
```

### Codecov (optional)

CI uploads coverage to [Codecov](https://codecov.io/gh/eddiethedean/range-key-dict-2) only when the repository is linked on Codecov and a `CODECOV_TOKEN` secret is configured; upload failures do not fail CI. The README coverage badge is updated automatically from `coverage.xml` on each push to `main`.

## 📋 Requirements

- Python 3.8 through 3.13 (see CI matrix)
- No runtime dependencies!

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md) for release notes. Current version: **2.1.0**.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Albert Li (menglong.li)** - Original [range-key-dict](https://github.com/albertmenglongli/range-key-dict) creator
- All contributors who help improve this project

## 📚 Related Projects

- [range-key-dict](https://github.com/albertmenglongli/range-key-dict) - The original implementation
- [intervaltree](https://github.com/chaimleib/intervaltree) - For more complex interval operations
- [portion](https://github.com/AlexandreDecan/portion) - Advanced interval arithmetic

## 📮 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/eddiethedean/range-key-dict-2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/eddiethedean/range-key-dict-2/discussions)

---

Made with ❤️ by Matthew Odos, inspired by Albert Li's original work.
