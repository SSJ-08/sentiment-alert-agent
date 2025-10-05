# data_sources.py
import random
from datetime import datetime, timedelta

def fetch_twitter_alerts(keyword="YourCompany", count=5):
    """Fetch latest tweets (mock)"""
    alerts = []
    for i in range(count):
        alerts.append({
            "id": f"tw_{int(datetime.now().timestamp())}_{i}",
            "timestamp": datetime.now() - timedelta(minutes=random.randint(0, 60)),
            "source": "Twitter",
            "platform": "twitter",
            "sentiment": random.choice(["negative", "very-negative"]),
            "text": f"Tweet {i+1} about {keyword}: Customer feedback...",
            "author": f"twitter_user_{i}",
            "urgency": random.choice(["high", "medium", "low"]),
            "recommendedResponse": "Automated response based on AI analysis.",
            "metrics": {"engagement": random.randint(10, 100), "reach": random.randint(100, 2000)}
        })
    return alerts

def fetch_google_reviews(count=5):
    """Fetch Google Reviews (mock)"""
    alerts = []
    for i in range(count):
        alerts.append({
            "id": f"gr_{int(datetime.now().timestamp())}_{i}",
            "timestamp": datetime.now() - timedelta(minutes=random.randint(0, 120)),
            "source": "Google Reviews",
            "platform": "reviews",
            "sentiment": random.choice(["negative", "very-negative"]),
            "text": f"Google review {i+1}: Product/service feedback...",
            "author": f"GoogleUser_{i}",
            "urgency": random.choice(["high", "medium", "low"]),
            "recommendedResponse": "Quality team investigation recommended.",
            "metrics": {"rating": random.randint(1, 5), "helpful": random.randint(0, 20)}
        })
    return alerts

def fetch_reddit_alerts(count=5):
    """Fetch Reddit posts/comments (mock)"""
    alerts = []
    for i in range(count):
        alerts.append({
            "id": f"rd_{int(datetime.now().timestamp())}_{i}",
            "timestamp": datetime.now() - timedelta(minutes=random.randint(0, 180)),
            "source": "Reddit",
            "platform": "forum",
            "sentiment": random.choice(["negative", "very-negative"]),
            "text": f"Reddit comment {i+1}: Users discussing issues...",
            "author": f"reddit_user_{i}",
            "urgency": random.choice(["high", "medium", "low"]),
            "recommendedResponse": "Community management to provide workaround.",
            "metrics": {"upvotes": random.randint(0, 50), "comments": random.randint(0, 20)}
        })
    return alerts

def fetch_app_store_reviews(count=5):
    """Fetch App Store reviews (mock)"""
    alerts = []
    for i in range(count):
        alerts.append({
            "id": f"as_{int(datetime.now().timestamp())}_{i}",
            "timestamp": datetime.now() - timedelta(minutes=random.randint(0, 240)),
            "source": "App Store",
            "platform": "reviews",
            "sentiment": random.choice(["negative", "very-negative"]),
            "text": f"App Store review {i+1}: App issues and feedback...",
            "author": f"AppUser_{i}",
            "urgency": random.choice(["high", "medium", "low"]),
            "recommendedResponse": "Technical team to provide update patch.",
            "metrics": {"rating": random.randint(1, 5), "helpful": random.randint(0, 20)}
        })
    return alerts

def fetch_all_alerts(count_per_source=5):
    """Aggregate all alerts from different sources"""
    alerts = []
    alerts.extend(fetch_twitter_alerts(count=count_per_source))
    alerts.extend(fetch_google_reviews(count=count_per_source))
    alerts.extend(fetch_reddit_alerts(count=count_per_source))
    alerts.extend(fetch_app_store_reviews(count=count_per_source))
    
    # Sort by timestamp descending
    alerts.sort(key=lambda x: x['timestamp'], reverse=True)
    return alerts
