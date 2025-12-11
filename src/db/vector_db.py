import os
import math
os.environ['ANONYMIZED_TELEMETRY'] = 'False'

import chromadb
import pandas as pd
from src.logger import logging


BATCH_SIZE = 25000  # safe limit for embedding + Chroma

class VectorDB:
    def __init__(self, persist_directory="./chroma_db"):

        os.makedirs(persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_directory)
        logging.info(f"Chroma DB initialized at {persist_directory}")


    def create_collection(self, products: pd.DataFrame, embeddings, collection_name="products"):
        """
        Create Vector DB in batches

        Args: 
            products: DataFrame with product data
            embeddings: 2D numpy array of embeddings
            collection_name: name of the collection
        """

        try:
            # Remove old collection if exists
            try:
                self.client.delete_collection(name=collection_name)
            except:
                pass

            # Create a fresh persistent collection
            collection = self.client.create_collection(name=collection_name)
            logging.info("Created new collection")

            # Prepare metadata
            metadata_df = products[['product_title', 'category', 'rating', 'price']].copy()
            metadata_df.fillna({'product_title': '',
                                'category': '',
                                'rating': 0.0,
                                'price': 0.0},
                                inplace=True)

            metadatas = metadata_df.to_dict('records')
            ids = products['parent_asin'].astype(str).tolist()
            documents = products['combined_text'].astype(str).tolist()

            total = len(products)
            num_batches = math.ceil(total / BATCH_SIZE)

            logging.info(f"Adding {total} products in {num_batches} batches")

            # Batch insertion
            for i in range(0, total, BATCH_SIZE):
                end = i + BATCH_SIZE
                logging.info(f"Processing batch {i//BATCH_SIZE + 1}/{num_batches}: rows {i} → {end}")

                collection.add(
                    embeddings=embeddings[i:end].tolist(),
                    documents=documents[i:end],
                    ids=ids[i:end],
                    metadatas=metadatas[i:end]
                )

            logging.info(f"✓ Completed! Total stored: {collection.count()} products")
            return collection
        
        except Exception as e:
            logging.error(f"VectorDB ingestion failed: {e}")
            raise e
        
# if __name__ == "__main__":
#     from src.ingest import DataIngestor
#     from src.processing.preprocessing import PreProcessing
#     from src.db.vector_db import VectorDB

#     ingestor = DataIngestor()
#     df = ingestor.load_data(limit=150000)

#     preprocessor = PreProcessing()
#     products = preprocessor.group_products(df)
#     products = preprocessor.prepare_for_embeddings(products)

#     #generate embeddings
#     from src.embeddings.embeddings import CreateEmbeddings

#     generate_embeddings = CreateEmbeddings()
#     embeddings = generate_embeddings.create_embeddings(products = products)

#     vector_db = VectorDB()
#     collection = vector_db.create_collection(products, embeddings)

#     print("Created collection of products into Vector DB")



    
        
    
