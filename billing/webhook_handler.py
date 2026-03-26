import streamlit as st
import database
import json

def handle_webhook_event(event_data):
    """
    Simulated Webhook Handler for V10.
    In a real app, this would be an endpoint receiving Stripe JSON.
    """
    event_type = event_data.get("type")
    
    if event_type == "checkout.session.completed":
        session = event_data.get("data", {}).get("object", {})
        username = session.get("client_reference_id")
        plan_name = session.get("metadata", {}).get("plan_name")
        stripe_sub_id = session.get("subscription")
        stripe_cus_id = session.get("customer")
        
        if username and plan_name:
            database.update_plan(username, plan_name, stripe_sub_id, stripe_cus_id, 'Active')
            database.log_activity(username, f"Subscription upgraded to {plan_name} via Stripe")
            return True, f"User {username} upgraded to {plan_name}"
            
    elif event_type == "customer.subscription.deleted":
        sub = event_data.get("data", {}).get("object", {})
        # Here we would need to find the user by sub_id
        # For simulation, we assume user is found
        return True, "Subscription cancelled"
        
    return False, "Unhandle event type"

def simulate_upgrade(username, plan_name):
    """Shortcut for testing V10 upgrades."""
    mock_event = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "client_reference_id": username,
                "metadata": {"plan_name": plan_name},
                "subscription": "sub_test_123",
                "customer": "cus_test_123"
            }
        }
    }
    return handle_webhook_event(mock_event)
