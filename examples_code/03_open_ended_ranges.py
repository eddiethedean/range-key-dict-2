"""
Open-Ended Ranges Examples for range-key-dict-2

This script demonstrates how to use None as infinity for unbounded ranges.
Run this file directly: python 03_open_ended_ranges.py
"""

from range_key_dict import RangeKeyDict


def example_1_negative_infinity():
    """Example 1: Using None as negative infinity"""
    print("=" * 70)
    print("Example 1: None as Negative Infinity")
    print("=" * 70)

    # (None, 0) means from negative infinity to 0
    rkd = RangeKeyDict({(None, 0): "negative"})

    test_values = [-1000000, -100, -1, -0.5]
    for value in test_values:
        print(f"{value:10.1f} → {rkd[value]}")

    print(f"\n0 in rkd: {0 in rkd} (0 is NOT included)")
    print()


def example_2_positive_infinity():
    """Example 2: Using None as positive infinity"""
    print("=" * 70)
    print("Example 2: None as Positive Infinity")
    print("=" * 70)

    # (0, None) means from 0 to positive infinity
    rkd = RangeKeyDict({(0, None): "non-negative"})

    test_values = [0, 1, 100, 1000000]
    for value in test_values:
        print(f"{value:10d} → {rkd[value]}")
    print()


def example_3_all_numbers():
    """Example 3: Both bounds as None (all numbers)"""
    print("=" * 70)
    print("Example 3: Both Bounds as None (All Numbers)")
    print("=" * 70)

    # (None, None) means all numbers from -∞ to +∞
    rkd = RangeKeyDict({(None, None): "everything"})

    test_values = [-1000000, -1, 0, 1, 1000000]
    for value in test_values:
        print(f"{value:10d} → {rkd[value]}")
    print()


def example_4_mixed_ranges():
    """Example 4: Mix of open-ended and closed ranges"""
    print("=" * 70)
    print("Example 4: Mixed Open-Ended and Closed Ranges")
    print("=" * 70)

    temperature = RangeKeyDict(
        {
            (None, 0): "freezing",  # (-∞, 0)
            (0, 20): "cold",  # [0, 20)
            (20, 30): "comfortable",  # [20, 30)
            (30, None): "hot",  # [30, +∞)
        }
    )

    test_temps = [-100, -1, 0, 10, 25, 30, 50, 100]
    for temp in test_temps:
        print(f"{temp:4d}°C → {temperature[temp]}")
    print()


def example_5_age_categories():
    """Example 5: Age categories with open ends"""
    print("=" * 70)
    print("Example 5: Age Categories")
    print("=" * 70)

    categories = RangeKeyDict(
        {
            (None, 13): "child",
            (13, 20): "teenager",
            (20, 65): "adult",
            (65, None): "senior",
        }
    )

    test_ages = [5, 16, 30, 70, 100]
    for age in test_ages:
        print(f"Age {age:3d} → {categories[age]}")
    print()


def example_6_grade_with_extra_credit():
    """Example 6: Grading system with extra credit"""
    print("=" * 70)
    print("Example 6: Grading System with Extra Credit")
    print("=" * 70)

    # F: < 60, D: 60-70, C: 70-80, B: 80-90, A: 90-100, A+: > 100
    grades = RangeKeyDict(
        {
            (None, 60): "F",
            (60, 70): "D",
            (70, 80): "C",
            (80, 90): "B",
            (90, 100): "A",
            (100, None): "A+",  # Extra credit!
        }
    )

    test_scores = [0, 50, 65, 75, 85, 95, 105, 200]
    print("Score → Grade")
    print("-" * 20)
    for score in test_scores:
        print(f"{score:3d} → {grades[score]}")
    print()


