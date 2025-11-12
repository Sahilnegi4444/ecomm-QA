import pandas as pd
from sentence_transformers import SentenceTransformer
import logging

class EmbeddingsConfig:
    pass

class CreateEmbeddings:
    def __init__(self,model = 'all-MiniLM-L6-v2'):
        logging.info("Loading embbeding model: {model}")
        self.model = SentenceTransformer(model)
        logging.info("Model loaded successfully")

        

    def create_embeddings(self, products):

        try:
            logging.info("Generating embeddings")
            embeddings = self.model.encode(
                products['combined_text'].tolist(),
                show_progress_bar=True,
                batch_size=32
            )

            logging.info("Generated embeddings with the shape: {embeddings.shape}")
            return embeddings
        
        except Exception as e:
            raise e

