from datetime import datetime
from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from app import create_app, db
from app.models import Client, ClientParking, Parking


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    app = create_app()
    app.config.update(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def db_session(app: Flask) -> Generator[Session, None, None]:
    with app.app_context():
        yield db.session


@pytest.fixture
def setup_data(db_session: Session) -> dict[str, object]:
    client = Client(
        name="Ivan", surname="Ivanov", car_number="A123BC", credit_card="1234"
    )
    parking = Parking(
        address="Main Street", opened=True, count_places=10, count_available_places=5
    )
    db_session.add(client)
    db_session.add(parking)
    db_session.commit()

    cp = ClientParking(
        client_id=client.id, parking_id=parking.id, time_in=datetime.now()
    )
    db_session.add(cp)
    db_session.commit()

    return {"client": client, "parking": parking}
