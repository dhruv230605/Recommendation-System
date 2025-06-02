from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os

# Initialize the client and get the collection
chroma_client = Client(Settings(
    persist_directory="./chroma_db",
    is_persistent=True  # Explicitly enable persistence
))

print(f"Using persistence directory: {os.path.abspath('./chroma_db')}")

try:
    collection = chroma_client.get_collection(name="financial_data")
    print(f"Successfully retrieved collection: financial_data")
    print(f"Collection count: {collection.count()}")
except Exception as e:
    print(f"Error accessing collection: {str(e)}")
    raise

# Initialize the same embedding model used for creating embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

def query_by_text(query_text, n_results=5):
    """Query the collection using text and return similar items"""
    # Convert query text to embedding
    query_embedding = model.encode(query_text).tolist()
    
    # Search the collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    return results

def query_by_metadata(metadata_filter, n_results=5):
    """Query the collection using metadata filters"""
    results = collection.query(
        where=metadata_filter,
        n_results=n_results
    )
    return results

# Example 1: Search for similar transactions
print("\n=== Searching for transactions similar to 'groceries' ===")
results = query_by_text("groceries")
for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
    print(f"\nResult {i+1}:")
    print(f"Document: {doc}")
    print(f"Metadata: {metadata}")

# Example 2: Search by metadata
print("\n=== Searching for high-risk financial assets ===")
results = query_by_metadata(
    {"record_type": "financial_asset", "risk_rating": "high"}
)
for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
    print(f"\nResult {i+1}:")
    print(f"Document: {doc}")
    print(f"Metadata: {metadata}")

# Example 3: Get all records of a specific type
print("\n=== Getting all offers ===")
results = query_by_metadata(
    {"record_type": "offer"}
)
for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
    print(f"\nResult {i+1}:")
    print(f"Document: {doc}")
    print(f"Metadata: {metadata}") 