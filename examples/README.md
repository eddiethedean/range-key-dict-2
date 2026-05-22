# range-key-dict-2 Examples

This directory contains **Jupyter notebooks** with comprehensive examples demonstrating all features of `range-key-dict-2` (version **2.1.0**).

## Range semantics (read first)

- **Half-open keys** `(start, end)` match `[start, end)` — `start` is included, `end` is excluded.
- **Point keys** `(n, n)` match only the single value `n` (useful for exact thresholds).
- **`None` bounds** mean negative or positive infinity, e.g. `(None, 0)` or `(0, None)`.
- **Overlapping ranges** require an `overlap_strategy` other than the default `'error'`.

## 📓 Format Options

Each example is available in **two formats**:

1. **Jupyter Notebooks** (`.ipynb`) - **This directory** - Interactive with pre-executed outputs
2. **Python Scripts** (`.py`) - **[../examples_code/](../examples_code/)** directory - Run from command line

Both formats contain identical examples - choose based on your preference!

## 📚 Example Scripts

### 1. Basic Usage
**Notebook:** `01_basic_usage.ipynb` (this directory)  
**Python Script:** `../examples_code/01_basic_usage.py`

Learn the fundamentals:
- Creating a RangeKeyDict
- Looking up values
- Understanding range boundaries `[start, end)` and point keys `(n, n)`
- Safe lookups with `get()`
- Checking membership with `in`
- Working with floats
- Real-world shipping cost calculator

### 2. Dict Interface
**Notebook:** `02_dict_interface.ipynb` (this directory)  
**Python Script:** `../examples_code/02_dict_interface.py`

Master the dict-like API:
- Creating empty dicts
- Adding ranges with `[key] = value`
- Updating existing ranges
- Using `keys()`, `values()`, `items()`
- Iterating over ranges
- Deleting ranges with `del`
- String representations
- Equality comparison
- Dynamic system building

### 3. Open-Ended Ranges
**Notebook:** `03_open_ended_ranges.ipynb` (this directory)  
**Python Script:** `../examples_code/03_open_ended_ranges.py`

Work with infinity:
- Using `None` as negative infinity `(None, 100)`
- Using `None` as positive infinity `(100, None)`
- All numbers range `(None, None)`
- Mixed open and closed ranges
- Age categories
- Grading with extra credit
- Income tax brackets
- Network QoS
- Risk assessment

### 4. Overlap Strategies
**Notebook:** `04_overlap_strategies.ipynb` (this directory)  
**Python Script:** `../examples_code/04_overlap_strategies.py`

Handle overlapping ranges:
- **Error strategy** (default) - Raises ValueError
- **First strategy** - Returns first inserted range
- **Last strategy** - Returns last inserted range (useful for overrides)
- **Shortest strategy** - Returns shortest matching range
- **Longest strategy** - Returns longest matching range
- Priority systems
- Pricing tiers with regional overrides
- Service level agreements
- Geographic restrictions

### 5. Real-World Use Cases
**Notebook:** `05_real_world_use_cases.ipynb` (this directory)  
**Python Script:** `../examples_code/05_real_world_use_cases.py`

Production-ready examples:
1. HTTP status code categorization
2. Smart shipping calculator
3. Progressive tax calculator
4. Credit score rating system
5. BMI calculator
6. API rate limiting tiers
7. Age-based ticket pricing
8. Server auto-scaling configuration
9. Environmental monitoring alerts
10. Customer lifetime value segmentation

## 🚀 Quick Start

### Option 1: Jupyter Notebooks (Recommended)

```bash
# Start Jupyter from this directory
cd examples
jupyter notebook

# Or Jupyter Lab
jupyter lab
```

Then open any `.ipynb` file. **All notebooks include pre-executed outputs** so you can see results immediately!

### Option 2: Python Scripts

```bash
# Run from examples_code directory
cd examples_code

# Run individual scripts
python 01_basic_usage.py
python 02_dict_interface.py
python 03_open_ended_ranges.py
python 04_overlap_strategies.py
python 05_real_world_use_cases.py

# Or run all at once
bash run_all.sh
```

## 📝 Example Output

Each script provides detailed, formatted output showing:
- ✅ What feature is being demonstrated
- 📊 Input and output examples
- 💡 Explanatory notes
- 🎯 Real-world context

