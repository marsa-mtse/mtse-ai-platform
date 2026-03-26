# ==========================================================
# MTSE Marketing Engine - Feature Flag System
# Plans: Starter (Free), Pro (Paid), Command (Enterprise Paid)
# ==========================================================

class PlanManager:
    """
    Starter  = Free plan  (basic access)
    Pro      = Paid plan  (advanced AI features)
    Command  = Enterprise (everything unlimited)
    """
    PAID_PLANS = ["Pro", "Command"]
    ENTERPRISE = ["Command"]

    def __init__(self, current_plan="Starter"):
        # Legacy mapping
        legacy_map = {
            "Explorer": "Starter",
            "Strategist": "Pro",
            "Business": "Command"
        }
        self.plan = legacy_map.get(current_plan, current_plan)

    # ---------- FEATURE GATES ----------

    def can_access_ai_generator(self):
        """All plans - but free is limited to 5/month (enforced by DB counter)."""
        return True

    def can_access_universal_analyzer(self):
        return True

    def can_access_competitor_battleground(self):
        """Pro and Command only."""
        return self.plan in self.PAID_PLANS

    def can_access_sentiment_command(self):
        """Pro and Command only."""
        return self.plan in self.PAID_PLANS

    def can_access_viral_analyzer(self):
        """All plans."""
        return True

    def can_access_trend_predictor(self):
        """Command (Enterprise) only."""
        return self.plan in self.ENTERPRISE

    def can_access_integrations(self):
        """Pro and Command only."""
        return self.plan in self.PAID_PLANS

    def can_access_white_label(self):
        """Command only."""
        return self.plan in self.ENTERPRISE

    def can_access_multimodal(self):
        """Pro and Command only."""
        return self.plan in self.PAID_PLANS

    def can_access_campaign_orchestrator(self):
        """Pro and Command only."""
        return self.plan in self.PAID_PLANS

    def can_access_image_studio(self):
        """Pro and Command only."""
        return self.plan in self.PAID_PLANS

    def can_access_video_scripts(self):
        """Pro and Command only."""
        return self.plan in self.PAID_PLANS

    def can_access_email_campaigns(self):
        """Pro and Command only."""
        return self.plan in self.PAID_PLANS

    def get_plan_badge(self):
        badges = {
            "Starter": ("🆓", "#34d399"),
            "Pro":     ("⚡", "#a78bfa"),
            "Command": ("👑", "#f0abfc"),
        }
        return badges.get(self.plan, ("🆓", "#94a3b8"))

    def get_features_list(self):
        return {
            "ai_generator": self.can_access_ai_generator(),
            "competitor_battleground": self.can_access_competitor_battleground(),
            "sentiment_command": self.can_access_sentiment_command(),
            "api_integrations": self.can_access_integrations(),
            "white_label": self.can_access_white_label(),
            "viral_analyzer": self.can_access_viral_analyzer(),
            "trend_predictor": self.can_access_trend_predictor(),
            "campaign_orchestrator": self.can_access_campaign_orchestrator(),
            "image_studio": self.can_access_image_studio(),
            "video_scripts": self.can_access_video_scripts(),
            "email_campaigns": self.can_access_email_campaigns(),
        }
