import uuid
import asyncio
import json
from fastapi import UploadFile, HTTPException
from typing import List
from schemas.property_schema import PropertyCreate
from utils.supabase_connection import supabase, SUPABASE_BUCKET_NAME


# ---------------------------
# Upload single image
# ---------------------------
async def upload_single_image(image: UploadFile, property_id: str) -> str:
    try:
            
        file_path = f"{property_id}/{image.filename}"
        contents = await image.read()

        supabase.storage.from_(SUPABASE_BUCKET_NAME).upload(file_path, contents)

        # Get public URL
        public_url = supabase.storage.from_(SUPABASE_BUCKET_NAME).get_public_url(file_path)
        

        
        if not public_url:
            raise HTTPException(status_code=500, detail="Failed to retrieve public URL from Supabase")

        return public_url
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# ---------------------------
# Create property service
# ---------------------------
async def create_property_service(json_data: str, images: list[UploadFile]):
    # Step 1: Parse and validate input JSON
    try:
        property_dict = json.loads(json_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in 'json_data' field")

    property_obj = PropertyCreate(**property_dict)

    # Step 2: Insert property record (without images)
    insert_res = supabase.table("property_details").insert(property_obj.dict() | {"images": []}).execute()
    if not insert_res.data:
        raise HTTPException(status_code=500, detail="Failed to insert property data")

    property_id = insert_res.data[0]["property_id"]

    # Step 3: Upload images concurrently
    upload_tasks = [upload_single_image(img, property_id) for img in images]
    uploaded_urls = await asyncio.gather(*upload_tasks)

    # Step 4: Update DB with image URLs
    supabase.table("property_details").update({"images": uploaded_urls}).eq("property_id", property_id).execute()

    return {
        "message": "Property created successfully",
        "property_id": property_id,
        "image_urls": uploaded_urls,
    }
