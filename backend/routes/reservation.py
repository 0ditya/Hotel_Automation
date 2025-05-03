# backend/routes/reservation.py

from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from db_config import db
from models import Reservation

#guest_bp = Blueprint('guest_reservation', __name__)
reservation_bp = Blueprint("reservation", __name__)
'''
@reservation_bp.route('/reserve', methods=['POST'])
@cross_origin(supports_credentials=True)
def guest_reserve():
    data = request.get_json()
    print("📦 Received data in /guest/reserve:", data)
    room_number = data.get("roomNumber")
    check_in = data.get("checkInDate")
    check_out = data.get("checkOutDate")
    advance = data.get("advance")
    guest_id = session.get("guest_id")

    if not guest_id:
        return jsonify({"success": False, "message": "Login required"}), 401

    reservation = Reservation(
        guest_id=guest_id,
        room_number=room_number,
        check_in=check_in,
        check_out=check_out,
        advance=advance
    )
    db.session.add(reservation)
    db.session.commit()

    print("🚨 /guest/reserve endpoint HIT!")  # fallback print
    try:
        data = request.get_json()
        print("📦 Received data:", data)
    except Exception as e:
        print("❌ Error parsing JSON:", e)

    return jsonify({"success": True})
'''