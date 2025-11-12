import pandas as pd
import logging

class PreprocessConfig:
    pass

class PreProcessing:
    def __init__(self):
        pass

    def group_products(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            products = df.groupby('parent_asin').agg(
                {
                    'product_title': 'first',
                    'review_headline': 'first',
                    'category': 'first',
                    'price': 'mean',
                    'rating': 'mean',
                    'review': lambda x: ' '.join(x.astype(str)[:10]),
                    'rating_number':'first',
                    'features': 'first',
                    'description': 'first',
                    'details': 'first'
                }
            ).reset_index()

            return products
        
        except Exception as e:
            raise e
        
    def create_combined_text(self, row): 
        
        parts = []

        parts.append(f"Product title: {row['product_title']}")

        if pd.notna(row['category']):
            parts.append(f"Category: {row['category']}")

        if pd.notna(row['features']):
            parts.append(f"Features: {row['features'][:400]}")

        if pd.notna(row['rating']):
            parts.append(f"Rating: {row['rating']}/5")

        if pd.notna(row['review']):
            parts.append(f"Reviews: {row['review'][:600]}")

        if pd.notna(row['description']):
            parts.append(f"Description: {row['description'][:400]}")

        if pd.notna(row['price']):
            parts.append(f"Price: {row['Price']:.2f}") 

        return " | ".join(parts)    

    def prepare_for_embeddings(self, products: pd.Dataframe) -> pd.DataFrame:
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
         





            


        
