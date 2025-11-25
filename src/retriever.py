from src.logger import logging
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, collection, model_name = 'all-MiniLM-L6-v2'):
         self.collection = collection
         self.model = SentenceTransformer(model_name)

    def search(self,query, k=5):
            """
            Search for products matching query
            """
            try:
                query_embedding = self.model.encode([query])

                results = self.collection.query(
                    query_embeddings=query_embedding.tolist(),
                    n_results = k
                )
                
                return results
            
            except Exception as e:
                raise e
    
    def format_results(self, results):
        """
        Format results for LLM
        """
        context = "Relevent products:\n"

        for i, meta in enumerate(results['metadatas'][0]):
              context += f"{i+1}. Product: {meta['product_title']}\n"
              context += f"Category: {meta['category']}\n"
              context += f"Ratings :{meta['rating']}\n"
              context += f"Price :{meta['price']}\n"

        return context