def example_7_income_brackets():
    """Example 7: Income tax brackets"""
    print("=" * 70)
    print("Example 7: Income Tax Brackets")
    print("=" * 70)

    tax_brackets = RangeKeyDict(
        {
            (None, 11000): 0.10,  # $0 to $11,000: 10%
            (11000, 44725): 0.12,
            (44725, 95375): 0.22,
            (95375, 182100): 0.24,
            (182100, 231250): 0.32,
            (231250, 578125): 0.35,
            (578125, None): 0.37,  # Over $578,125: 37%
        }
    )

    test_incomes = [5000, 50000, 100000, 500000, 1000000]
    print("Income → Tax Rate")
    print("-" * 35)
    for income in test_incomes:
        rate = tax_brackets[income]
        print(f"${income:,} → {rate:.0%}")
    print()


def example_8_network_qos():
    """Example 8: Network Quality of Service (QoS)"""
    print("=" * 70)
    print("Example 8: Network QoS Priority")
    print("=" * 70)

    qos_priority = RangeKeyDict(
        {
            (None, 100): "Critical",  # Very low latency
            (100, 500): "High",  # Low latency
            (500, 1000): "Medium",  # Normal latency
            (1000, None): "Low",  # High latency
        }
    )

    test_latencies = [50, 200, 750, 2000, 5000]
    print("Latency (ms) → Priority")
    print("-" * 30)
    for latency in test_latencies:
        priority = qos_priority[latency]
        print(f"{latency:5d}ms → {priority}")
    print()


def example_9_risk_assessment():
    """Example 9: Risk assessment levels"""
    print("=" * 70)
    print("Example 9: Risk Assessment")
    print("=" * 70)

    risk_levels = RangeKeyDict(
        {
            (None, 0): {"level": "Invalid", "action": "Review data"},
            (0, 25): {"level": "Low", "action": "Monitor"},
            (25, 50): {"level": "Medium", "action": "Review monthly"},
            (50, 75): {"level": "High", "action": "Review weekly"},
            (75, 100): {"level": "Critical", "action": "Immediate action"},
            (100, None): {"level": "Extreme", "action": "Emergency protocol"},
        }
    )

    test_scores = [-5, 10, 40, 60, 85, 120]
    print("Risk Score → Assessment")
    print("-" * 50)
    for score in test_scores:
        assessment = risk_levels[score]
        print(f"{score:4d} → {assessment['level']:10s} | {assessment['action']}")
    print()


def example_10_infinity_boundaries():
    """Example 10: Demonstrating infinity behavior"""
    print("=" * 70)
    print("Example 10: Infinity Boundaries")
    print("=" * 70)

    rkd = RangeKeyDict({(None, 0): "negative", (0, 100): "middle", (100, None): "positive"})

    # Test with extreme values
    extreme_values = [float("-inf"), -1e100, 0, 50, 100, 1e100, float("inf")]

    print("Testing extreme values:")
    for value in extreme_values:
        try:
            if value == float("-inf") or value == float("inf"):
                # Infinity values
                result = rkd.get(value, "N/A")
                print(f"  {str(value):>15s} → {result}")
            else:
                result = rkd[value]
                print(f"  {value:>15.2e} → {result}")
        except (KeyError, OverflowError) as e:
            print(f"  {value:>15s} → Error: {type(e).__name__}")
    print()


def main():
    """Run all examples"""
    print("\n" + "∞" * 35)
    print(" " * 8 + "range-key-dict-2 Open-Ended Ranges Examples")
    print("∞" * 35 + "\n")

    example_1_negative_infinity()
    example_2_positive_infinity()
    example_3_all_numbers()
    example_4_mixed_ranges()
    example_5_age_categories()
    example_6_grade_with_extra_credit()
    example_7_income_brackets()
    example_8_network_qos()
    example_9_risk_assessment()
    example_10_infinity_boundaries()

    print("=" * 70)
    print("✅ All open-ended range examples completed successfully!")
    print("=" * 70)
    print("\nNext: Run 04_overlap_strategies.py to learn about overlapping ranges\n")


if __name__ == "__main__":
    main()
