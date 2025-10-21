"""
Real-World Use Cases for range-key-dict-2

This script demonstrates practical, production-ready use cases.
Run this file directly: python 05_real_world_use_cases.py
"""

from range_key_dict import RangeKeyDict


def example_1_http_status_codes():
    """Example 1: HTTP status code categorization"""
    print("=" * 70)
    print("Example 1: HTTP Status Code Categorization")
    print("=" * 70)

    http_categories = RangeKeyDict(
        {
            (100, 200): "Informational",
            (200, 300): "Success",
            (300, 400): "Redirection",
            (400, 500): "Client Error",
            (500, 600): "Server Error",
        }
    )

    test_codes = [200, 201, 301, 404, 500, 503]
    print("Status Code → Category")
    print("-" * 30)
    for code in test_codes:
        category = http_categories[code]
        print(f"  {code} → {category}")
    print()


def example_2_shipping_calculator():
    """Example 2: Smart shipping cost calculator"""
    print("=" * 70)
    print("Example 2: Smart Shipping Cost Calculator")
    print("=" * 70)

    # Shipping costs based on order value and weight
    shipping_by_value = RangeKeyDict(
        {
            (0, 25): 5.99,
            (25, 50): 3.99,
            (50, 100): 1.99,
            (100, None): 0.00,  # Free shipping over $100
        }
    )

    shipping_by_weight = RangeKeyDict(
        {
            (0, 1): 2.99,  # Up to 1 lb
            (1, 5): 4.99,  # 1-5 lbs
            (5, 10): 7.99,  # 5-10 lbs
            (10, None): 12.99,  # Over 10 lbs
        }
    )

    orders = [
        {"value": 15.00, "weight": 0.5},
        {"value": 75.00, "weight": 3.0},
        {"value": 125.00, "weight": 8.0},
        {"value": 40.00, "weight": 12.0},
    ]

    print("Order Value | Weight | Value-Based | Weight-Based | Actual")
    print("-" * 70)
    for order in orders:
        value_shipping = shipping_by_value[order["value"]]
        weight_shipping = shipping_by_weight[order["weight"]]
        # Use the higher of the two
        actual_shipping = max(value_shipping, weight_shipping)

        print(
            f"  ${order['value']:6.2f}  | {order['weight']:4.1f} lb | "
            f"  ${value_shipping:5.2f}   |   ${weight_shipping:5.2f}    | "
            f"${actual_shipping:5.2f}"
        )
    print()


def example_3_progressive_tax_calculator():
    """Example 3: Progressive tax calculator"""
    print("=" * 70)
    print("Example 3: Progressive Tax Calculator")
    print("=" * 70)

    tax_brackets_2024 = RangeKeyDict(
        {
            (0, 11000): 0.10,
            (11000, 44725): 0.12,
            (44725, 95375): 0.22,
            (95375, 182100): 0.24,
            (182100, 231250): 0.32,
            (231250, 578125): 0.35,
            (578125, None): 0.37,
        }
    )

    def calculate_progressive_tax(income):
        """Calculate tax using progressive brackets"""
        total_tax = 0
        remaining = income

        for (start, end), rate in tax_brackets_2024.items():
            bracket_start = start if start is not None else 0
            bracket_end = end if end is not None else income

            if remaining <= 0:
                break

            taxable_in_bracket = min(remaining, bracket_end - bracket_start)
            tax_in_bracket = taxable_in_bracket * rate
            total_tax += tax_in_bracket
            remaining -= taxable_in_bracket

        return total_tax

    test_incomes = [30000, 75000, 150000, 500000, 1000000]
    print("Income → Tax (Effective Rate)")
    print("-" * 45)
    for income in test_incomes:
        tax = calculate_progressive_tax(income)
        effective_rate = (tax / income) * 100
        print(f"  ${income:>8,} → ${tax:>10,.2f} ({effective_rate:.2f}%)")
    print()


def example_4_credit_score_rating():
    """Example 4: Credit score to rating system"""
    print("=" * 70)
    print("Example 4: Credit Score Rating System")
    print("=" * 70)

    credit_ratings = RangeKeyDict(
        {
            (None, 580): {"rating": "Poor", "apr": 24.99, "approval_chance": 20},
            (580, 670): {"rating": "Fair", "apr": 19.99, "approval_chance": 50},
            (670, 740): {"rating": "Good", "apr": 14.99, "approval_chance": 75},
            (740, 800): {"rating": "Very Good", "apr": 10.99, "approval_chance": 90},
            (800, None): {
                "rating": "Excellent",
                "apr": 7.99,
                "approval_chance": 98,
            },
        }
    )

    test_scores = [520, 620, 700, 760, 820]
    print("Credit Score → Rating | APR | Approval %")
    print("-" * 55)
    for score in test_scores:
        info = credit_ratings[score]
        print(
            f"  {score:3d} → {info['rating']:12s} | {info['apr']:5.2f}% | "
            f"{info['approval_chance']:3d}%"
        )
    print()


