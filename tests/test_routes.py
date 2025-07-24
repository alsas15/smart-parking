import pytest
from flask.testing import FlaskClient
from app.models import Client, Parking


@pytest.mark.parametrize("url", ["/clients", "/clients/1"])
def test_get_endpoints(
    client: FlaskClient, setup_data: dict[str, Client | Parking], url: str
) -> None:
    res = client.get(url)
    assert res.status_code == 200


def test_create_client(client: FlaskClient) -> None:
    res = client.post(
        "/clients",
        json={
            "name": "Ivan",
            "surname": "Sidorov",
            "car_number": "X123YZ",
            "credit_card": "5555",
        },
    )
    assert res.status_code == 201


def test_create_parking(client: FlaskClient) -> None:
    res = client.post(
        "/parkings",
        json={
            "address": "Test St",
            "opened": True,
            "count_places": 20,
            "count_available_places": 20,
        },
    )
    assert res.status_code == 201


@pytest.mark.parking
def test_enter_parking(
    client: FlaskClient, setup_data: dict[str, Client | Parking]
) -> None:
    res = client.post(
        "/client_parkings",
        json={
            "client_id": setup_data["client"].id,
            "parking_id": setup_data["parking"].id,
        },
    )
    assert res.status_code == 200


@pytest.mark.parking
def test_exit_parking(
    client: FlaskClient, setup_data: dict[str, Client | Parking]
) -> None:
    res = client.delete(
        "/client_parkings",
        json={
            "client_id": setup_data["client"].id,
            "parking_id": setup_data["parking"].id,
        },
    )
    assert res.status_code == 200
