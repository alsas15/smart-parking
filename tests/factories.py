from factory.alchemy import SQLAlchemyModelFactory

from app.models import Client, Parking
from app import db


class ClientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    name = "Ivan"
    surname = "Ivanov"
    car_number = "A123BC"
    credit_card = "1234"


class ParkingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    address = "Test Street"
    opened = True
    count_places = 10
    count_available_places = 10
