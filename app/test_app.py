from unittest import TestCase
from unittest.mock import call, create_autospec

from app.crud import create_category, create_location
from app.models import Category, Location
from app.schemas import CategoryCreate, LocationCreate
from sqlalchemy.orm import Session

class TestApp(TestCase):
    """
    Class for running crud tests     
    """

    def test_create_category(self) -> None:        
        input_category = CategoryCreate(name="test 1")        
        mock_session = create_autospec(Session, instance=True)
        expected_category = Category(id=1,name="test 1")
        output = create_category(mock_session, input_category)

        #Test output category
        self.assertEqual(expected_category.name, output.name)

    def test_create_location(self) -> None:
        input_location = LocationCreate(
            latitude = 1,
            longitude = 1,
            category_id = 1
        )
        mock_session = create_autospec(Session, instance=True)
        expected_location = Location(
            latitude = 1,
            longitude = 1,
            category_id = 1
        )
        output = create_location(mock_session, input_location)

        #Test output location
        self.assertEqual(expected_location.latitude, output.latitude)
        self.assertEqual(expected_location.longitude, output.longitude)
        self.assertEqual(expected_location.category_id, output.category_id)
