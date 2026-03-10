import stripe
import os
import json
from fastapi import FastAPI, Request, HTTPException
from database import update_plan
import uvicorn
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# --- Configuration ---
# In production, these should be environment variables.
# We'll try to read from Streamlit secrets file manually, or fallback to ENV
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

# Fast loading of Streamlit secrets if needed
if not STRIPE_SECRET_KEY:
    try:
        import toml
        secrets_path = os.path.join(".streamlit", "secrets.toml")
        if os.path.exists(secrets_path):
            secrets = toml.load(secrets_path)
            STRIPE_SECRET_KEY = secrets.get("STRIPE_SECRET_KEY")
            STRIPE_WEBHOOK_SECRET = secrets.get("STRIPE_WEBHOOK_SECRET")
    except Exception as e:
        logging.warning(f"Could not load Streamlit secrets: {e}")

stripe.api_key = STRIPE_SECRET_KEY

@app.post("/webhook")
async def stripe_webhook(request: Request):
    """
    Handle incoming Stripe webhooks.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        logging.error("Invalid payload")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logging.error("Invalid signature")
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # We need to know WHICH user bought WHICH plan.
        # This is typically passed in `client_reference_id` or `metadata`.
        username = session.get('client_reference_id')
        plan_name = session.get('metadata', {}).get('plan_name', 'Command') # Fallback to top tier if not set
        
        if username:
            logging.info(f"Payment successful for user {username}. Upgrading to {plan_name}.")
            try:
                # Update database
                update_plan(username, plan_name)
                logging.info(f"Database updated successfully for {username}.")
            except Exception as e:
                logging.error(f"Failed to update database for {username}: {e}")
        else:
            logging.warning("Received successful payment but no client_reference_id (username) was attached.")

    else:
        logging.info(f"Unhandled event type {event['type']}")

    return {"status": "success"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logging.info(f"Starting Stripe Webhook listener on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
