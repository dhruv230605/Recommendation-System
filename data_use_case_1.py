import uuid
import random
import json
from datetime import datetime, timedelta

def now(): return datetime.now().isoformat()
def future(days): return (datetime.now() + timedelta(days=days)).isoformat()

def random_tags():
    return random.sample(["business", "urgent", "personal", "gift", "recurring", "travel"], k=random.randint(0, 3))

def location_data():
    return {
        "geocoordinates": [round(random.uniform(-90, 90), 6), round(random.uniform(-180, 180), 6)],
        "city": random.choice(["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"]),
        "country": "India"
    }

def generate_transaction():
    return {
        "transaction_id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),
        "timestamp": now(),
        "amount": round(random.uniform(100, 10000), 2),
        "currency": "INR",
        "category": random.choice(["dining", "electronics", "travel", "groceries"]),
        "merchant_name": random.choice(["Amazon", "Flipkart", "Swiggy", "Uber", "IRCTC"]),
        "payment_method": random.choice(["credit card", "debit card", "UPI", "net banking"]),
        "location": location_data(),
        "tags": random_tags(),
        "recurrence": {
            "is_recurring": random.choice([True, False]),
            "frequency": random.choice(["monthly", "weekly", "yearly", ""]) if random.choice([True, False]) else ""
        },
        "metadata": {
            "invoice_details": f"INV-{random.randint(1000,9999)}",
            "itemized_breakdown": [
                {"product": "Item A", "quantity": 1, "price": 499.0},
                {"product": "Item B", "quantity": 2, "price": 250.0}
            ],
            "loyalty_points_earned": random.randint(0, 100)
        },
        "keywords": ["transaction", "finance", "payment"],
        "created_at": now(),
        "updated_at": now(),
        "expiry_date": "",
        "compatible_user_profiles": ["frequent_shopper", "tech_savvy"],
        "prerequisites": []
    }

# Predefined offer templates
OFFER_TEMPLATES = [
    {
        "name": "Super Saver Offer",
        "description": "Get {discount}% cashback on {category} with a minimum spend of ₹{min_amount} at {merchant}.",
        "type": "cashback",
        "categories": ["dining", "electronics"],
        "min_amount_range": (500, 2000),
        "discount_range": (5, 20),
        "merchants": ["Zomato", "Flipkart", "Amazon", "Swiggy"]
    },
    {
        "name": "Weekend Special",
        "description": "Enjoy {discount}% off on {category} purchases this weekend at {merchant}.",
        "type": "discount",
        "categories": ["dining", "groceries"],
        "min_amount_range": (300, 1000),
        "discount_range": (10, 30),
        "merchants": ["Swiggy", "BigBasket", "Grofers"]
    },
    {
        "name": "First Purchase Bonus",
        "description": "Get {discount}% extra cashback on your first {category} purchase at {merchant}.",
        "type": "cashback",
        "categories": ["electronics", "travel"],
        "min_amount_range": (1000, 5000),
        "discount_range": (15, 25),
        "merchants": ["Amazon", "Flipkart", "MakeMyTrip"]
    }
]

def generate_offer():
    template = random.choice(OFFER_TEMPLATES)
    min_amount = random.randint(*template["min_amount_range"])
    discount = random.randint(*template["discount_range"])
    category = random.choice(template["categories"])
    merchant = random.choice(template["merchants"])
    
    return {
        "offer_id": str(uuid.uuid4()),
        "name": template["name"],
        "description": template["description"].format(
            discount=discount,
            category=category,
            min_amount=min_amount,
            merchant=merchant
        ),
        "type": template["type"],
        "applicable_categories": [category],
        "minimum_transaction_amount": min_amount,
        "discount_value": {
            "type": "percent",
            "value": discount
        },
        "validity_period": {
            "start_date": now(),
            "end_date": future(30)
        },
        "partner_merchants": [merchant],
        "targeting_rules": {
            "user_spending_threshold": min_amount * 2,
            "preferred_categories": [category],
            "risk_profile": "low"
        },
        "redemption": {
            "conditions": "Minimum 3 eligible transactions",
            "terms_link": "https://example.com/terms"
        },
        "keywords": ["offer", "cashback", "discount"],
        "created_at": now(),
        "updated_at": now(),
        "expiry_date": future(30),
        "compatible_user_profiles": ["young_professionals"],
        "prerequisites": []
    }

