from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class Review(BaseModel):
    id: str
    text: Optional[str] = None
    rating: Optional[int] = None
    likes_count: Optional[int] = None
    date_created: Optional[datetime] = None  
    
class AdditionalInfo(BaseModel):
    telephone_number: Optional[str] = None
    description: str = None
    avarage_check: int = None
    profile: Dict[str, List[str]] = Field(default_factory=dict)

class Establishment(BaseModel):
    two_gis_id: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    title: Optional[str] = None
    image_urls: List[str] = []  
    address: Optional[str] = None
    coordinates: Optional[List[float]] = None
    additional_info: Optional[AdditionalInfo] = None 
    branch_rating: Optional[float] = None
    branch_reviews_count: Optional[int] = None
    reviews: Optional[List[Review]] = None  

class EstablishmentInDB(Establishment):
    id: str 
