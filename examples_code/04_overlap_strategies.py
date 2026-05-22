"""
Overlap Strategies Examples for range-key-dict-2

This script demonstrates how to handle overlapping ranges with different strategies.
Run this file directly: python 04_overlap_strategies.py
"""

from typing import Any, Dict, List

from range_key_dict import OverlapStrategy, RangeKey, RangeKeyDict


def example_1_error_strategy():
    """Example 1: Error strategy (default)"""
    print("=" * 70)
    print("Example 1: Error Strategy (Default)")
    print("=" * 70)

    # By default, overlapping ranges raise an error
    try:
        _ = RangeKeyDict(
            {
                (0, 100): "A",
                (50, 150): "B",  # Overlaps with previous range
            }
        )
        print("No error - shouldn't reach here")
    except ValueError as e:
        print(f"✓ ValueError caught as expected: {e}")
    print()


def example_2_first_strategy():
    """Example 2: First strategy"""
    print("=" * 70)
    print("Example 2: First Strategy (First Inserted Wins)")
    print("=" * 70)

    rkd = RangeKeyDict(
        {
            (0, 100): "first",
            (50, 150): "second",
            (25, 75): "third",
        },
        overlap_strategy="first",
    )

    test_points = [10, 30, 60, 80, 120]
    for point in test_points:
        result = rkd[point]
        print(f"Point {point:3d} → {result}")

    print("\nNote: Returns the FIRST inserted range that contains the point")
    print()


def example_3_last_strategy():
    """Example 3: Last strategy"""
    print("=" * 70)
    print("Example 3: Last Strategy (Last Inserted Wins)")
    print("=" * 70)

    rkd = RangeKeyDict(
        {
            (0, 100): "first",
            (50, 150): "second",
            (25, 75): "third",
        },
        overlap_strategy="last",
    )

    test_points = [10, 30, 60, 80, 120]
    for point in test_points:
        result = rkd[point]
        print(f"Point {point:3d} → {result}")

    print("\nNote: Returns the LAST inserted range that contains the point")
    print()


def example_4_shortest_strategy():
    """Example 4: Shortest strategy"""
    print("=" * 70)
    print("Example 4: Shortest Strategy (Shortest Range Wins)")
    print("=" * 70)

    rkd = RangeKeyDict(
        {
            (0, 200): "long (200 units)",
            (50, 150): "medium (100 units)",
            (80, 90): "short (10 units)",
        },
        overlap_strategy="shortest",
    )

    test_points = [10, 60, 85, 100, 180]
    for point in test_points:
        if point in rkd:
            result = rkd[point]
            print(f"Point {point:3d} → {result}")
        else:
            print(f"Point {point:3d} → Not in any range")

    print("\nNote: Returns the SHORTEST range that contains the point")
    print()


def example_5_longest_strategy():
    """Example 5: Longest strategy"""
    print("=" * 70)
    print("Example 5: Longest Strategy (Longest Range Wins)")
    print("=" * 70)

    rkd = RangeKeyDict(
        {
            (0, 200): "long (200 units)",
            (50, 150): "medium (100 units)",
            (80, 90): "short (10 units)",
        },
        overlap_strategy="longest",
    )

    test_points = [10, 60, 85, 100, 180]
    for point in test_points:
        if point in rkd:
            result = rkd[point]
            print(f"Point {point:3d} → {result}")
        else:
            print(f"Point {point:3d} → Not in any range")

    print("\nNote: Returns the LONGEST range that contains the point")
    print()


def example_6_priority_system():
    """Example 6: Priority system using 'last' strategy"""
    print("=" * 70)
    print("Example 6: Priority System (Override Defaults)")
    print("=" * 70)

    # Default permissions for all users
    permissions = RangeKeyDict(overlap_strategy="last")

    # Add default permissions for all user IDs
    permissions[(0, 10000)] = {"read": True, "write": False, "admin": False}

    # Add special permissions for moderators
    permissions[(1000, 2000)] = {"read": True, "write": True, "admin": False}

    # Add admin permissions
    permissions[(1900, 1950)] = {"read": True, "write": True, "admin": True}

    test_users = [500, 1500, 1920, 5000]
    print("User ID → Permissions")
    print("-" * 40)
    for user_id in test_users:
        perms = permissions[user_id]
        print(f"  {user_id:4d} → R:{perms['read']}, W:{perms['write']}, A:{perms['admin']}")

    print("\nNote: Later (more specific) ranges override earlier ones")
    print()