Example:

```
======================================================================
Example 1: Creating a Basic RangeKeyDict
======================================================================
Grade mapping created with 5 ranges

======================================================================
Example 2: Looking Up Values
======================================================================
Score 45 → Grade F
Score 68 → Grade D
Score 75 → Grade C
Score 85 → Grade B
Score 95 → Grade A
```

## 🔧 Requirements

- Python 3.8+
- range-key-dict-2 package

```bash
pip install range-key-dict-2
```

Or if running from the repository:

```bash
# From project root
pip install -e .
```

## 📖 Learning Path

We recommend following the examples in order:

1. **Start here** → `01_basic_usage.py` - Learn the basics
2. **Next** → `02_dict_interface.py` - Master dict operations
3. **Then** → `03_open_ended_ranges.py` - Understand infinity bounds
4. **After** → `04_overlap_strategies.py` - Handle complex scenarios
5. **Finally** → `05_real_world_use_cases.py` - See production examples

## 💡 Use Case Index

Find examples by use case:

### E-Commerce
- Shipping costs (01, 02, 05)
- Discount systems (02, 04)
- Pricing tiers (04, 05)
- Customer segmentation (05)

### Finance
- Tax calculations (05)
- Credit scoring (05)
- Income brackets (03)

### System Administration
- Server auto-scaling (05)
- API rate limiting (05)
- Service level agreements (04)

### Web Development
- HTTP status codes (05)
- Geographic restrictions (04)

### Healthcare/Wellness
- BMI calculator (05)
- Age categorization (03, 05)

### Monitoring
- Environmental alerts (05)
- Network QoS (03)
- Risk assessment (03)

## 🎓 Code Snippets

### Quick Copy-Paste Examples

**Simple Grade Mapper:**
```python
from range_key_dict import RangeKeyDict

grades = RangeKeyDict({
    (0, 60): 'F',
    (60, 70): 'D',
    (70, 80): 'C',
    (80, 90): 'B',
    (90, 100): 'A',
})

print(grades[85])  # Output: B
```

**Infinite Ranges:**
```python
temperature = RangeKeyDict({
    (None, 0): 'freezing',
    (0, 20): 'cold',
    (20, 30): 'comfortable',
    (30, None): 'hot',
})

print(temperature[-100])  # Output: freezing
print(temperature[1000])  # Output: hot
```

**Overlap Strategy:**
```python
# VIP customers override default pricing
pricing = RangeKeyDict({
    (0, 1000): 15.99,  # VIP price
    (0, 10000): 19.99,  # Standard price
}, overlap_strategy='first')

print(pricing[500])  # Output: 15.99 (VIP)
print(pricing[5000])  # Output: 19.99 (Standard)
```

**Point Range (exact value):**
```python
flags = RangeKeyDict({(404, 404): "not_found"})
print(flags[404])  # Output: not_found
print(404.0 in flags)  # True
print(403 in flags)  # False
```

## 🧪 Testing the Examples

All examples include inline assertions and validations. If an example completes without errors, all tests passed!

```bash
# Test a specific example
python 01_basic_usage.py && echo "✅ All tests passed!"

# Test all examples
for file in 0*.py; do 
    python "$file" && echo "✅ $file passed" || echo "❌ $file failed"
done
```

## 📚 Additional Resources

- [Main README](../README.md) - Full package documentation
- [API Reference](../range_key_dict/range_key_dict.py) - Source code with docstrings
- [Tests](../tests/) - Comprehensive test suite
- [GitHub](https://github.com/eddiethedean/range-key-dict-2) - Report issues, contribute

## 🤝 Contributing Examples

Have a great use case? We'd love to add it!

1. Create a new example script: `0X_your_example.py`
2. Follow the existing format with detailed comments
3. Include 5-10 practical demonstrations
4. Test thoroughly
5. Submit a pull request

## 💬 Questions?

- 📖 Read the [main documentation](../README.md)
- 🐛 [Report issues](https://github.com/eddiethedean/range-key-dict-2/issues)
- 💡 [Start a discussion](https://github.com/eddiethedean/range-key-dict-2/discussions)

---

**Happy coding with range-key-dict-2!** 🚀

