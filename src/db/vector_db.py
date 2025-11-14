import os
os.environ['ANONYMIZED_TELEMETRY'] = 'False'        # remove telementary services

import chromadb
import pandas as pd
from src.embeddings.embeddings import CreateEmbeddings
from src.logger import logging


class VectorDB:
    def __init__(self):
        self.client = chromadb.Client()
        logging.info("Chroma DB initialized")


    def create_collection(self, products:pd.DataFrame, embeddings, collection_name = 'products'):
        """
        Create Vector Db from products and embeddings

        Args: 
            products: dataframe with product data           
            embeddings: numpy array of embeddings
            collection_name: name of the collection
        """

        try:
            try:
                # Delete collection if already exists
                self.client.delete_collection(name=collection_name)
            except :
                pass
            
            # Create collection
            collection = self.client.create_collection(name=collection_name)
            logging.info("Created new collection")

            metadata_df = products[['product_title','category','rating','price']].copy()

            metadata_df['product_title'] = metadata_df['product_title'].fillna('')
            metadata_df['category'] = metadata_df['category'].fillna('')
            metadata_df['rating'] = metadata_df['rating'].fillna(0.0)
            metadata_df['price'] = metadata_df['price'].fillna(0.0)

            metadatas = metadata_df.to_dict('records')

            # ADD to collection
            logging.info(f"Adding {len(products)} products to Vector DB")
            collection.add(
                embeddings=embeddings.tolist(),
                documents=products['combined_text'].tolist(), 
                ids= products['parent_asin'].astype(str).tolist(),
                metadatas=metadatas
            )
            logging.info(f"Successfully added {collection.count()} products into VectorDB")
            return collection
        

        except Exception as e:
            raise e
        
if __name__ == "__main__":
    from src.ingest import DataIngestor
    from src.processing.preprocessing import PreProcessing
    from src.db.vector_db import VectorDB

    ingestor = DataIngestor()
    df = ingestor.load_data(limit=1000)

    preprocessor = PreProcessing()
    products = preprocessor.group_products(df)
    products = preprocessor.prepare_for_embeddings(products)

    #generate embeddings
    from src.embeddings.embeddings import CreateEmbeddings

    generate_embeddings = CreateEmbeddings()
    embeddings = generate_embeddings.create_embeddings(products = products)

    vector_db = VectorDB()
    collection = vector_db.create_collection(products, embeddings)

    print("Created collection of products into Vector DB")



    
        
    
