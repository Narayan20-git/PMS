import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # Make sure this is set in your .env

def create_customer(name, email):
    """Create a Stripe customer"""
    customer = stripe.Customer.create(
        name=name,
        email=email
    )
    return customer

def create_verification_session(customer_id, tenant_id):
    """Create a Stripe Identity Verification Session"""
    # Note: Do NOT pass `customer` unless using a connected endpoint that supports it
    session = stripe.identity.VerificationSession.create(
        type="document",  # type of verification
        metadata={"tenant_id": str(tenant_id)},  # optional, helpful to track
        # Optional: return_url to redirect after verification
        # return_url="https://yourapp.com/verification-complete"
    )
    
    return session.url
