import datetime
from sqlalchemy import or_, nullsfirst
from sqlalchemy.orm import Session

from . import models, schemas

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def create_location(db: Session, location: schemas.LocationCreate):
    db_location = models.Location(latitude=location.latitude, longitude=location.longitude, category_id=location.category_id)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)

    #Create a 'location_category_reviewed' register in data base for the new location for future review
    db_location_category_reviewed = models.LocationCategoryReview(location_id=db_location.id, category_id=db_location.category_id)
    db.add(db_location_category_reviewed)
    db.commit()

    return db_location


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.id == location_id).first()

def get_location_by_longitude_and_latitude(db: Session, latitude: float, longitude: float, category_id: int):
    return db.query(models.Location).filter(
        models.Location.latitude == latitude,
        models.Location.longitude == longitude, 
        models.Location.category_id == category_id
    ).first()

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Location).offset(skip).limit(limit).all()

def get_recommendations(db: Session):
    result = []
    current_time = datetime.datetime.now()
    filter_time = current_time - datetime.timedelta(days=30)
    reviews = db.query(models.LocationCategoryReview).filter(
        or_(models.LocationCategoryReview.review_at == None, models.LocationCategoryReview.review_at > filter_time)
    ).order_by(nullsfirst(models.LocationCategoryReview.review_at.desc())).limit(10)
    for review in reviews:
        db_location = db.query(models.Location).filter(models.Location.id == review.location_id).first()
        result.append(db_location)
    return result

def set_review(db: Session, location_id: int, category_id: int, review: str):
    db.query(models.LocationCategoryReview).filter(
        models.LocationCategoryReview.location_id == location_id, models.LocationCategoryReview.category_id == category_id
    ).update({'reviewed': True, 'review': review, 'review_at': datetime.datetime.now()})
    db.commit()
    db_review = db.query(models.LocationCategoryReview).filter(
        models.LocationCategoryReview.location_id == location_id, models.LocationCategoryReview.category_id == category_id
    ).first()
    return db_review


