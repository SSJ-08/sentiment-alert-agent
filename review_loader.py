import pandas as pd
import random
from datetime import datetime, timedelta
flipkart_df = pd.read_csv("data/FlipkartReviews.csv")
flipkart_df = flipkart_df.rename(columns={
    'Review': 'text',
    'Summary': 'author',
    'Rate': 'rating'
})
flipkart_df['timestamp'] = [datetime.now() - timedelta(days=random.randint(0,30), hours=random.randint(0,23)) 
                            for _ in range(len(flipkart_df))]
amazon_df = pd.read_csv("data/AmazonReviews.csv")
amazon_df = amazon_df.rename(columns={
    'Text': 'text',
    'ProfileName': 'author',
    'Score': 'rating',
    'Time': 'timestamp'
})
amazon_df['timestamp'] = pd.to_datetime(amazon_df['timestamp'], unit='s')  
df = pd.concat([flipkart_df, amazon_df], ignore_index=True)
def get_new_alerts(existing_ids=set(), n=5):
    """Simulate fetching new alerts from combined dataset."""
    new_reviews = df[~df.index.isin(existing_ids)].sample(n=min(n, len(df)))
    alerts = []
    for idx, row in new_reviews.iterrows():
        alerts.append({
            "id": str(idx),
            "text": row['text'],
            "author": row['author'],
            "platform": random.choice(['flipkart', 'amazon']),
            "sentiment": random.choice(['negative', 'very-negative','positive','neutral']),
            "urgency": random.choice(['high', 'medium','low']),
            "recommendedResponse": "Automated recommended response",
            "metrics": {"rating": row.get('rating', 0)}
        })
    return alerts