# Predefined asset templates
ASSET_TEMPLATES = [
    {
        "name": "HDFC Balanced Advantage Fund",
        "type": "mutual fund",
        "issuer": "HDFC",
        "risk_rating_range": (3, 5),
        "return_range": (8, 12),
        "liquidity": "medium",
        "min_investment_range": (5000, 10000)
    },
    {
        "name": "ICICI Prudential Technology Fund",
        "type": "mutual fund",
        "issuer": "ICICI",
        "risk_rating_range": (4, 5),
        "return_range": (12, 18),
        "liquidity": "medium",
        "min_investment_range": (5000, 15000)
    },
    {
        "name": "SBI Fixed Deposit",
        "type": "FD",
        "issuer": "SBI",
        "risk_rating_range": (1, 2),
        "return_range": (5, 7),
        "liquidity": "low",
        "min_investment_range": (10000, 50000)
    }
]

def generate_financial_asset():
    template = random.choice(ASSET_TEMPLATES)
    risk_rating = random.randint(*template["risk_rating_range"])
    expected_return = round(random.uniform(*template["return_range"]), 2)
    min_investment = random.randint(*template["min_investment_range"])
    
    return {
        "asset_id": str(uuid.uuid4()),
        "type": template["type"],
        "name": template["name"],
        "issuer": template["issuer"],
        "risk_rating": risk_rating,
        "expected_return": expected_return,
        "liquidity": template["liquidity"],
        "minimum_investment_amount": min_investment,
        "tenure": "5 years",
        "financial_details": {
            "historical_performance": {
                "2022": f"{round(expected_return - 2, 1)}%",
                "2023": f"{round(expected_return - 1, 1)}%"
            },
            "tax_implications": {
                "short_term": "15%",
                "long_term": "10% after 1 year"
            },
            "key_features": ["dividend-paying", "tax-saving"]
        },
        "metadata": {
            "regulatory_documents": ["https://example.com/prospectus.pdf"],
            "tags": ["ESG", "high-growth"]
        },
        "keywords": ["investment", template["type"], template["issuer"]],
        "created_at": now(),
        "updated_at": now(),
        "expiry_date": "",
        "compatible_user_profiles": ["investors", "retirees"],
        "prerequisites": ["Demat account"]
    }

# Predefined strategy templates
STRATEGY_TEMPLATES = [
    {
        "name": "Conservative Retirement Plan",
        "risk_profile": "conservative",
        "time_horizon": "long-term",
        "target_return_range": (7, 9),
        "allocation": {
            "FD": 40,
            "mutual_funds": 40,
            "bonds": 20
        }
    },
    {
        "name": "Aggressive Growth Strategy",
        "risk_profile": "aggressive",
        "time_horizon": "medium-term",
        "target_return_range": (12, 15),
        "allocation": {
            "equities": 60,
            "mutual_funds": 30,
            "crypto": 10
        }
    },
    {
        "name": "Balanced Income Portfolio",
        "risk_profile": "moderate",
        "time_horizon": "medium-term",
        "target_return_range": (9, 11),
        "allocation": {
            "mutual_funds": 50,
            "FD": 30,
            "equities": 20
        }
    }
]

def generate_investment_strategy():
    template = random.choice(STRATEGY_TEMPLATES)
    target_return = round(random.uniform(*template["target_return_range"]), 1)
    
    return {
        "strategy_id": str(uuid.uuid4()),
        "name": template["name"],
        "risk_profile": template["risk_profile"],
        "time_horizon": template["time_horizon"],
        "target_annual_return": target_return,
        "allocation_blueprint": template["allocation"],
        "performance_metrics": {
            "backtested_results": f"{round(target_return - 0.2, 1)}% CAGR over 10 years",
            "volatility_score": round(random.uniform(1.5, 2.5), 1),
            "tax_efficiency_rating": "high"
        },
        "user_requirements": {
            "minimum_capital": 100000,
            "recommended_account_types": ["Demat", "Savings"]
        },
        "keywords": ["investment", template["risk_profile"], "strategy"],
        "created_at": now(),
        "updated_at": now(),
        "expiry_date": "",
        "compatible_user_profiles": ["investors", "retirees"],
        "prerequisites": ["KYC", "Demat account"]
    }

# Generate mock data with more variety
mock_data = {
    "transactions": [generate_transaction() for _ in range(5)],
    "offers": [generate_offer() for _ in range(3)],
    "financial_assets": [generate_financial_asset() for _ in range(3)],
    "investment_strategies": [generate_investment_strategy() for _ in range(3)]
}

with open("mock_financial_data.json", "w") as f:
    json.dump(mock_data, f, indent=2)

print("Mock data generated successfully!")
