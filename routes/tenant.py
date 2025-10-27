import os
from fastapi import APIRouter, HTTPException, Form
from supabase import create_client
from services.stripe_service import create_customer, create_verification_session
from dotenv import load_dotenv
from utils.supabase_connection import supabase


load_dotenv()

router = APIRouter()


@router.post("/signup")
def tenant_signup(
    name: str = Form(...),
    email: str = Form(...)
):
    try:
        # Create Stripe Customer
        customer = create_customer(name, email)
        
        # Store tenant in Supabase
        result = supabase.table("tenants").insert({
            "name": name,
            "email": email,
            "stripe_customer_id": customer.id,
            "is_verified": False
        }).execute()
        
        tenant_id = result.data[0]["id"]

        # Create Stripe Identity Verification Session
        verification_url = create_verification_session(customer.id, tenant_id)
        
        return {
            "message": "Tenant created successfully",
            "tenant_id": tenant_id,
            "verification_url": verification_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
