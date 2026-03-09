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
        self.secret_key = st.secrets.get("STRIPE_SECRET_KEY", None)
        self.is_live = bool(self.secret_key)
        
        if self.is_live:
            try:
                import stripe
                stripe.api_key = self.secret_key
            except ImportError:
                self.is_live = False

    def create_checkout_session(self, plan_name, price_amount, user_email=None):
        """Create a Stripe checkout session."""
        if not self.is_live:
            # Simulation Mode
            return {
                "status": "simulation",
                "url": "https://mtse-platform.example.com/checkout/simulated",
                "message": "Stripe API Key not found. Displaying simulated checkout link."
            }
            
        try:
            import stripe
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                customer_email=user_email,
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"MTSE {plan_name} Plan",
                            "description": f"Enterprise Marketing Platform Subscription"
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
