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

def generate_offer():
    return {
        "offer_id": str(uuid.uuid4()),
        "name": "Super Saver Offer",
        "description": "Get 10% cashback on dining with a minimum spend of ₹1000 at Zomato and Flipkart.",
        "type": random.choice(["cashback", "discount", "reward points"]),
        "applicable_categories": ["dining", "electronics"],
        "minimum_transaction_amount": 1000,
        "discount_value": {"type": "percent", "value": 10},
        "validity_period": {"start_date": now(), "end_date": future(30)},
        "partner_merchants": ["Zomato", "Flipkart"],
        "targeting_rules": {
            "user_spending_threshold": 3000,
            "preferred_categories": ["dining"],
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

def generate_financial_asset():
    return {
        "asset_id": str(uuid.uuid4()),
        "type": random.choice(["mutual fund", "FD", "crypto", "bond"]),
        "name": "HDFC Balanced Advantage Fund",
        "issuer": "HDFC",
        "risk_rating": random.randint(1, 5),
        "expected_return": round(random.uniform(5.0, 15.0), 2),
        "liquidity": random.choice(["high", "medium", "low"]),
        "minimum_investment_amount": 5000,
        "tenure": "5 years",
        "financial_details": {
            "historical_performance": {
                "2022": "12.3%",
                "2023": "10.5%"
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
        "keywords": ["investment", "mutual fund", "HDFC"],
        "created_at": now(),
        "updated_at": now(),
        "expiry_date": "",
        "compatible_user_profiles": ["investors", "retirees"],
        "prerequisites": ["Demat account"]
    }

def generate_investment_strategy():
    return {
        "strategy_id": str(uuid.uuid4()),
        "name": "Conservative Retirement Plan",
        "risk_profile": "conservative",
        "time_horizon": "long-term",
        "target_annual_return": 8.0,
        "allocation_blueprint": {
            "FD": 40,
            "mutual_funds": 40,
            "bonds": 20
        },
        "performance_metrics": {
            "backtested_results": "7.8% CAGR over 10 years",
            "volatility_score": 1.9,
            "tax_efficiency_rating": "high"
        },
        "user_requirements": {
            "minimum_capital": 100000,
            "recommended_account_types": ["Demat", "Savings"]
        },
        "keywords": ["retirement", "low-risk", "strategy"],
        "created_at": now(),
        "updated_at": now(),
        "expiry_date": "",
        "compatible_user_profiles": ["retirees", "risk_averse"],
        "prerequisites": ["KYC", "Demat account"]
    }


mock_data = {
    "transactions": [generate_transaction() for _ in range(5)],
    "offers": [generate_offer() for _ in range(3)],
    "financial_assets": [generate_financial_asset() for _ in range(3)],
    "investment_strategies": [generate_investment_strategy() for _ in range(3)]
}

with open("mock_financial_data.json", "w") as f:
    json.dump(mock_data, f, indent=2)

print("confirm")
