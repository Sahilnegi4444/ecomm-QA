#Orchestrate layer

from src.retriever import Retreiver
from src.llm.chat import LLMchat

class Chatbot:
    def __init__(self, collection):
        self.retreiver = Retreiver(collection)
        self.llm = LLMchat(use_ollama=True)

    def chat(self, user_query, k=5):
        """
        Complte RAG Pipeline
        """

        # Step 1: Retrieve relevant products
        results = self.retreiver.search(user_query, k=k)

        #Step2: Format context for LLM 
        context = self.retreiver.format_results(results)

        # Step 3: Create prompt for LLM
        prompt = f"""You are a helpful e-commerce shopping assistant. Answer the customer's question using the product information provided.

        Customer Question: "{user_query}"

        Available Products:
        {context}

        Instructions:
        - Answer the question directly and conversationally
        - Recommend specific products from the list
        - Explain WHY they're good matches
        - Mention ratings and prices
        - If asking about features, explain what the products offer
        - If comparing, highlight differences


        Answer: """
        
        
        #Step4: Generate response with LLM
        response = self.llm.generate(prompt)

        # Step5 : Retun response 
        return response, results

if __name__ == "__main__":
    print("Chatbot is working fine")