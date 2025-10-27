import stripe
import os
from fastapi import APIRouter, Request, HTTPException
from supabase import create_client
from dotenv import load_dotenv
from utils.supabase_connection import supabase

load_dotenv()

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")


@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        print("⚠️ Signature verification failed:", str(e))
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event.get("type")
    session = event.get("data", {}).get("object", {})

    # Verify identity event
    if event_type == "identity.verification_session.verified":
        user_id = session.get("metadata", {}).get("user_id")

        if not user_id:
            print("⚠️ No user_id found in metadata!")
            return {"status": "missing_user_id"}

        #Update Supabase tenant
        response = (
            supabase.table("tenants")
            .update({"is_verified": True})
            .eq("id", user_id)
            .execute()
        )

        print(f"Tenant Verified User ID: {user_id}")

    return {"status": "success"}
