from typing import List, Optional
from pydantic import BaseModel, Field, validator


# ---------------------------------
# BASE SCHEMA (shared)
# ---------------------------------
class PropertyBase(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    property_type: Optional[str] = Field(
        None, pattern="^(Apartment|House|Villa|Studio|Commercial)$"
    )
    price: Optional[float] = Field(None, gt=0)
    location: Optional[str] = Field(None, min_length=2)
    bedrooms: Optional[int] = Field(None, ge=0)
    area_in_square_feet: Optional[float] = Field(None, ge=0)
    amenities: Optional[List[str]] = Field(default_factory=list)

    @validator("amenities", pre=True)
    def convert_comma_string_to_list(cls, v):
        """Allow amenities to be passed as a comma-separated string."""
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v


# ---------------------------------
# CREATE SCHEMA (for POST)
# ---------------------------------
class PropertyCreate(PropertyBase):
    title: str = Field(..., min_length=3, max_length=100)
    property_type: str = Field(
        ..., pattern="^(Apartment|House|Villa|Studio|Commercial)$"
    )
    price: float = Field(..., gt=0)
    location: str = Field(..., min_length=2)
    bedrooms: int = Field(None, ge=0)
    area_in_square_feet: float = Field(None, ge=0)


# ---------------------------------
# UPDATE SCHEMA (for PUT)
# ---------------------------------
class PropertyUpdate(PropertyBase):
    property_id: str = Field(..., description="Unique property identifier")


# ---------------------------
# Request schema for search
# ---------------------------
class PropertySearchRequest(BaseModel):
    location: Optional[str] = None
    property_type: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    bedrooms: Optional[int] = None
