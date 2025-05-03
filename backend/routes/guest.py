from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from models import Guest, CateringOrderItem, FoodMenuItem, Room, Reservation
from utils.pdf_generator import generate_bill_pdf
from db_config import db
from flask_cors import cross_origin
import os
from datetime import datetime

guest_bp = Blueprint('guest', __name__, url_prefix='/guest')

@guest_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']  # No hashing

        new_guest = Guest(name=name, email=email, contact=contact, password=password)
        db.session.add(new_guest)
        db.session.commit()
        flash("Guest registered successfully")
        return redirect(url_for('guest.login'))
    return render_template('guest/register.html')

@guest_bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def login():
    if request.method == 'OPTIONS':
        return jsonify({"message": "CORS preflight OK"}), 200

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = Guest.query.filter_by(email=email).first()

    if user and user.password == password:
        session['guest_id'] = user.id
        print(f"✅ Guest login success, setting session guest_id = {user.id}")
        return jsonify({ "success": True, "role": "guest" })
    else:
        return jsonify({ "success": False }), 401

@guest_bp.route('/dashboard')
def dashboard():
    guest_id = session.get('guest_id')
    guest = Guest.query.get_or_404(guest_id)
    return render_template('guest/dashboard.html', guest=guest)

@guest_bp.route('/reserve', methods=['POST'])
@cross_origin(supports_credentials=True)
def reserve_room():
    guest_id = session.get("guest_id")
    if 'guest_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    print("✅ Guest is authenticated")
    print("➡️ Incoming reservation request:", request.json)
    if not guest_id:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    reservation = Reservation(
        checkin_date=datetime.strptime(data["checkin_date"], "%Y-%m-%d"),
        checkout_date=datetime.strptime(data["checkout_date"], "%Y-%m-%d"),
        advance_paid=float(data["advance_paid"]),
        guest_id=guest_id,
        room_id=int(data["room_id"])
    )

    db.session.add(reservation)
    db.session.commit()

    return jsonify({ "success": True, "reservation_id": reservation.id })

STATIC_MENU = [
    { "itemID": 1, "name": "Paneer Butter Masala", "price": 180 },
    { "itemID": 2, "name": "Veg Biryani", "price": 150 },
    { "itemID": 3, "name": "Tandoori Roti", "price": 20 },
    { "itemID": 4, "name": "Gulab Jamun", "price": 40 }
]

@guest_bp.route('/api/guest/food-menu', methods=['GET'])
def get_static_menu():
    return jsonify(STATIC_MENU)

@guest_bp.route('/food-order', methods=['POST'])
def food_order():
    data = request.get_json()
    items = data.get('items', [])

    # Optionally save to DB here
    print(f"Received food order: {items}")

    return jsonify({'success': True})

@guest_bp.route('/bill', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_guest_bill():
    guest_id = session.get('guest_id')
    if not guest_id:
        return jsonify({"message": "Unauthorized"}), 401

    print(f"🔍 Fetching bill for guest_id: {guest_id}")

    reservations = Reservation.query.filter_by(guest_id=guest_id).all()
    total_room = 0
    for r in reservations:
        if r.room:
            nights = (r.checkout_date - r.checkin_date).days
            rate = r.room.current_tariff or r.room.base_tariff
            total_room += (rate * nights)
    room_tax = total_room * 0.18

    orders = CateringOrderItem.query.join(CateringOrderItem.order).filter_by(guest_id=guest_id).all()
    total_food = sum((item.price_per_unit or 0) * item.quantity for item in orders)
    food_tax = total_food * 0.15

    final_amount = round(total_room + room_tax + total_food + food_tax)

    print(f"🧾 Room: ₹{total_room}, Room Tax: ₹{room_tax}")
    print(f"🍽️ Food: ₹{total_food}, Food Tax: ₹{food_tax}")
    print(f"💰 Total Amount: ₹{final_amount}")

    return jsonify({
        "isPaid": False,
        "totalAmount": final_amount
    })

@guest_bp.route('/bill/pdf', methods=['GET'])
def download_bill_pdf():
    guest_name = "John Doe"
    room_number = "204"
    total_amount = 2400

    # Absolute path for generated_bills directory
    base_dir = os.path.dirname(os.path.abspath(__file__))  # routes folder
    bill_dir = os.path.join(base_dir, "..", "generated_bills")
    os.makedirs(bill_dir, exist_ok=True)

    # Generate absolute path for PDF file
    output_path = os.path.abspath(os.path.join(bill_dir, "hotel_bill.pdf"))

    # Generate PDF
    generate_bill_pdf(guest_name, room_number, total_amount, output_path)

    # Send the file
    return send_file(output_path, as_attachment=True)

__all__ = ['guest_bp']