from typing import Union
from datetime import datetime

from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class LocationBase(BaseModel):
    latitude: float
    longitude: float
    category_id: int

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    category: Category

    class Config:
        orm_mode = True

class LocationCategoryReview(BaseModel):
    location_id: int
    category_id: int
    review: str

    class Config:
        orm_mode = True
