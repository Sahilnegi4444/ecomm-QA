import chromadb
import sys
import os

print("\n🔍 VERIFYING COLLECTION")
print("="*60)

# Check if chroma_db folder exists
print("\n[1] Checking if chroma_db folder exists...")
if os.path.exists("./chroma_db"):
    print(f"   ✅ Found: {os.path.abspath('./chroma_db')}")
    print(f"   Contents: {os.listdir('./chroma_db')}")
else:
    print(f"   ❌ Folder not found at: {os.path.abspath('./chroma_db')}")
    print("\n   You need to run the pipeline first:")
    print("   python -m src.test.test_chatbot")
    sys.exit(1)

# Try to connect to ChromaDB
print("\n[2] Connecting to ChromaDB...")
try:
    client = chromadb.PersistentClient(path="./chroma_db")
    print("   ✅ Connected to ChromaDB")
except Exception as e:
    print(f"   ❌ Failed to connect: {e}")
    sys.exit(1)

# Try to get collection
print("\n[3] Looking for 'products' collection...")
try:
    collection = client.get_collection(name="products")
    print(f"   ✅ Collection found!")
    print(f"   📦 Products: {collection.count()}")
except Exception as e:
    print(f"   ❌ Collection not found: {e}")
    
    # List available collections
    try:
        collections = client.list_collections()
        print(f"\n   Available collections: {[c.name for c in collections]}")
    except:
        print(f"   No collections exist yet")
    
    sys.exit(1)

# Test a search
print("\n[4] Testing search functionality...")
try:
    results = collection.query(
        query_texts=["shampoo"],
        n_results=3
    )
    
    print(f"   ✅ Search works!")
    print(f"\n   📦 Sample products:")
    for i, meta in enumerate(results['metadatas'][0]):
        print(f"      {i+1}. {meta.get('product_title', 'No title')}")
    
except Exception as e:
    print(f"   ❌ Search failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("✅ VERIFICATION COMPLETE")
print("="*60)