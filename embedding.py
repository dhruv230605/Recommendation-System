import json
import os
from sentence_transformers import SentenceTransformer
from chromadb import Client
from chromadb.config import Settings
import chromadb.errors

# 1) CONFIGURATION: adjust paths or parameters here if needed
JSON_PATH = "mock_financial_data.json"       # Path to your uploaded JSON file
COLLECTION_NAME = "financial_data"           # ChromaDB collection name
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"    # Sentence-Transformers model

# 2) Load JSON data
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# 3) Initialize embedding model
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# 4) Initialize ChromaDB client & create (or get) a collection
chroma_client = Client(Settings(
    persist_directory="./chroma_db",
    is_persistent=True  # Explicitly enable persistence
))

print(f"Using persistence directory: {os.path.abspath('./chroma_db')}")

try:
    collection = chroma_client.get_collection(name=COLLECTION_NAME)
    print(f"Found existing collection: {COLLECTION_NAME}")
except chromadb.errors.NotFoundError:
    collection = chroma_client.create_collection(name=COLLECTION_NAME)
    print(f"Created new collection: {COLLECTION_NAME}")

# Verify collection exists
print(f"Collection count: {collection.count()}")

# 5) Helper: build a text representation for a record
def record_to_text(record: dict, record_type: str) -> str:
    """
    Given a dictionary 'record' and its type (e.g., "transaction"),
    return a string that concatenates key fields for meaningful embedding.
    """
    if record_type == "transaction":
        fields = [
            f"Transaction ID: {record.get('transaction_id', '')}",
            f"Category: {record.get('category', '')}",
            f"Merchant: {record.get('merchant_name', '')}",
            f"Amount: {record.get('amount', '')} {record.get('currency', '')}",
            f"Tags: {', '.join(record.get('tags', []))}",
            f"User ID: {record.get('user_id', '')}",
        ]
        # Optionally include a short breakdown of metadata.itemized_breakdown
        items = record.get("metadata", {}).get("itemized_breakdown", [])
        if items:
            item_strs = [f"{itm['product']} (qty {itm['quantity']}, ₹{itm['price']})" for itm in items]
            fields.append(f"Items: {', '.join(item_strs)}")
        return " • ".join(fields)

    elif record_type == "offer":
        fields = [
            f"Offer ID: {record.get('offer_id', '')}",
            f"Name: {record.get('name', '')}",
            f"Description: {record.get('description', '')}",
            f"Type: {record.get('type', '')}",
            f"Categories: {', '.join(record.get('applicable_categories', []))}",
            f"Min Amount: {record.get('minimum_transaction_amount', '')}",
            f"Discount: {record.get('discount_value', {}).get('value', '')}{record.get('discount_value', {}).get('type', '')}",
        ]
        return " • ".join(fields)

    elif record_type == "financial_asset":
        fields = [
            f"Asset ID: {record.get('asset_id', '')}",
            f"Name: {record.get('name', '')}",
            f"Type: {record.get('type', '')}",
            f"Issuer: {record.get('issuer', '')}",
            f"Risk Rating: {record.get('risk_rating', '')}",
            f"Expected Return: {record.get('expected_return', '')}%",
        ]
        return " • ".join(fields)

    elif record_type == "investment_strategy":
        fields = [
            f"Strategy ID: {record.get('strategy_id', '')}",
            f"Name: {record.get('name', '')}",
            f"Risk Profile: {record.get('risk_profile', '')}",
            f"Time Horizon: {record.get('time_horizon', '')}",
            f"Allocation: {', '.join([f'{k}:{v}%' for k,v in record.get('allocation_blueprint', {}).items()])}",
        ]
        return " • ".join(fields)

    else:
        # Fallback: full JSON dump
        return json.dumps(record)

# 6) Iterate over each top‐level section and embed+upload
# We will use a single Chroma collection, but prefix IDs with their type
all_ids = []
all_texts = []
all_embeddings = []
all_metadatas = []

# 6.1 Transactions
for tx in data.get("transactions", []):
    rec_id = "txn_" + tx["transaction_id"]
    text = record_to_text(tx, "transaction")
    embedding = model.encode(text).tolist()

    metadata = {
        "record_type": "transaction",
        "user_id": tx.get("user_id", ""),
        "category": tx.get("category", ""),
        "currency": tx.get("currency", ""),
    }

    all_ids.append(rec_id)
    all_texts.append(text)
    all_embeddings.append(embedding)
    all_metadatas.append(metadata)

# 6.2 Offers
for off in data.get("offers", []):
    rec_id = "off_" + off["offer_id"]
    text = record_to_text(off, "offer")
    embedding = model.encode(text).tolist()

    metadata = {
        "record_type": "offer",
        "type": off.get("type", ""),
        "min_amount": off.get("minimum_transaction_amount", ""),
    }

    all_ids.append(rec_id)
    all_texts.append(text)
    all_embeddings.append(embedding)
    all_metadatas.append(metadata)

# 6.3 Financial Assets
for asset in data.get("financial_assets", []):
    rec_id = "asset_" + asset["asset_id"]
    text = record_to_text(asset, "financial_asset")
    embedding = model.encode(text).tolist()

    metadata = {
        "record_type": "financial_asset",
        "type": asset.get("type", ""),
        "risk_rating": asset.get("risk_rating", ""),
    }

    all_ids.append(rec_id)
    all_texts.append(text)
    all_embeddings.append(embedding)
    all_metadatas.append(metadata)

# 6.4 Investment Strategies
for strat in data.get("investment_strategies", []):
    rec_id = "strat_" + strat["strategy_id"]
    text = record_to_text(strat, "investment_strategy")
    embedding = model.encode(text).tolist()

    metadata = {
        "record_type": "investment_strategy",
        "risk_profile": strat.get("risk_profile", ""),
        "time_horizon": strat.get("time_horizon", ""),
    }

    all_ids.append(rec_id)
    all_texts.append(text)
    all_embeddings.append(embedding)
    all_metadatas.append(metadata)

# 7) Add all documents to ChromaDB
collection.add(
    ids=all_ids,
    documents=all_texts,
    embeddings=all_embeddings,
    metadatas=all_metadatas
)

print(f"Added {len(all_ids)} records to ChromaDB collection '{COLLECTION_NAME}'.")