import chromadb
from src.rag_pipeline.chatbot import Chatbot


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
        if chatbot.is_followup(query):
            response, results = chatbot.chat(query)
            
        
        else:
            response, results = chatbot.chat(query)

            print(response)
            print("="*60)
            print("\n📦 Products found:")
            for p in chatbot.last_products:
                price = f"${p['price']:.2f}" if p['price'] > 0 else "N/A"
                print(f"   {p['index']}. {p['title']}")
                print(f"      ⭐ {p['rating']:.1f} | 💰 {price}")
    
    
        
