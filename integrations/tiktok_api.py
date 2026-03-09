# ==========================================================
# MTSE Marketing Engine - TikTok API Integration
# ==========================================================

import random
import pandas as pd
from datetime import datetime, timedelta

class TikTokAdsAPI:
    """
    Simulated TikTok Ads API connector.
    In production, this would use the official TikTok Events API / Graph API.
    """
    def __init__(self, access_token=None):
        self.access_token = access_token
        self.is_connected = access_token is not None

    def test_connection(self):
        """Simulate a connection test"""
        return {"status": "success", "message": "Connected to TikTok Business Account"}

    def fetch_campaign_performance(self, days=30):
        """Generate simulated data matching TikTok's actual metrics structure"""
        if not self.is_connected:
            raise ValueError("Not connected to TikTok API")
            
        data = []
        today = datetime.now()
        
        campaigns = ["UGC Launch", "Spark Ads Promo", "Creator Collab 1", "Trend Challenge"]
        
        for i in range(days):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            for camp in campaigns:
                spend = random.uniform(50, 500)
                views = int(spend * random.uniform(200, 800))
                clicks = int(views * random.uniform(0.01, 0.05))
                conversions = int(clicks * random.uniform(0.02, 0.1))
                cpa = spend / max(conversions, 1)
                
                data.append({
                    "date": date,
                    "campaign_name": camp,
                    "platform": "TikTok",
                    "spend": round(spend, 2),
                    "impressions": views,  # TikTok calls them views usually
                    "clicks": clicks,
                    "conversions": conversions,
                    "cpa": round(cpa, 2)
                })
                
        return pd.DataFrame(data)
