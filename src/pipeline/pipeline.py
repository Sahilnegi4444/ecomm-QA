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

    #1. Load Data
    logging.info("\nLoading Data")
    ingestor = DataIngestor()
    df = ingestor.load_data(limit=limit)

    #2. Preprocess
    logging.info("\nData Preprocessing")
    preprocessor = PreProcessing()
    products = preprocessor.group_products(df)
    products = preprocessor.create_combined_text(products)

    #3. Generate embeddings
    logging.info("\nCreating embeddings")
    generate_embeddings = CreateEmbeddings()
    embeddings = generate_embeddings.create_embeddings(products)

    #4. Pushing data into vector DB
    logging.info("\nPushing data into Vector Database")
    vector_db = VectorDB()
    collection = vector_db.create_collection(products, embeddings)

    #5 Test Search
    logging.info("\nTesting search")
    test_results = Retreiver()
    result = test_results.search(query="Best facewah for oily skin")

    #6. Formatted Results
    logging.info("\nFormatted results")
    output = test_results.format_results(results = result)
    print(output)

    