def example_5_bmi_calculator():
    """Example 5: BMI (Body Mass Index) calculator"""
    print("=" * 70)
    print("Example 5: BMI Calculator")
    print("=" * 70)

    bmi_categories = RangeKeyDict(
        {
            (None, 18.5): {"category": "Underweight", "risk": "Malnutrition risk"},
            (18.5, 25): {"category": "Normal", "risk": "Low risk"},
            (25, 30): {"category": "Overweight", "risk": "Moderate risk"},
            (30, 35): {"category": "Obese Class I", "risk": "High risk"},
            (35, 40): {"category": "Obese Class II", "risk": "Very high risk"},
            (40, None): {"category": "Obese Class III", "risk": "Extremely high risk"},
        }
    )

    test_bmis = [16.5, 22.0, 27.5, 32.0, 42.0]
    print("BMI → Category | Health Risk")
    print("-" * 60)
    for bmi in test_bmis:
        info = bmi_categories[bmi]
        print(f"  {bmi:4.1f} → {info['category']:16s} | {info['risk']}")
    print()


def example_6_api_rate_limiting():
    """Example 6: API rate limiting tiers"""
    print("=" * 70)
    print("Example 6: API Rate Limiting Tiers")
    print("=" * 70)

    rate_limits = RangeKeyDict(
        {
            (0, 100): {"tier": "Free", "requests_per_hour": 100, "cost": 0.00},
            (100, 1000): {
                "tier": "Basic",
                "requests_per_hour": 1000,
                "cost": 9.99,
            },
            (1000, 10000): {
                "tier": "Pro",
                "requests_per_hour": 10000,
                "cost": 49.99,
            },
            (10000, 100000): {
                "tier": "Business",
                "requests_per_hour": 100000,
                "cost": 199.99,
            },
            (100000, None): {
                "tier": "Enterprise",
                "requests_per_hour": float("inf"),
                "cost": 999.99,
            },
        }
    )

    # Simulate API request counts
    test_users = [
        ("user_123", 50),
        ("startup_456", 500),
        ("company_789", 5000),
        ("enterprise_001", 50000),
        ("mega_corp_999", 500000),
    ]

    print("User | Requests | Tier | Rate Limit | Monthly Cost")
    print("-" * 75)
    for user_id, request_count in test_users:
        limits = rate_limits[request_count]
        req_limit = (
            "Unlimited"
            if limits["requests_per_hour"] == float("inf")
            else f"{limits['requests_per_hour']:,}/hr"
        )
        print(
            f"  {user_id:15s} | {request_count:8,} | {limits['tier']:10s} | "
            f"{req_limit:>12s} | ${limits['cost']:7.2f}"
        )
    print()


def example_7_age_based_pricing():
    """Example 7: Age-based ticket pricing"""
    print("=" * 70)
    print("Example 7: Age-Based Ticket Pricing")
    print("=" * 70)

    ticket_prices = RangeKeyDict(
        {
            (None, 3): {"category": "Infant", "price": 0.00, "restrictions": []},
            (3, 12): {
                "category": "Child",
                "price": 15.00,
                "restrictions": ["Adult supervision required"],
            },
            (12, 18): {
                "category": "Teen",
                "price": 25.00,
                "restrictions": ["Student ID for discount"],
            },
            (18, 65): {"category": "Adult", "price": 35.00, "restrictions": []},
            (65, None): {
                "category": "Senior",
                "price": 20.00,
                "restrictions": ["ID verification"],
            },
        }
    )

    family = [
        ("Baby Emma", 1),
        ("Child Noah", 8),
        ("Teen Olivia", 15),
        ("Parent James", 42),
        ("Parent Sarah", 40),
        ("Grandpa Robert", 72),
    ]

    total_cost = 0
    print("Name | Age | Category | Price")
    print("-" * 50)
    for name, age in family:
        pricing = ticket_prices[age]
        print(f"  {name:15s} | {age:3d} | {pricing['category']:8s} | ${pricing['price']:5.2f}")
        total_cost += pricing["price"]

    print("-" * 50)
    print(f"{'Total Family Cost:':33s} ${total_cost:.2f}")
    print()


def example_8_server_auto_scaling():
    """Example 8: Auto-scaling configuration"""
    print("=" * 70)
    print("Example 8: Server Auto-Scaling Configuration")
    print("=" * 70)

    scaling_config = RangeKeyDict(
        {
            (0, 100): {"instances": 1, "cpu_limit": "50%", "memory": "512MB"},
            (100, 1000): {"instances": 2, "cpu_limit": "70%", "memory": "1GB"},
            (1000, 5000): {"instances": 5, "cpu_limit": "80%", "memory": "2GB"},
            (5000, 20000): {"instances": 10, "cpu_limit": "85%", "memory": "4GB"},
            (20000, None): {"instances": 20, "cpu_limit": "90%", "memory": "8GB"},
        }
    )

    # Simulate load changes throughout the day
    load_scenarios = [
        ("Night (low traffic)", 50),
        ("Morning rush", 2500),
        ("Lunch peak", 7500),
        ("Afternoon steady", 3000),
        ("Evening spike", 15000),
        ("Black Friday", 50000),
    ]

    print("Time Period | Load | Instances | CPU Limit | Memory")
    print("-" * 70)
    for period, concurrent_users in load_scenarios:
        config = scaling_config[concurrent_users]
        print(
            f"  {period:22s} | {concurrent_users:5d} | {config['instances']:9d} | "
            f"{config['cpu_limit']:9s} | {config['memory']}"
        )
    print()


