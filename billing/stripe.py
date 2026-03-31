# ==========================================================
# MTSE Marketing Engine - Stripe Billing Integration
# ==========================================================

import streamlit as st

class BillingEngine:
    """
    Advanced Billing Engine handling Stripe operations.
    If actual keys are unavailable, simulates the entire process gracefully.
    """
    def __init__(self):
        self.secret_key = None
        try:
            from streamlit.errors import StreamlitAPIException
            self.secret_key = st.secrets.get("STRIPE_SECRET_KEY", None)
        except Exception:
            self.secret_key = None
            
        self.is_live = bool(self.secret_key)
        
        if self.is_live:
            try:
                import stripe
                stripe.api_key = self.secret_key
            except ImportError:
                self.is_live = False

    def create_checkout_session(self, plan_name, price_amount, username=None):
        """Create a Stripe checkout session."""
        if not self.is_live:
            # Simulation Mode
            return {
                "status": "simulation",
                "url": f"https://mtse-platform.example.com/checkout/simulated?plan={plan_name}&user={username}",
                "message": "Stripe API Key not found. Displaying simulated checkout link."
            }
            
        try:
            import stripe
            # Pass the username as client_reference_id so the Webhook knows who to upgrade
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                client_reference_id=username, # CRITICAL: Map to MTSE username
                metadata={"plan_name": plan_name},
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"MTSE {plan_name} Plan",
                            "description": f"Enterprise Marketing Platform Subscription - V10 Generation"
                        },
                        "unit_amount": int(price_amount * 100), # cents
                    },
                    "quantity": 1,
                }],
                mode="subscription",
                success_url="https://mtse.streamlit.app/?payment=success",
                cancel_url="https://mtse.streamlit.app/?payment=cancel",
            )
            return {
                "status": "success",
                "url": session.url
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def cancel_subscription(self, subscription_id):
        """Cancel an active subscription."""
        if not self.is_live:
            return True, "Subscription cancelled (Simulated)"
            
        try:
            import stripe
            stripe.Subscription.delete(subscription_id)
            return True, "Subscription cancelled successfully"
        except Exception as e:
            return False, str(e)
