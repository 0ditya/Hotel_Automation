# routes/catering.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from db_config import db
from models import CateringOrderItem, CateringOrder  

catering_bp = Blueprint('catering', __name__)

# ✅ Hardcoded static food menu
STATIC_MENU = [
    { "itemID": 1, "name": "Paneer Butter Masala", "price": 180 },
    { "itemID": 2, "name": "Veg Biryani", "price": 150 },
    { "itemID": 3, "name": "Tandoori Roti", "price": 20 },
    { "itemID": 4, "name": "Gulab Jamun", "price": 40 }
]

# ✅ API: Serve static menu to React
@catering_bp.route('/api/guest/food-menu', methods=['GET'])
def get_static_menu():
    return jsonify(STATIC_MENU)

# ✅ API: Submit food order from React frontend
@catering_bp.route('/api/guest/food-order', methods=['POST'])
def submit_food_order_api():
    data = request.get_json()
    guest_id = session.get('guest_id')
    items = data.get('items', [])

    if not guest_id:
        return jsonify({ "success": False, "message": "Guest not logged in" }), 401

    if not items:
        return jsonify({ "success": False, "message": "Empty order" }), 400

    order = CateringOrder(guest_id=guest_id)
    db.session.add(order)
    db.session.flush()  # So we get order.orderID

    for item in items:
        menu_item = next((m for m in STATIC_MENU if m["itemID"] == item["itemID"]), None)
        if not menu_item:
            continue
        db.session.add(CateringOrderItem(
            orderID=order.id,
            itemID=item['itemID'],
            item_name=item['name'],
            quantity=item['quantity'],
            price_per_unit=item['price']
        ))

    db.session.commit()
    return jsonify({ "success": True })

# ✅ Admin route (template-based)
@catering_bp.route('/admin/catering-orders')
def view_orders():
    orders = CateringOrder.query.all()
    return render_template('admin/view_orders.html', orders=orders)
