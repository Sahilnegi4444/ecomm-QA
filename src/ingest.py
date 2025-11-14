from sqlalchemy import create_engine, text
from src.logger import logging
import pandas as pd

class DataIngestionConfig:
    DATABASE_URL = 'mysql+pymysql://root:Lihasigen%404444@localhost:3306/amazon_data_db'
    

class DataIngestor:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        self.engine = create_engine(self.ingestion_config.DATABASE_URL)
        
    def load_data(self, limit = None):
        try:
            with self.engine.connect() as conn:
                logging.info("Loading data from database")
                
                # Check the df
                query = text("SELECT * FROM amazon_dataframe LIMIT :limit")
                

                df = pd.read_sql(query, conn, params={"limit":limit})

                logging.info(f"Loaded: {len(df):,} rows")

                return df
            
        except Exception as e:
            raise e

if __name__=='__main__':
    ingestor = DataIngestor()
    df = ingestor.load_data(limit=10000)
    print(df.head(10))

