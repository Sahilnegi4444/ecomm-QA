import chromadb
import pandas as pd
from src.embeddings.embeddings import CreateEmbeddings
import logging

class VectorDBconfig:
    def __init__(self):
        pass

class VectorDB:
    def __init__(self):
        self.client = chromadb.Client()
        logging.info("Chroma DB initialized")


    def create_collection(self, products:pd.DataFrame,embeddings, collection_name = 'products'):
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
                logging.info("Deleted existing collection: {collection_name}")
            except :
                pass
            
            # Create collection
            collection = self.client.create_collection(name=collection_name)
            logging.info("Created new collection")

            metadata_df = products[['product_title','category','rating','price']]

            metadata_df['product_title'] = metadata_df['product_title'].fillna('')
            metadata_df['category'] = metadata_df['category'].fillna('')
            metadata_df['rating'] = metadata_df['rating'].fillna(0.0)
            metadata_df['price'] = metadata_df['price'].fillna(metadata_df.groupby('category')['price'].transform('median'))

            metadatas = metadata_df.to_dict('records')

            # ADD to collection
            logging.info("Adding products to Vector DB")
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
        
    def search(self, collection_name, query_embedding, k=5):
        """
        Search for similar products
        """
        try:
            collection = self.client.get_collection(name=collection_name)
            results = collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results = k
            )
            return results
        
        except Exception as e:
            raise e
