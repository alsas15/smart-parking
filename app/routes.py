from datetime import datetime

from flask import Blueprint, jsonify, request
from flask.wrappers import Response

from . import db
from .models import Client, ClientParking, Parking

bp = Blueprint("api", __name__)


@bp.route("/clients", methods=["GET"])
def get_clients() -> Response:
    clients = Client.query.all()
    return jsonify(
        [{"id": c.id, "name": c.name, "surname": c.surname} for c in clients]
    )

@bp.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id: int) -> Response:
    c = Client.query.get_or_404(client_id)
    return jsonify(
        {
            "id": c.id,
            "name": c.name,
            "surname": c.surname,
            "car_number": c.car_number,
            "credit_card": c.credit_card,
        }
    )

@bp.route("/clients", methods=["POST"])
def create_client() -> Response:
    data = request.json
    c = Client(**data)
    db.session.add(c)
    db.session.commit()
    return jsonify({"id": c.id}), 201

@bp.route("/parkings", methods=["POST"])
def create_parking() -> Response:
    data = request.json
    p = Parking(**data)
    db.session.add(p)
    db.session.commit()
    return jsonify({"id": p.id}), 201

@bp.route("/client_parkings", methods=["POST"])
def enter_parking() -> Response:
    data = request.json
    client = Client.query.get(data["client_id"])
    parking = Parking.query.get(data["parking_id"])

    if not client or not parking:
        return jsonify({"error": "Client or parking not found"}), 404

    if not parking.opened or parking.count_available_places < 1:
        return jsonify({"error": "Parking unavailable"}), 400

    cp = ClientParking(
        client_id=client.id, parking_id=parking.id, time_in=datetime.now()
    )
    db.session.add(cp)
    parking.count_available_places -= 1
    db.session.commit()
    return jsonify({"message": "Client entered"})

@bp.route("/client_parkings", methods=["DELETE"])
def exit_parking() -> Response:
    data = request.json
    cp = ClientParking.query.filter_by(
        client_id=data["client_id"], parking_id=data["parking_id"]
    ).first()

    if not cp or cp.time_out:
        return jsonify({"error": "No active parking session"}), 404

    client = Client.query.get(cp.client_id)
    if not client.credit_card:
        return jsonify({"error": "Credit card not linked"}), 400

    cp.time_out = datetime.now()
    parking = Parking.query.get(cp.parking_id)
    parking.count_available_places += 1
    db.session.commit()
    return jsonify({"message": "Client exited and paid"})
