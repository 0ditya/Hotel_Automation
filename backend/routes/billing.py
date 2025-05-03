from flask import Blueprint, jsonify, session
from datetime import datetime
from models import db, Reservation, CateringOrder, CateringOrderItem, Room
from flask_cors import cross_origin

billing_bp = Blueprint("billing", __name__, url_prefix="/guest")


@billing_bp.route("/bill", methods=["GET"])
@cross_origin(supports_credentials=True)
def get_guest_bill():
    print(f"🔍 Session keys: {list(session.keys())}")
    guest_id = session.get("guest_id")
    if not guest_id:
        print("❌ No guest_id found in session")
        return jsonify({"error": "Unauthorized"}), 401

    print(f"📄 Calculating bill for guest_id: {guest_id}")

    reservations = Reservation.query.filter_by(guest_id=guest_id).all()
    orders = CateringOrder.query.filter_by(guest_id=guest_id).all()

    room_total = 0
    food_total = 0
    bill_breakdown = []

    for res in reservations:
        room = Room.query.get(res.room_id)
        if not room:
            continue
        checkin = res.checkin_date
        checkout = res.checkout_date
        days = (checkout - checkin).days or 1
        rate = room.current_tariff or room.base_tariff or 0
        base = rate * days
        tax = round(base * 0.18, 2)
        total = round(base + tax, 2)
        room_total += total

        bill_breakdown.append({
            "type": "Room",
            "room_number": room.room_number,
            "room_type": room.room_type,
            "checkin": checkin.strftime("%Y-%m-%d"),
            "checkout": checkout.strftime("%Y-%m-%d"),
            "days": days,
            "rate": rate,
            "tax": tax,
            "total": total
        })

    for order in orders:
        items = CateringOrderItem.query.filter_by(orderID=order.id).all()
        order_total = 0
        item_details = []

        for item in items:
            if not item.item_name or not item.price_per_unit:
                continue
            line = item.quantity * item.price_per_unit
            item_details.append({
                "item": item.item_name,
                "quantity": item.quantity,
                "unit_price": item.price_per_unit,
                "line_total": line
            })
            order_total += line

        service = round(order_total * 0.15, 2)
        order_grand = round(order_total + service, 2)
        food_total += order_grand

        bill_breakdown.append({
            "type": "Food",
            "items": item_details,
            "subtotal": order_total,
            "service_charge": service,
            "total": order_grand
        })

    total_amount = round(room_total + food_total, 2)

    print("🧾 Room Total:", room_total)
    print("🧾 Food Total:", food_total)
    print("💵 Grand Total:", total_amount)

    return jsonify({
        "isPaid": False,  # assuming payment isn't tracked
        "totalAmount": total_amount,
        "billBreakdown": bill_breakdown
    })
