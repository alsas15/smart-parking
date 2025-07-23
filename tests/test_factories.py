import pytest
from tests.factories import ClientFactory, ParkingFactory

def test_create_client_with_factory(db_session):
    client = ClientFactory(sqlalchemy_session=db_session)
    assert client.id is not None
    assert client.name is not None

def test_create_parking_with_factory(db_session):
    parking = ParkingFactory(sqlalchemy_session=db_session)
    assert parking.count_places == parking.count_available_places
