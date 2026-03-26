# MTSE Marketing Engine v13 - Pages Package
from . import dashboard_page
from . import analytics_page
from . import reports_page
from . import users_page
from . import billing_page
from . import settings_page
from . import workspace_page
from . import video_intel_page
from . import intel_hub_page
from . import creative_hub_page
from . import social_command_page
from . import campaign_builder_view
from . import owner_panel_page
from . import ai_engine_page

# v13 New Modules
try:
    from . import image_generator_page
except Exception:
    pass

try:
    from . import competitor_intel_page
except Exception:
    pass

try:
    from . import trend_forecaster_page
except Exception:
    pass

try:
    from . import email_campaign_page
except Exception:
    pass
