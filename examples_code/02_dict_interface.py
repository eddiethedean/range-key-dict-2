"""
Dict-Like Interface Examples for range-key-dict-2

This script demonstrates the full dictionary-like interface of RangeKeyDict.
Run this file directly: python 02_dict_interface.py
"""

from range_key_dict import RangeKeyDict


def example_1_empty_dict():
    """Example 1: Creating and using an empty RangeKeyDict"""
    print("=" * 70)
    print("Example 1: Creating an Empty RangeKeyDict")
    print("=" * 70)

    rkd = RangeKeyDict()
    print(f"Empty dict, length: {len(rkd)}")
    print(f"Is empty: {len(rkd) == 0}\n")
    return rkd


def example_2_adding_ranges(rkd):
    """Example 2: Adding ranges with __setitem__"""
    print("=" * 70)
    print("Example 2: Adding Ranges")
    print("=" * 70)

    rkd[(0, 100)] = "Low"
    rkd[(100, 200)] = "Medium"
    rkd[(200, 300)] = "High"

    print(f"After adding 3 ranges: {len(rkd)}")
    print(f"Value at 50: {rkd[50]}")
    print(f"Value at 150: {rkd[150]}")
    print(f"Value at 250: {rkd[250]}\n")
    return rkd


def example_3_updating_ranges(rkd):
    """Example 3: Updating existing ranges"""
    print("=" * 70)
    print("Example 3: Updating Existing Ranges")
    print("=" * 70)

    print(f"Before update: {rkd[150]}")
    rkd[(100, 200)] = "Updated Medium"
    print(f"After update: {rkd[150]}")
    print(f"Length unchanged: {len(rkd)}\n")


def example_4_viewing_keys_values_items():
    """Example 4: Viewing keys, values, and items"""
    print("=" * 70)
    print("Example 4: Viewing Keys, Values, and Items")
    print("=" * 70)

    rkd = RangeKeyDict({(0, 100): "A", (100, 200): "B", (200, 300): "C"})

    print("Keys (ranges):")
    for key in rkd.keys():
        print(f"  {key}")

    print("\nValues:")
    for value in rkd.values():
        print(f"  {value}")

    print("\nItems (range, value pairs):")
    for key, value in rkd.items():
        print(f"  {key} → {value}")
    print()


def example_5_iterating():
    """Example 5: Iterating over ranges"""
    print("=" * 70)
    print("Example 5: Iterating Over Ranges")
    print("=" * 70)

    rkd = RangeKeyDict({(0, 10): "first", (10, 20): "second", (20, 30): "third"})

    print("Direct iteration returns keys:")
    for range_key, value in rkd.items():
        print(f"  Range {range_key}: value = {value}")
    print()


def example_6_deleting_ranges():
    """Example 6: Deleting ranges"""
    print("=" * 70)
    print("Example 6: Deleting Ranges")
    print("=" * 70)

    rkd = RangeKeyDict({(0, 100): "A", (100, 200): "B", (200, 300): "C"})

    print(f"Before deletion: {len(rkd)} ranges")
    print(f"Keys: {rkd.keys()}")

    del rkd[(100, 200)]

    print(f"\nAfter deletion: {len(rkd)} ranges")
    print(f"Keys: {rkd.keys()}")

    print(f"\n150 in rkd: {150 in rkd} (was in deleted range)")
    print(f"50 in rkd: {50 in rkd} (still in remaining range)\n")


def example_7_string_representation():
    """Example 7: String representations"""
    print("=" * 70)
    print("Example 7: String Representations")
    print("=" * 70)

    demo = RangeKeyDict({(0, 10): "A", (10, 20): "B", (20, 30): "C"})

    print("repr():")
    print(repr(demo))

    print("\nstr():")
    print(str(demo))
    print()


def example_8_equality():
    """Example 8: Equality comparison"""
    print("=" * 70)
    print("Example 8: Equality Comparison")
    print("=" * 70)

    dict1 = RangeKeyDict({(0, 100): "A", (100, 200): "B"})
    dict2 = RangeKeyDict({(0, 100): "A", (100, 200): "B"})
    dict3 = RangeKeyDict({(0, 100): "A"})

    print(f"dict1 == dict2: {dict1 == dict2}")
    print(f"dict1 == dict3: {dict1 == dict3}")
    print(f"dict1 != dict3: {dict1 != dict3}\n")


def example_9_dynamic_configuration():
    """Example 9: Building a dynamic configuration system"""
    print("=" * 70)
    print("Example 9: Dynamic Configuration System")
    print("=" * 70)

    server_config = RangeKeyDict()

    configs = [
        ((0, 100), {"instances": 1, "memory": "512MB"}),
        ((100, 1000), {"instances": 2, "memory": "1GB"}),
        ((1000, 10000), {"instances": 5, "memory": "2GB"}),
        ((10000, 100000), {"instances": 10, "memory": "4GB"}),
    ]

    for range_key, config in configs:
        server_config[range_key] = config
        print(f"Added config for {range_key[0]}-{range_key[1]} users")

    print(f"\nTotal configurations: {len(server_config)}")

    test_users = [50, 500, 5000, 50000]
    print("\nRecommended configurations:")
    for users in test_users:
        config = server_config[users]
        print(f"  {users:5d} users → {config['instances']} instances, {config['memory']}")
    print()


def example_10_discount_system():
    """Example 10: Dynamic discount system"""
    print("=" * 70)
    print("Example 10: Dynamic Discount System")
    print("=" * 70)

    discounts = RangeKeyDict()
    discounts[(0, 100)] = 0.0
    discounts[(100, 500)] = 0.05
    discounts[(500, 1000)] = 0.10

    print("Initial discount structure:")
    for range_key, discount in discounts.items():
        print(f"  ${range_key[0]}-${range_key[1]}: {discount * 100:.0f}% off")

    discounts[(1000, 10000)] = 0.15
    print("\n✓ Added VIP tier (15% off for orders $1000+)")

    discounts[(500, 1000)] = 0.12
    print("✓ Updated mid-tier discount to 12%")

    orders = [50, 250, 750, 2000]
    print("\nCalculating discounts:")
    for order_value in orders:
        discount_rate = discounts[order_value]
        discount_amount = order_value * discount_rate
        final_price = order_value - discount_amount
        print(f"  ${order_value:6.2f} → {discount_rate * 100:2.0f}% off = ${final_price:.2f}")
    print()


def main():
    """Run all examples"""
    print("\n" + "📚" * 35)
    print(" " * 10 + "range-key-dict-2 Dict Interface Examples")
    print("📚" * 35 + "\n")

    rkd = example_1_empty_dict()
    rkd = example_2_adding_ranges(rkd)
    example_3_updating_ranges(rkd)
    example_4_viewing_keys_values_items()
    example_5_iterating()
    example_6_deleting_ranges()
    example_7_string_representation()
    example_8_equality()
    example_9_dynamic_configuration()
    example_10_discount_system()

    print("=" * 70)
    print("✅ All dict interface examples completed successfully!")
    print("=" * 70)
    print("\nNext: Run 03_open_ended_ranges.py to learn about infinite bounds\n")


if __name__ == "__main__":
    main()
