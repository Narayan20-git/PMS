from typing import List, Optional, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from services.property_service import PropertyService
from schemas.property_schema import PropertySearchRequest, PropertyUpdate

router = APIRouter(prefix="/properties", tags=["Properties"])
property_service = PropertyService()

@router.post("/create_property")
async def create_property(
    json_data: str = Form(...),
    images: List[UploadFile] = File(...)
):
    """
    Create a new property with details (in JSON) and optional image uploads.
    """
    return await property_service.create_property(json_data, images or [])


# ---------------------------------
# UPDATE Property
# ---------------------------------
@router.put("/update_property")
async def update_property(
    json_data: str = Form(...),
    images: Optional[List[UploadFile]] = None,
):
    """
    Update any property fields dynamically, and optionally upload new images.
    JSON should include property_id.
    Example:
    {
        "property_id": "33a5d46c-9cee-4078-b334-74013da5963a",
        "price": 1800,
        "bedrooms": 3
    }
    """
    return await property_service.update_property(json_data, images)


# ---------------------------------
# DELETE Property
# ---------------------------------
@router.delete("/delete_property")
def delete_property(request: PropertyUpdate):
    """
    Delete a property and all its images from Supabase storage and table.
    Example JSON:
    {
        "property_id": "6df465b0-e53b-4c76-8b2f-adbe6faafc0c"
    }
    """
    try:
        return property_service.delete_property(request.property_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Search properties
# ---------------------------
@router.post("/search_property")
def search_property(search_data: PropertySearchRequest):
    """
    Search properties dynamically using JSON body.
    Example JSON:
    {
        "location": "Mumbai",
        "property_type": "Apartment",
        "min_price": 1000,
        "max_price": 3000,
        "bedrooms": 2
    }
    """
    try:
        return property_service.search_property(search_data.dict(exclude_none=True))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


