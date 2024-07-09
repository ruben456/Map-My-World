from .database import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, Integer, Float, ForeignKey, DateTime


class LocationCategoryReview(Base):
    __tablename__ = "location_category_reviewed"

    location_id = Column(ForeignKey('locations.id'), primary_key=True)
    category_id = Column(ForeignKey('categories.id'), primary_key=True)
    reviewed = Column(Boolean, default=False)
    review = Column(String, nullable=True, default=None)
    review_at = Column(DateTime, nullable=True)  

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key = True, autoincrement = True)
    latitude = Column(Float)
    longitude = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="locations")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String, unique=True)

    locations = relationship("Location", back_populates="category")
