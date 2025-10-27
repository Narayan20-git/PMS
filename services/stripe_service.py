import stripe
import os
from utils.config_loader import load_config

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Load YAML config
config = load_config()

# Your production URL (deployed FastAPI endpoint)
VERIFICATION_CALLBACK_URL = config["webhook"]["url"]
#VERIFICATION_CALLBACK_URL = os.getenv("VERIFICATION_RETURN_URL")

def create_customer(name, email):
    """Create a Stripe customer"""
    customer = stripe.Customer.create(
        name=name,
        email=email
    )
    return customer


def create_verification_session(customer_id, tenant_id):
    """Create a Stripe Identity Verification Session"""
    session = stripe.identity.VerificationSession.create(
        type="document",
        metadata={"tenant_id": str(tenant_id)},  #matches webhook now
        return_url=f"{VERIFICATION_CALLBACK_URL}?session_id={{VERIFICATION_SESSION_ID}}"  #Redirect after success
    )
    
    return session.url
