# routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from models import Admin, Room, Guest, CateringOrder, CateringOrderItem, Reservation
from flask_cors import cross_origin
from db_config import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    print(f"🟡 Login attempt → role: {role}, email: {email}, password: {password}")

    if role == "admin":
        user = Admin.query.filter_by(username=email).first()
    else:
        user = Guest.query.filter_by(email=email).first()

    print(f"🔍 Found user: {user}")

    if user:
        print(f"👁 Stored password: {user.password}")
        if user.password == password:
            print("✅ Password match")
            return jsonify({"success": True, "role": role})
        else:
            print("❌ Password mismatch")
    else:
        print("❌ User not found")

    return jsonify({"success": False}), 401

@admin_bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/guests')
def view_guests():
    guests = Guest.query.all()
    return render_template('admin/guests.html', guests=guests)

@admin_bp.route('/rooms-data', methods=['GET','OPTIONS','POST'])
def get_rooms_data():
    rooms = Room.query.all()
    room_list = [
        {
            "id":room.id,
            "room_number": room.roomNumber,
            "room_type": room.roomType,
            "is_ac": room.isAC,
            "base_tariff": room.baseTariff,
            "current_tariff": room.currentTariff,
            "is_occupied": room.isOccupied
        }
        for room in rooms
    ]
    return jsonify(room_list)

@admin_bp.route('/guests-data')
def get_guests():
    guests = Guest.query.all()
    return jsonify([
        {
            "id": g.id,
            "name": g.name,
            "email": g.email,
            "contact": g.contact,
            "is_frequent": g.is_frequent
        } for g in guests
    ])

@admin_bp.route('/catering-orders-data')
def catering_orders_data():
    orders = CateringOrder.query.order_by(CateringOrder.id.desc()).all()
    result = []
    for o in orders:
        # Fetch guest
        guest = Guest.query.get(o.guest_id)
        # Fetch items
        items = CateringOrderItem.query.filter_by(orderID=o.id).all()
        item_list = [
            {
            "name": it.item_name,
            "quantity": it.quantity,
            "price": it.price_per_unit or 0.0    # default None→0.0
            }
            for it in items
        ]
        total = sum(it["quantity"] * it["price"] for it in item_list)
        result.append({
            "id": o.id,
            "guestName": guest.name if guest else "Unknown",
            "items": item_list,
            "total": total
        })
    return jsonify(result)

@admin_bp.route('/reservations-data', methods=['GET'])
def get_reservations():
    reservations = Reservation.query.all()
    data = []

    for res in reservations:
        data.append({
            "id": res.id,
            "guest_name": res.guest.name if res.guest else "Unknown",
            "room_number": res.room.roomNumber if res.room else "Unknown",
            "check_in": res.checkin_date.strftime("%Y-%m-%d") if res.checkin_date else "N/A",
            "check_out": res.checkout_date.strftime("%Y-%m-%d") if res.checkout_date else "N/A",
            "advance_paid": res.advance_paid or 0.0
        })

    return jsonify(data)
