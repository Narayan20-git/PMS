import json
import asyncio
from typing import List, Optional, Dict, Any
from fastapi import UploadFile, HTTPException
from utils.supabase_connection import supabase, SUPABASE_BUCKET_NAME
from schemas.property_schema import PropertyCreate, PropertyUpdate


class PropertyService:
    """Service class to handle property creation, update, delete, search, and image uploads."""

    def __init__(self):
        self.bucket = supabase.storage.from_(SUPABASE_BUCKET_NAME)
        self.table = supabase.table("property_details")

    # ---------------------------------
    # Helper: upload single image
    # ---------------------------------
    async def upload_single_image(self, image: UploadFile, property_id: str) -> str:
        try:
            file_path = f"{property_id}/{image.filename}"
            contents = await image.read()
            self.bucket.upload(file_path, contents)

            public_url = self.bucket.get_public_url(file_path)
            if not public_url:
                raise HTTPException(status_code=500, detail="Failed to retrieve public URL")

            return public_url
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    # ---------------------------------
    # Helper: upload multiple images
    # ---------------------------------
    async def upload_images(self, images: Optional[List[UploadFile]], property_id: str) -> List[str]:
        if not images:
            return []
        upload_tasks = [self.upload_single_image(img, property_id) for img in images]
        return await asyncio.gather(*upload_tasks)

    # ---------------------------------
    # CREATE Property
    # ---------------------------------
    async def create_property(self, json_data: str, images: List[UploadFile]):
        try:
            property_dict = json.loads(json_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in 'json_data'")

        property_obj = PropertyCreate(**property_dict)

        insert_res = self.table.insert(property_obj.dict() | {"images": []}).execute()
        if not insert_res.data:
            raise HTTPException(status_code=500, detail="Failed to insert property data")

        property_id = insert_res.data[0]["property_id"]

        uploaded_urls = await self.upload_images(images, property_id)
        self.table.update({"images": uploaded_urls}).eq("property_id", property_id).execute()

        return {
            "message": "Property created successfully",
            "property_id": property_id,
            "image_urls": uploaded_urls,
        }

    # ---------------------------------
    # UPDATE Property
    # ---------------------------------
    async def update_property(self, json_data: str, images: Optional[List[UploadFile]] = None):
        try:
            property_dict = json.loads(json_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in 'json_data'")

        property_obj = PropertyUpdate(**property_dict)
        property_id = property_obj.property_id

        existing = self.table.select("*").eq("property_id", property_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Property not found")

        existing_images = existing.data[0].get("images", [])

        # commented the code as amenties were coming as empty list
        # update_fields = {
        #     k: v for k, v in property_obj.dict().items()
        #     if v is not None and k != "property_id"
        # }

        update_fields = {
            k: v for k, v in property_dict.items()
            if v is not None and k != "property_id"
        }


        uploaded_urls = await self.upload_images(images, property_id)
        if uploaded_urls:
            update_fields["images"] = existing_images + uploaded_urls

        if not update_fields:
            raise HTTPException(status_code=400, detail="No valid fields to update")

        self.table.update(update_fields).eq("property_id", property_id).execute()

        return {
            "message": "Property updated successfully",
            "property_id": property_id,
            "updated_fields": update_fields,
            "new_images": uploaded_urls,
        }

    # ---------------------------------
    # DELETE Property (and its images)
    # ---------------------------------
    def delete_property(self, property_id: str):
        try:
            existing = self.table.select("*").eq("property_id", property_id).execute()
            if not existing.data:
                raise HTTPException(status_code=404, detail="Property not found")

            # Delete images folder from storage
            files_res = self.bucket.list(path=property_id)
            for f in files_res:
                self.bucket.remove([f"{property_id}/{f['name']}"])

            # Delete property record
            self.table.delete().eq("property_id", property_id).execute()

            return {"message": f"Property {property_id} deleted successfully."}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting property: {str(e)}")

    # ---------------------------------
    # SEARCH Property dynamically
    # ---------------------------------
    def search_property(self, filters: Dict[str, Any]):
            """
            Example filters:
            {
            "location": "Mumbai",
            "property_type": "Apartment",
            "min_price": 1000,
            "max_price": 3000,
            "bedrooms": 2
            }
            """
            try:
                query = self.table.select("*")

                # Apply filters dynamically
                if "location" in filters:
                    query = query.eq("location", filters["location"])
                if "property_type" in filters:
                    query = query.eq("property_type", filters["property_type"])
                if "bedrooms" in filters:
                    query = query.eq("bedrooms", filters["bedrooms"])

                # Handle price range separately
                if "min_price" in filters:
                    query = query.gte("price", filters["min_price"])
                if "max_price" in filters:
                    query = query.lte("price", filters["max_price"])

                results = query.execute()

                if not results.data:
                    return {"message": "No matching properties found", "data": []}

                return {"count": len(results.data), "data": results.data}

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
