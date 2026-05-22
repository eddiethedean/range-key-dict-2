# Python Example Scripts

This directory contains Python scripts demonstrating all features of `range-key-dict-2` (version **2.1.0**).

Ranges use half-open semantics `[start, end)` unless `start == end`, in which case only that exact value matches. Use `None` for unbounded ends. See [../README.md](../README.md) for overlap strategies and validation rules.

## 📄 Scripts

- `01_basic_usage.py` - Fundamental features and basic operations
- `02_dict_interface.py` - Dict-like interface and methods
- `03_open_ended_ranges.py` - Open-ended ranges with None bounds
- `04_overlap_strategies.py` - Overlap handling strategies
- `05_real_world_use_cases.py` - Production-ready examples
- `run_all.sh` - Run all examples at once

## 🚀 Running Examples

Run individual scripts:
```bash
python 01_basic_usage.py
python 02_dict_interface.py
python 03_open_ended_ranges.py
python 04_overlap_strategies.py
python 05_real_world_use_cases.py
```

Or run all at once:
```bash
bash run_all.sh
```

## 📓 Jupyter Notebooks

For interactive examples with pre-executed outputs, see the **[../examples/](../examples/)** directory which contains Jupyter notebooks (.ipynb files).

## 📚 Documentation

For comprehensive documentation, see [../examples/README.md](../examples/README.md)

