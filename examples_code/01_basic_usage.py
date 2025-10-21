"""
Basic Usage Examples for range-key-dict-2

This script demonstrates the fundamental features of RangeKeyDict.
Run this file directly: python 01_basic_usage.py
"""

from range_key_dict import RangeKeyDict


def example_1_creating_basic_dict():
    """Example 1: Creating a basic RangeKeyDict"""
    print("=" * 70)
    print("Example 1: Creating a Basic RangeKeyDict")
    print("=" * 70)

    # Create a simple range dictionary for grade mapping
    grades = RangeKeyDict(
        {
            (0, 60): "F",
            (60, 70): "D",
            (70, 80): "C",
            (80, 90): "B",
            (90, 100): "A",
        }
    )

    print(f"Grade mapping created with {len(grades)} ranges\n")
    return grades


def example_2_looking_up_values(grades):
    """Example 2: Looking up values"""
    print("=" * 70)
    print("Example 2: Looking Up Values")
    print("=" * 70)

    test_scores = [45, 68, 75, 85, 95]

    for score in test_scores:
        grade = grades[score]
        print(f"Score {score:2d} → Grade {grade}")
    print()


def example_3_range_boundaries(grades):
    """Example 3: Understanding range boundaries [start, end)"""
    print("=" * 70)
    print("Example 3: Understanding Range Boundaries [start, end)")
    print("=" * 70)

    boundary_tests = [
        (59, "Should be F (just below 60)"),
        (60, "Should be D (60 is start of D range)"),
        (69, "Should be D (just below 70)"),
        (70, "Should be C (70 is start of C range)"),
    ]

    for score, description in boundary_tests:
        grade = grades[score]
        print(f"{score:2d}: {grade} - {description}")
    print()


def example_4_safe_lookups():
    """Example 4: Safe lookups with get()"""
    print("=" * 70)
    print("Example 4: Safe Lookups with get()")
    print("=" * 70)

    grades = RangeKeyDict({(0, 60): "F", (60, 70): "D", (70, 80): "C"})

    # Using get() with a default value
    print(f"Score 65: {grades.get(65)}")  # Returns 'D'
    print(f"Score 150 (with default): {grades.get(150, 'Out of range')}")
    print(f"Score -10 (with default): {grades.get(-10, 'Invalid score')}")
    print()


def example_5_checking_membership():
    """Example 5: Checking membership with 'in'"""
    print("=" * 70)
    print("Example 5: Checking Membership")
    print("=" * 70)

    grades = RangeKeyDict({(0, 60): "F", (60, 70): "D", (70, 100): "C+"})

    test_values = [50, 85, 100, 150, -10]

    for value in test_values:
        if value in grades:
            print(f"✓ {value:3d} is in a valid grade range: {grades[value]}")
        else:
            print(f"✗ {value:3d} is not in any grade range")
    print()


def example_6_working_with_floats():
    """Example 6: Working with float ranges"""
    print("=" * 70)
    print("Example 6: Working with Floats")
    print("=" * 70)

    temperature = RangeKeyDict(
        {
            (0.0, 10.0): "Cold",
            (10.0, 20.0): "Cool",
            (20.0, 30.0): "Comfortable",
            (30.0, 40.0): "Hot",
        }
    )

    temps = [5.5, 15.2, 25.8, 35.0, 12.3]
    for temp in temps:
        print(f"{temp:5.1f}°C: {temperature[temp]}")
    print()


def example_7_handling_keyerror():
    """Example 7: Handling KeyError"""
    print("=" * 70)
    print("Example 7: Handling KeyError")
    print("=" * 70)

    grades = RangeKeyDict({(0, 100): "Valid"})

    try:
        result = grades[150]
        print(f"Grade: {result}")
    except KeyError as e:
        print(f"KeyError caught: {e}")
        print("Tip: Use get() method with a default value to avoid this error")
    print()


def example_8_real_world_shipping_costs():
    """Example 8: Real-world shipping cost calculator"""
    print("=" * 70)
    print("Example 8: Real-World Example - Shipping Costs")
    print("=" * 70)

    shipping_costs = RangeKeyDict(
        {
            (0, 25): 5.99,
            (25, 50): 3.99,
            (50, 100): 1.99,
            (100, 1000): 0.00,  # Free shipping for orders $100+
        }
    )

    orders = [15.00, 30.50, 75.00, 125.00]

    print("Order Value → Shipping Cost")
    print("-" * 40)
    for order_value in orders:
        shipping = shipping_costs[order_value]
        total = order_value + shipping
        print(f"${order_value:7.2f} → ${shipping:5.2f} (Total: ${total:7.2f})")
    print()


def main():
    """Run all examples"""
    print("\n" + "🚀" * 35)
    print(" " * 10 + "range-key-dict-2 Basic Usage Examples")
    print("🚀" * 35 + "\n")

    # Run all examples
    grades = example_1_creating_basic_dict()
    example_2_looking_up_values(grades)
    example_3_range_boundaries(grades)
    example_4_safe_lookups()
    example_5_checking_membership()
    example_6_working_with_floats()
    example_7_handling_keyerror()
    example_8_real_world_shipping_costs()

    print("=" * 70)
    print("✅ All basic usage examples completed successfully!")
    print("=" * 70)
    print("\nNext: Run 02_dict_interface.py to learn about dict-like methods\n")


if __name__ == "__main__":
    main()
