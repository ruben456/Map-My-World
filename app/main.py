from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

from app import crud, models, schemas
from app.database import SessionLocal, engine

app = FastAPI(title="Technical test 'Map My World'")
models.Base.metadata.create_all(bind=engine)

#Dependency to get de Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/categories/", response_model=list[schemas.Category])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get a list of all categories created

    Args:
        skip (int): start of pagination. Defaults to 0.
        limit (int): limit of pagination. Defaults to 100.
        db (Session): connection to data base. Defaults to Depends(get_db).

    Returns:
        List[schemas.Category]: A list Category objects 
    """
    try:
        categories = crud.get_categories(db, skip=skip, limit=limit)
        return categories
    except:
        raise HTTPException(status_code=500, detail="Internal Error getting the category list")

@app.get("/categories/{category_id}", response_model=schemas.Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by id

    Args:
        category_id (int): category id to search
        db (Session): connection to data base. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 not found, 500 internal error

    Returns:
        schemas.Category: Category object
    """
    try:
        db_category = crud.get_category(db, category_id=category_id)
        if db_category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return db_category
    except:
        raise HTTPException(status_code=500, detail=f"Internal Error getting the category {category_id}")

@app.get("/locations/{location_id}", response_model=schemas.Location)
def get_location(location_id: int, db: Session = Depends(get_db)):
    """Get a specific location by id

    Args:
        location_id (int): location id to search
        db (Session): connection to data base. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 not found, 500 internal error

    Returns:
        schemas.Location: Location object
    """
    try:
        db_location = crud.get_location(db, location_id=location_id)
        if db_location is None:
            raise HTTPException(status_code=404, detail="Location not found")
        return db_location
    except:
        raise HTTPException(status_code=500, detail=f"Internal Error getting the location {location_id}")

@app.get("/locations/", response_model=list[schemas.Location])
def get_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get a list of all locations in data base

    Args:
        skip (int): start of pagination. Defaults to 0.
        limit (int): limit of pagination. Defaults to 100.
        db (Session): connection to data base. Defaults to Depends(get_db).

    Raises:
        HTTPException: 500 internal error

    Returns:
        List[schemas.Location]: A list Location objects 
    """
    try:
        locations = crud.get_locations(db, skip=skip, limit=limit)
        return locations
    except:
        raise HTTPException(status_code=500, detail="Internal Error getting the location list")

@app.get("/recommendations/", response_model=list[schemas.Location])
def get_recommendations(db: Session = Depends(get_db)):
    """Get a list of all locations in data base

    Args:
        skip (int): start of pagination. Defaults to 0.
        limit (int): limit of pagination. Defaults to 100.
        db (Session): connection to data base. Defaults to Depends(get_db).

    Raises:
        HTTPException: 500 internal error

    Returns:
        List[schemas.Location]: A list Location objects 
    
    """
    try:
        return crud.get_recommendations(db)
    except:
        raise HTTPException(status_code=500, detail="Internal Error getting the recommendations list")

@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Endpoint to create a new category in data base

    Args:
        category (schemas.CategoryCreate): Category schema
        db (Session): connection to data base. Defaults to Depends(get_db).

    Raises:
        HTTPException: 400 bad request, 500 internal error

    Returns:
        category (schemas.Category): Category object
    """
    try:
        db_category = crud.get_category_by_name(db, name=category.name)
        if db_category:        
            raise HTTPException(status_code=400, detail=f"Category '{category.name}' already exists")
        return crud.create_category(db=db, category=category)
    except:
        raise HTTPException(status_code=500, detail=f"Internal Error creating the new category {category.name}")

@app.post("/locations/", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    """Endpoint to create a new location in data base

    Args:
        location (schemas.LocationCreate): _description_
        db (Session): connection to data base. Defaults to Depends(get_db).

    Raises:
        HTTPException: 400 bad request, 500 internal error

    Returns:
        schemas.Location: Location object
    """
    try:
        db_location = crud.get_location_by_longitude_and_latitude(db, latitude=location.latitude, longitude=location.longitude, category_id=location.category_id)
        if db_location:        
            raise HTTPException(status_code=400, detail=f"Location '{location.latitude}, {location.longitude}' for category {location.category_id} already exists")
        return crud.create_location(db, location=location)
    except:
        raise HTTPException(status_code=500, detail="Internal Error creating the new location")

@app.patch("/reviews/", response_model=schemas.LocationCategoryReview)
def review_location_category(location_id: int, category_id: int, review: str, db: Session = Depends(get_db)):
    """Review a location and category

    Args:
        location_id (int): location id to review
        category_id (int): category id to review
        review (str): review to store in data base
        db (Session): connection to data base. Defaults to Depends(get_db).

    Raises:
        HTTPException: 500 internal error

    Returns:
        schemas.LocationCategoryReview: Location Category Review object
    """
    try:
        return crud.set_review(db, location_id=location_id, category_id=category_id, review=review)
    except:
        raise HTTPException(status_code=500, detail="Internal Error reviewing the new location and category")