def example_9_environmental_monitoring():
    """Example 9: Environmental monitoring alerts"""
    print("=" * 70)
    print("Example 9: Environmental Monitoring System")
    print("=" * 70)

    temperature_alerts = RangeKeyDict(
        {
            (None, 0): {"level": "CRITICAL", "action": "Heating system failure"},
            (0, 15): {"level": "WARNING", "action": "Temperature too low"},
            (15, 25): {"level": "NORMAL", "action": "Monitor"},
            (25, 30): {"level": "WARNING", "action": "Temperature elevated"},
            (30, None): {"level": "CRITICAL", "action": "Cooling system failure"},
        }
    )

    humidity_alerts = RangeKeyDict(
        {
            (None, 30): {"level": "WARNING", "action": "Too dry"},
            (30, 60): {"level": "NORMAL", "action": "Monitor"},
            (60, None): {"level": "WARNING", "action": "Too humid"},
        }
    )

    readings = [
        {"temp": -5, "humidity": 40},
        {"temp": 20, "humidity": 45},
        {"temp": 28, "humidity": 70},
        {"temp": 35, "humidity": 25},
    ]

    print("Reading | Temperature Alert | Humidity Alert")
    print("-" * 80)
    for i, reading in enumerate(readings, 1):
        temp_alert = temperature_alerts[reading["temp"]]
        humid_alert = humidity_alerts[reading["humidity"]]
        print(
            f"  #{i:2d}    | {temp_alert['level']:8s}: {temp_alert['action']:25s} | "
            f"{humid_alert['level']:8s}: {humid_alert['action']}"
        )
    print()


def example_10_customer_segmentation():
    """Example 10: Customer lifetime value segmentation"""
    print("=" * 70)
    print("Example 10: Customer Lifetime Value Segmentation")
    print("=" * 70)

    clv_segments = RangeKeyDict(
        {
            (0, 100): {
                "segment": "Bronze",
                "perks": ["Basic support"],
                "discount": 0,
            },
            (100, 500): {
                "segment": "Silver",
                "perks": ["Priority support", "10% discount"],
                "discount": 10,
            },
            (500, 2000): {
                "segment": "Gold",
                "perks": ["24/7 support", "15% discount", "Free shipping"],
                "discount": 15,
            },
            (2000, 10000): {
                "segment": "Platinum",
                "perks": [
                    "Dedicated manager",
                    "20% discount",
                    "Free shipping",
                    "Early access",
                ],
                "discount": 20,
            },
            (10000, None): {
                "segment": "Diamond",
                "perks": [
                    "VIP manager",
                    "30% discount",
                    "Free shipping",
                    "Exclusive products",
                    "Private sales",
                ],
                "discount": 30,
            },
        }
    )

    customers = [
        ("Alice", 75),
        ("Bob", 350),
        ("Charlie", 1200),
        ("Diana", 5500),
        ("Eve", 25000),
    ]

    print("Customer | Lifetime Value | Segment | Discount | Perks")
    print("-" * 90)
    for name, clv in customers:
        segment_info = clv_segments[clv]
        perks = ", ".join(segment_info["perks"][:2])  # Show first 2 perks
        if len(segment_info["perks"]) > 2:
            perks += "..."
        print(
            f"  {name:10s} | ${clv:10,.2f}     | {segment_info['segment']:8s} | "
            f"{segment_info['discount']:3d}%     | {perks}"
        )
    print()


def main():
    """Run all examples"""
    print("\n" + "🌍" * 35)
    print(" " * 10 + "range-key-dict-2 Real-World Use Cases")
    print("🌍" * 35 + "\n")

    example_1_http_status_codes()
    example_2_shipping_calculator()
    example_3_progressive_tax_calculator()
    example_4_credit_score_rating()
    example_5_bmi_calculator()
    example_6_api_rate_limiting()
    example_7_age_based_pricing()
    example_8_server_auto_scaling()
    example_9_environmental_monitoring()
    example_10_customer_segmentation()

    print("=" * 70)
    print("✅ All real-world use case examples completed successfully!")
    print("=" * 70)
    print("\n🎉 You've completed all example scripts!")
    print("📚 Check out the examples/README.md for more information\n")


if __name__ == "__main__":
    main()
