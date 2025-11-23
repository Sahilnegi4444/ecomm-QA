import chromadb
from src.rag_pipeline.chatbot import Chatbot
from src.retriever import Retreiver

print("\n🤖 Testing Full Chatbot\n")

# Load collection
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("products")
print(f"✅ Loaded {collection.count()} products")

# Create chatbot
print("✅ Initializing chatbot...")
chatbot = Chatbot(collection)

# Test queries
while True:
    query = input("Question: ")

    if query.lower() in ['q','quit','exit']:
        print("Thank you for using our service")
        break

    if query.strip():
    
        response, results = chatbot.chat(query, k=5)

        print(response)
        print("="*60)
        print("\n📦 Products found:")
        for i, meta in enumerate(results['metadatas'][0]):
            price = f"${meta['price']:.2f}" if meta['price'] > 0 else "N/A"
            print(f"   {i+1}. {meta['product_title']}")
            print(f"      ⭐ {meta['rating']:.1f} | 💰 {price}")
        print()
