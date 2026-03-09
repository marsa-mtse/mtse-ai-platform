# ==========================================================
# MTSE Marketing Engine - Instagram API Integration
# ==========================================================

import random
import pandas as pd
from datetime import datetime, timedelta

class InstagramGraphAPI:
    """
    Simulated Instagram Graph API connector.
    Fetches both organic and paid insights.
    """
    def __init__(self, access_token=None, account_id=None):
        self.access_token = access_token
        self.account_id = account_id
        self.is_connected = access_token is not None

    def authenticate(self):
        """Simulate OAuth authentication"""
        return {"status": "success", "username": "@mtse_official"}

    def get_audience_demographics(self):
        """Return fake demographic data"""
        return {
            "age_gender": {"18-24.F": 15, "18-24.M": 12, "25-34.F": 35, "25-34.M": 28},
            "cities": {"Cairo": 45, "Riyadh": 20, "Dubai": 15, "Alexandria": 10}
        }

    def fetch_reel_performance(self, limit=10):
        """Simulate Reel metrics which are crucial for IG right now"""
        if not self.is_connected:
            raise ValueError("Instagram account not connected")
            
        data = []
        for i in range(limit):
            plays = random.randint(5000, 100000)
            likes = int(plays * random.uniform(0.05, 0.15))
            comments = int(likes * random.uniform(0.01, 0.08))
            shares = int(likes * random.uniform(0.1, 0.3))
            saves = int(likes * random.uniform(0.1, 0.4))
            
            data.append({
                "reel_id": f"REEL_{i+1000}",
                "posted_at": (datetime.now() - timedelta(days=i*2)).strftime("%Y-%m-%d"),
                "plays": plays,
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "saves": saves,
                "engagement_rate": round(((likes+comments+shares+saves)/plays)*100, 2)
            })
            
        return pd.DataFrame(data)
