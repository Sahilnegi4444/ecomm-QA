from sqlalchemy import create_engine, text
import logging
import pandas as pd

class DataIngestionConfig:
    DATABASE_URL = 'mysql+pymysql://root:Lihasigen%404444@localhost:3306/amazon_data_db'
    

class DataIngestor:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        self.engine = create_engine(self.config.DATABASE_URL)
        
    def load_data(self,limit = None):
        try:
            with self.ingestion_config.engine.connect() as conn:
                logging.info("Loading data from database")
                
                # Check total rows
                query = conn.execute(text("SELECT * FROM amazon_dataframe"))
                df = pd.read_sql(query, self.engine)

                logging.info(f"Loaded: {len(df):,} rows")

                return df
            
        except Exception as e:
            raise e

if __name__=='__main__':
    ingestor = DataIngestor()
    df = ingestor.load_data(limit=10000)
    print(df.head())

