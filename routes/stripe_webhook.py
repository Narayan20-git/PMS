import stripe
import os
from fastapi import APIRouter, Request, HTTPException
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
    print("🔔 Webhook received")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        print("⚠️ Signature verification failed:", str(e))
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event.get("type")
    session = event.get("data", {}).get("object", {})

    if event_type == "identity.verification_session.verified":
        metadata = session.get("metadata", {})
        tenant_id = metadata.get("tenant_id")

        print("Metadata:", metadata)
        print("tenant_id:", tenant_id)

        if not tenant_id:
            print("⚠️ No tenant_id in metadata!")
            return {"status": "missing_tenant_id"}

        resp = supabase.table("tenants") \
            .update({"is_verified": True}) \
            .eq("id", tenant_id) \
            .execute()

        print("Updated tenant verification:", resp)

    return {"status": "success"}
