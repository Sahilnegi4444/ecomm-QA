#Orchestrate layer

from src.retriever import Retriever
from src.llm.chat import LLMChat

class Chatbot:
    def __init__(self, collection):
        self.retriever = Retriever(collection)
        self.llm = LLMChat(use_ollama=True)

        self.convo_memory = []          #conversation memory for chatbot
        self.last_products = []         #last products
        self.last_results = None        #store full results

    def is_followup(self, user_query):

        """Detects if question is a follow-up"""
        followup_keywords = [
            'the first', 'the second', 'the third','the fourth', 'the fifth' 'the last one',
            ' first', ' second', ' third', ' fourth', ' fifth',
            'that one', 'this one', 'it', 'its', 'them',
            'compare', 'difference', 'which is better',
            'tell me more', 'more about', 'details',
            'what about', 'how about', 
        ]
        user_query =  user_query.lower() 
        return any(keyword in user_query for keyword in followup_keywords)      #returns True if followup question

    def handle_followup(self, user_query):

        """Handle follow-up question with memory"""
        product_context = self._format_products_context()
                
        convo_context = "\n".join(
            f"User: {turn['user']}\nAssistant: {turn['bot']}"
            for turn in self.convo_memory[-5:]                                  #checks the last 5 conversation in the memory
        )

        prompt = f""" 
        You are a helpful shopping assistant.
        Continue the conversation using the past context and product list.

        Previous products
        {product_context}

        Previous conversation
        {convo_context}

        New Question
        {user_query}

        If user says "the second one", identify the correct product from the list.

        """
        response = self.llm.generate(prompt)
        print(response)

        #Add to memory
        self._store_memory(user_query,response)

        return response, self.last_results

    def chat(self, user_query, k=5):
        """
        Complte RAG Pipeline with conversation memory
        """
        if self.last_products and self.is_followup(user_query):
            return self.handle_followup(user_query)
        
        #Reset product list for new query
        self.last_products = []
        
        # Step 1: Search for products
        results = self.retriever.search(user_query, k=k)
        self.last_results = results

        #Step1: Store products in memory
        for i, meta in enumerate(results['metadatas'][0]):
            self.last_products.append({
                'index': i + 1,
                'title': meta['product_title'],
                'category': meta['category'],
                'rating': meta['rating'],
                'price': meta['price'],
            })

        #Step2: Format context for LLM 
        product_context = self._format_products_context()

        # Step 3: Create prompt for LLM
        prompt = f"""You are a helpful e-commerce shopping assistant. Answer the customer's question using the product information provided.

        Customer Question: "{user_query}"

        Available Products (numbered):
        {product_context}

        Recommend the best items using their numbers (1, 2, 3...) 
        and explain why you picked them. Be specific about features, ratings, and prices."""
        
        
        #Step4: Generate response 
        response = self.llm.generate(prompt)
    
        # Step5: Add to conversation memory
        self.convo_memory.append({
            "user" : user_query,
            "bot" : response,
            "products" : self.last_products.copy()
        })

        return response, results
    
    def _format_products_context(self):

        """Format last products into readable context"""
        if not self.last_products:
            return "No products available"
        
        lines = []
        for product in self.last_products:
            price = f"${product['price']:.2f}" if product['price'] > 0 else "N/A"
            lines.append(
                f"{product['index']}. {product['title']}\n"
                f"   Category: {product['category']}\n"
                f"   Rating: {product['rating']}/5\n"
                f"   Price: {price}\n"
            )
        
        return "\n".join(lines)
    
    def _store_memory(self, user, bot):
        self.convo_memory.append({
            "user": user,
            "bot": bot,
            "products": self.last_products.copy()
        })

    def reset_memory(self):
        """Clear all conversation memory (fresh start)"""
        self.convo_memory = []
        self.last_products = []
        self.last_results = None
        print("🔄 Memory cleared - starting fresh conversation")