def example_7_pricing_tiers():
    """Example 7: Pricing tiers with regional overrides"""
    print("=" * 70)
    print("Example 7: Pricing Tiers with Regional Overrides")
    print("=" * 70)

    # Use 'first' strategy so base prices can be overridden
    pricing = RangeKeyDict(overlap_strategy="first")

    # Add special pricing for specific customer tiers first
    pricing[(0, 1000)] = 15.99  # VIP pricing for customers 0-1000
    pricing[(5000, 6000)] = 12.99  # Partner pricing

    # Add standard pricing (these overlap but won't override due to 'first')
    pricing[(0, 10000)] = 19.99  # Standard pricing

    test_customers = [50, 500, 1500, 5500, 8000]
    print("Customer ID → Price")
    print("-" * 30)
    for customer_id in test_customers:
        price = pricing[customer_id]
        print(f"  {customer_id:5d} → ${price:.2f}")

    print("\nNote: VIP and Partner tiers get special pricing")
    print()


def example_8_service_levels():
    """Example 8: Service level agreement (SLA) with exceptions"""
    print("=" * 70)
    print("Example 8: Service Level Agreement (SLA) Tiers")
    print("=" * 70)

    # Use 'shortest' to prioritize more specific SLAs
    sla = RangeKeyDict(
        {
            (0, 1000000): {"response": "24h", "uptime": "99.0%"},  # Basic
            (100000, 500000): {"response": "4h", "uptime": "99.9%"},  # Business
            (200000, 300000): {
                "response": "1h",
                "uptime": "99.95%",
            },  # Premium
            (240000, 260000): {
                "response": "15min",
                "uptime": "99.99%",
            },  # Enterprise
        },
        overlap_strategy="shortest",
    )

    test_ids = [50000, 150000, 250000, 255000, 400000]
    print("Customer ID → SLA Level")
    print("-" * 50)
    for cust_id in test_ids:
        sla_terms = sla[cust_id]
        print(
            f"  {cust_id:6d} → Response: {sla_terms['response']:>6s}, Uptime: {sla_terms['uptime']}"
        )

    print("\nNote: Most specific (shortest) range wins")
    print()


def example_9_geo_restrictions():
    """Example 9: Geographic restrictions with special zones"""
    print("=" * 70)
    print("Example 9: Geographic Restrictions")
    print("=" * 70)

    # IP ranges with geographic restrictions
    # Using 'shortest' to prioritize specific zones
    geo_policy = RangeKeyDict(
        {
            (0, 1000000): {"region": "Global", "restrictions": []},
            (100000, 500000): {"region": "EMEA", "restrictions": ["export"]},
            (200000, 300000): {
                "region": "EU",
                "restrictions": ["export", "gdpr"],
            },
            (250000, 270000): {
                "region": "Germany",
                "restrictions": ["export", "gdpr", "local_data"],
            },
        },
        overlap_strategy="shortest",
    )

    test_ips = [50000, 150000, 250000, 265000, 450000]
    print("IP Range → Policy")
    print("-" * 60)
    for ip in test_ips:
        policy = geo_policy[ip]
        restrictions = ", ".join(policy["restrictions"]) if policy["restrictions"] else "None"
        print(f"  {ip:6d} → {policy['region']:10s} | Restrictions: {restrictions}")

    print("\nNote: More specific geographic zones have additional restrictions")
    print()


def example_10_comparing_strategies():
    """Example 10: Comparing all strategies side-by-side"""
    print("=" * 70)
    print("Example 10: Comparing All Strategies")
    print("=" * 70)

    ranges: Dict[RangeKey, Any] = {
        (0, 100): "Range A (0-100)",
        (50, 150): "Range B (50-150)",
        (80, 120): "Range C (80-120)",
    }

    strategies: List[OverlapStrategy] = ["first", "last", "shortest", "longest"]
    test_point = 90  # This point is in all three ranges

    print(f"Looking up point {test_point} (in all 3 ranges):\n")
    for strategy in strategies:
        rkd = RangeKeyDict(ranges, overlap_strategy=strategy)
        result = rkd[test_point]
        print(f"  {strategy:>10s} strategy → {result}")

    print("\nExplanation:")
    print("  - first:    Returns the first defined range (A)")
    print("  - last:     Returns the last defined range (C)")
    print("  - shortest: Returns the shortest range (C, 40 units)")
    print("  - longest:  Returns the longest range (B, 100 units)")
    print()


def main():
    """Run all examples"""
    print("\n" + "🔀" * 35)
    print(" " * 8 + "range-key-dict-2 Overlap Strategies Examples")
    print("🔀" * 35 + "\n")

    example_1_error_strategy()
    example_2_first_strategy()
    example_3_last_strategy()
    example_4_shortest_strategy()
    example_5_longest_strategy()
    example_6_priority_system()
    example_7_pricing_tiers()
    example_8_service_levels()
    example_9_geo_restrictions()
    example_10_comparing_strategies()

    print("=" * 70)
    print("✅ All overlap strategy examples completed successfully!")
    print("=" * 70)
    print("\nNext: Run 05_real_world_use_cases.py for comprehensive examples\n")


if __name__ == "__main__":
    main()
