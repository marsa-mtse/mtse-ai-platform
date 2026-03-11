# ==========================================================
# MTSE Marketing Engine - Feature Flag System (Plans)
# ==========================================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PLAN_LIMITS

class PlanManager:
    """
    Manages access to features based on the MTSE Disruptor tiers.
    """
    def __init__(self, current_plan):
        # Legacy mapping for compatibility during transition
        plan_map = {"Starter": "Explorer", "Pro": "Strategist", "Business": "Command"}
        self.plan = plan_map.get(current_plan, current_plan)

    def can_access_ai_generator(self):
        """Strategist and Command only."""
        return self.plan in ["Strategist", "Command"]

    def can_access_universal_analyzer(self):
        """All plans."""
        return True

    def can_access_competitor_battleground(self):
        """Strategist and Command."""
        return self.plan in ["Strategist", "Command"]

    def can_access_sentiment_command(self):
        """Command (Ultimate) only."""
        return self.plan == "Command"

    def can_access_viral_analyzer(self):
        """Strategist and Command."""
        return self.plan in ["Strategist", "Command"]

    def can_access_trend_predictor(self):
        """Command only."""
        return self.plan == "Command"
        
    def can_access_integrations(self):
        """Command only - V10 Enterprise."""
        return self.plan == "Command"

    def can_access_white_label(self):
        """Command only."""
        return self.plan == "Command"

    def can_access_multimodal(self):
        """Strategist and Command."""
        return self.plan in ["Strategist", "Command"]

    def can_access_campaign_orchestrator(self):
        """Strategist and Command."""
        return self.plan in ["Strategist", "Command"]

    def get_features_list(self):
        """Return a dictionary of feature flags for the current plan."""
        return {
            "ai_generator": self.can_access_ai_generator(),
            "competitor_battleground": self.can_access_competitor_battleground(),
            "sentiment_command": self.can_access_sentiment_command(),
            "api_integrations": self.can_access_integrations(),
            "white_label": self.can_access_white_label(),
            "viral_analyzer": self.can_access_viral_analyzer(),
            "trend_predictor": self.can_access_trend_predictor(),
            "campaign_orchestrator": self.can_access_campaign_orchestrator(),
            "reports_limit": PLAN_LIMITS.get(self.plan, {}).get("reports", 0),
            "uploads_limit": PLAN_LIMITS.get(self.plan, {}).get("uploads", 0)
        }
