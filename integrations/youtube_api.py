# ==========================================================
# MTSE Marketing Engine - YouTube API Integration
# ==========================================================

import random
import pandas as pd
from datetime import datetime, timedelta

class YouTubeAnalyticsAPI:
    """
    Simulated YouTube Data API v3 connector.
    """
    def __init__(self, api_key=None, channel_id=None):
        self.api_key = api_key
        self.channel_id = channel_id
        self.is_connected = api_key is not None

    def get_channel_stats(self):
        """Return overall channel metrics"""
        return {
            "subscriber_count": random.randint(10000, 500000),
            "total_views": random.randint(1000000, 50000000),
            "video_count": random.randint(50, 500)
        }

    def fetch_traffic_sources(self):
        """Return traffic source percentage"""
        return [
            {"source": "YouTube Search", "percentage": 45},
            {"source": "Suggested Videos", "percentage": 25},
            {"source": "External (Google)", "percentage": 15},
            {"source": "Direct/Unknown", "percentage": 10},
            {"source": "Other YouTube Features", "percentage": 5}
        ]

    def fetch_video_metrics(self, days=30):
        """Generate simulated data for top videos over last 30 days"""
        if not self.is_connected:
            raise ValueError("YouTube API not connected")
            
        data = []
        today = datetime.now()
        
        for i in range(days):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            views = random.randint(500, 5000)
            watch_time_hours = round(views * random.uniform(0.05, 0.15), 2)
            ctr = round(random.uniform(2.5, 9.8), 2)
            avg_view_duration = f"0{random.randint(1,5)}:{random.randint(10,59)}"
            
            data.append({
                "date": date,
                "views": views,
                "watch_time_hours": watch_time_hours,
                "impressions_ctr": ctr,
                "avg_view_duration": avg_view_duration,
                "estimated_revenue": round(views * random.uniform(0.001, 0.005), 2)
            })
            
        return pd.DataFrame(data)
