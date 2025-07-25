from sqlalchemy.orm import Session

from tests.factories import ClientFactory, ParkingFactory


def test_create_client_with_factory(db_session: Session) -> None:
    client = ClientFactory.create()
    assert client.id is not None
    assert client.name is not None


def test_create_parking_with_factory(db_session: Session) -> None:
    parking = ParkingFactory.create()
    assert parking.count_places == parking.count_available_places
