from src.ingest import DataIngestor
from src.processing.preprocessing import PreProcessing
from src.embeddings.embeddings import CreateEmbeddings
from src.db.vector_db import VectorDB
from src.retriever import Retreiver

from src.logger import logging

def run_pipeline(limit = None):
    """
    RUN COMPLETE DATA PIPELINE
    """
    try:
        #1. Load Data
        logging.info("\nLoading Data")
        ingestor = DataIngestor()
        df = ingestor.load_data(limit=limit)

        #2. Preprocess
        logging.info("\nData Preprocessing")
        preprocessor = PreProcessing()
        products = preprocessor.group_products(df)
        products = preprocessor.prepare_for_embeddings(products)

        #3. Generate embeddings
        logging.info("\nCreating embeddings")
        generate_embeddings = CreateEmbeddings()
        embeddings = generate_embeddings.create_embeddings(products)

        #4. Pushing data into vector DB
        logging.info("\nPushing data into Vector Database")
        vector_db = VectorDB()
        collection = vector_db.create_collection(products, embeddings)

        # #5 Test Search
        # logging.info("\nTesting search")
        # test_results = Retreiver()                  #it will be used in LLM.py to retrive the data
        # result = test_results.search(query="Best facewash for oily skin")

        # #6. Formatted Results
        # logging.info("\nFormatted results")
        # output = test_results.format_results(results = result)

        logging.info("pipeline is working")
        return products, embeddings, collection
    
    except Exception as e:
        logging.error("Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    products, embeddings, collection = run_pipeline(limit=10000)

    