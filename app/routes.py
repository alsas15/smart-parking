from flask import Blueprint, request, jsonify
from datetime import datetime
from . import db
from .models import Client, Parking, ClientParking

bp = Blueprint('api', __name__)

@bp.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "surname": c.surname
    } for c in clients])

@bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    c = Client.query.get_or_404(client_id)
    return jsonify({
        "id": c.id,
        "name": c.name,
        "surname": c.surname,
        "car_number": c.car_number,
        "credit_card": c.credit_card
    })

@bp.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    c = Client(**data)
    db.session.add(c)
    db.session.commit()
    return jsonify({"id": c.id}), 201

@bp.route('/parkings', methods=['POST'])
def create_parking():
    data = request.json
    p = Parking(**data)
    db.session.add(p)
    db.session.commit()
    return jsonify({"id": p.id}), 201

@bp.route('/client_parkings', methods=['POST'])
def enter_parking():
    data = request.json
    client = Client.query.get(data['client_id'])
    parking = Parking.query.get(data['parking_id'])

    if not client or not parking:
        return {"error": "Client or parking not found"}, 404

    if not parking.opened or parking.count_available_places < 1:
        return {"error": "Parking unavailable"}, 400

    cp = ClientParking(
        client_id=client.id,
        parking_id=parking.id,
        time_in=datetime.now()
    )
    db.session.add(cp)
    parking.count_available_places -= 1
    db.session.commit()
    return {"message": "Client entered"}

@bp.route('/client_parkings', methods=['DELETE'])
def exit_parking():
    data = request.json
    cp = ClientParking.query.filter_by(
        client_id=data['client_id'],
        parking_id=data['parking_id']
    ).first()

    if not cp or cp.time_out:
        return {"error": "No active parking session"}, 404

    client = Client.query.get(cp.client_id)
    if not client.credit_card:
        return {"error": "Credit card not linked"}, 400

    cp.time_out = datetime.now()
    parking = Parking.query.get(cp.parking_id)
    parking.count_available_places += 1
    db.session.commit()
    return {"message": "Client exited and paid"}
