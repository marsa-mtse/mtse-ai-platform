# ==========================================================
# MTSE Marketing Engine - Feature Flag System (Plans)
# ==========================================================

from config import PLAN_LIMITS

class PlanManager:
    """
    Manages access to features based on the user's plan.
    """
    def __init__(self, current_plan):
        self.plan = current_plan

    def can_access_ai_generator(self):
        """AI Generator is available to Pro and Business."""
        return self.plan in ["Pro", "Business"]

    def can_access_viral_analyzer(self):
        """Viral Analyzer is Business only."""
        return self.plan == "Business"

    def can_access_trend_predictor(self):
        """Trend Predictor is Business only."""
        return self.plan == "Business"
        
    def can_access_integrations(self):
        """Direct API integrations available to Pro and Business."""
        return self.plan in ["Pro", "Business"]

    def can_access_white_label(self):
        """White Label is Business only."""
        return self.plan == "Business"

    def get_features_list(self):
        """Return a dictionary of feature flags for the current plan."""
        return {
            "ai_campaign_generator": self.can_access_ai_generator(),
            "viral_analyzer": self.can_access_viral_analyzer(),
            "trend_predictor": self.can_access_trend_predictor(),
            "api_integrations": self.can_access_integrations(),
            "white_label": self.can_access_white_label(),
            "reports_limit": PLAN_LIMITS.get(self.plan, {}).get("reports", 0),
            "uploads_limit": PLAN_LIMITS.get(self.plan, {}).get("uploads", 0)
        }
