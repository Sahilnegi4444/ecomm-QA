import pandas as pd
from src.logger import logging

class PreprocessConfig:
    pass

class PreProcessing:
    def __init__(self):
        pass

    def group_products(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info("Grouping reviews by product")
            products = df.groupby('parent_asin').agg(
                {
                    'product_title': 'first',
                    'review_headline': 'first',
                    'category': 'first',
                    'price': 'mean',
                    'rating': 'mean',
                    'reviews': lambda x: ' '.join(x.astype(str)[:10]),
                    'rating_number':'first',
                    'features': 'first',
                    'description': 'first',
                    'details': 'first'
                }
            ).reset_index()

            logging.info(f"Created {len(products)} unique products")

            return products
        
        except Exception as e:
            raise e
        
    def create_combined_text(self, row): 
        
        parts = []

        parts.append(f"Product title: {row['product_title']}")

        if pd.notna(row['category']):
            parts.append(f"Category: {row['category']}")

        if pd.notna(row['features']):
            parts.append(f"Features: {str(row['features'][:400])}")

        if pd.notna(row['rating']):
            parts.append(f"Rating: {row['rating']}/5")

        if pd.notna(row['reviews']):
            parts.append(f"Reviews: {str(row['reviews'][:600])}")

        if pd.notna(row['description']):
            parts.append(f"Description: {str(row['description'][:400])}")

        if pd.notna(row['price']):
            parts.append(f"Price: ${row['price']:.2f}") 

        return " | ".join(parts)    

    def prepare_for_embeddings(self, products: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info("Creating text for embeddings")      
            products['combined_text'] = products.apply(
                self.create_combined_text,
                axis = 1
            )
            logging.info("Combined text created")
            return products
        
        except Exception as e:
            raise e
        
if __name__ == "__main__":
    from src.ingest import DataIngestor
    from src.processing.preprocessing import PreProcessing

    ingestor = DataIngestor()
    df = ingestor.load_data(limit=1000)

    preprocessor = PreProcessing()
    products = preprocessor.group_products(df)
    products = preprocessor.prepare_for_embeddings(products)

    #generate embeddings
    from src.embeddings.embeddings import CreateEmbeddings

    generate_embeddings = CreateEmbeddings()
    embeddings = generate_embeddings.create_embeddings(products = products)

    print(f"Generated embeddings shape {embeddings.shape}")