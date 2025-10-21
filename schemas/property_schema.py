from typing import List, Optional
from pydantic import BaseModel, Field, validator

class PropertyCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    property_type: str = Field(..., pattern="^(Apartment|House|Villa|Studio|Commercial)$")
    price: float = Field(..., gt=0)
    location: str = Field(..., min_length=2)
    bedrooms: Optional[int] = Field(0, ge=0)
    area_in_square_feet: Optional[float] = Field(0, ge=0)
    amenities: Optional[List[str]] = Field(default_factory=list)

    @validator("amenities", pre=True)
    def convert_comma_string_to_list(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v
