from typing import List
from fastapi import APIRouter, UploadFile, File, Form
from services.property_service import create_property_service


router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("/create_property")
async def create_property(
    json_data: str = Form(...),
    images: List[UploadFile] = File(...)
):
    """
    Creates property with async image uploads.
    """
    return await create_property_service(json_data, images)