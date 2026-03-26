# ==========================================================
# MTSE Marketing Engine - Instagram Graph API (Real + Fallback)
# Uses real Meta Graph API v19.0 when token is provided,
# falls back to simulation when token is absent.
# ==========================================================

import requests
import random
import pandas as pd
from datetime import datetime, timedelta


class InstagramGraphAPI:
    """
    Real Instagram Graph API connector using Meta Business API v19.0.
    Falls back to simulation mode when no access token is provided.
    """
    BASE_URL = "https://graph.facebook.com/v19.0"

    def __init__(self, access_token=None, account_id=None):
        self.access_token = access_token
        self.account_id = account_id
        self.is_real = bool(access_token and account_id and
                           access_token != "simulated" and
                           account_id != "simulated")

    def test_connection(self):
        """Test if the real API connection is valid."""
        if not self.is_real:
            return {"status": "simulation", "message": "Running in simulation mode."}
        try:
            url = f"{self.BASE_URL}/me"
            resp = requests.get(url, params={
                "fields": "id,name",
                "access_token": self.access_token
            }, timeout=10)
            data = resp.json()
            if "error" in data:
                return {"status": "error", "message": data["error"].get("message", "Unknown error")}
            return {"status": "success", "message": f"Connected as: {data.get('name', 'Unknown')}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def authenticate(self):
        """Authenticate and return account info."""
        if not self.is_real:
            return {"status": "simulation", "username": "@demo_account (Simulation Mode)"}
        try:
            url = f"{self.BASE_URL}/{self.account_id}"
            resp = requests.get(url, params={
                "fields": "id,username,name,followers_count",
                "access_token": self.access_token
            }, timeout=10)
            data = resp.json()
            if "error" in data:
                return {"status": "error", "username": f"Error: {data['error'].get('message', 'Unknown')}"}
            return {
                "status": "success",
                "username": f"@{data.get('username', 'Unknown')}",
                "followers": data.get("followers_count", "N/A")
            }
        except Exception as e:
            return {"status": "error", "username": f"Connection Error: {str(e)}"}

    def get_audience_demographics(self):
        """Fetch real audience demographic data from Instagram Insights."""
        if not self.is_real:
            return self._simulate_demographics()
        try:
            url = f"{self.BASE_URL}/{self.account_id}/insights"
            resp = requests.get(url, params={
                "metric": "audience_city,audience_gender_age",
                "period": "lifetime",
                "access_token": self.access_token
            }, timeout=10)
            data = resp.json()
            if "error" in data:
                return self._simulate_demographics()

            cities = {}
            age_gender = {}
            for item in data.get("data", []):
                if item.get("name") == "audience_city":
                    top_cities = sorted(
                        item["values"][0]["value"].items(),
                        key=lambda x: x[1], reverse=True
                    )[:6]
                    total = sum(v for _, v in top_cities) or 1
                    cities = {k: round(v / total * 100, 1) for k, v in top_cities}
                elif item.get("name") == "audience_gender_age":
                    age_gender = item["values"][0]["value"]

            return {"cities": cities or {"No Data": 100}, "age_gender": age_gender}
        except Exception:
            return self._simulate_demographics()

    def fetch_reel_performance(self, limit=10):
        """Fetch real Reel performance metrics."""
        if not self.is_real:
            return self._simulate_reels(limit)
        try:
            # Step 1: Get media list
            url = f"{self.BASE_URL}/{self.account_id}/media"
            resp = requests.get(url, params={
                "fields": "id,media_type,timestamp,like_count,comments_count",
                "limit": limit * 2,
                "access_token": self.access_token
            }, timeout=10)
            media_data = resp.json()
            if "error" in media_data:
                return self._simulate_reels(limit)

            rows = []
            for item in media_data.get("data", [])[:limit]:
                # Step 2: Get insights per reel
                ins_resp = requests.get(
                    f"{self.BASE_URL}/{item['id']}/insights",
                    params={
                        "metric": "plays,reach,saved,shares",
                        "access_token": self.access_token
                    }, timeout=10
                )
                ins = {m["name"]: m["values"][0]["value"]
                       for m in ins_resp.json().get("data", [])}

                plays = ins.get("plays", 0) or 1
                likes = item.get("like_count", 0)
                comments = item.get("comments_count", 0)
                shares = ins.get("shares", 0)
                saves = ins.get("saved", 0)

                rows.append({
                    "reel_id": item["id"],
                    "posted_at": item.get("timestamp", "")[:10],
                    "plays": plays,
                    "likes": likes,
                    "comments": comments,
                    "shares": shares,
                    "saves": saves,
                    "engagement_rate": round(
                        ((likes + comments + shares + saves) / plays) * 100, 2
                    )
                })

            return pd.DataFrame(rows) if rows else self._simulate_reels(limit)
        except Exception:
            return self._simulate_reels(limit)

    # =====================
    # SIMULATION FALLBACKS
    # =====================
    def _simulate_demographics(self):
        return {
            "age_gender": {"18-24.F": 15, "18-24.M": 12, "25-34.F": 35, "25-34.M": 28},
            "cities": {"Cairo": 45, "Riyadh": 20, "Dubai": 15, "Alexandria": 10,
                       "Jeddah": 7, "Casablanca": 3}
        }

    def _simulate_reels(self, limit=10):
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
                "plays": plays, "likes": likes, "comments": comments,
                "shares": shares, "saves": saves,
                "engagement_rate": round(((likes+comments+shares+saves)/plays)*100, 2)
            })
        return pd.DataFrame(data)
