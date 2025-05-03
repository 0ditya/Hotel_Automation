from db_config import db
from datetime import datetime

# Admin
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Guest
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    contact = db.Column(db.String(120))
    is_frequent = db.Column(db.Boolean, default=False, nullable=True)
    reservations = db.relationship("Reservation", back_populates="guest")
    food_orders = db.relationship('CateringOrder', backref='guest', lazy=True)
    bills = db.relationship('Bill', backref='guest', lazy=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)

# Room
class Room(db.Model):
    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True)
    roomNumber = db.Column('room_number', db.String(10), unique=True, nullable=False)
    roomType = db.Column('room_type', db.String(50))
    isAC = db.Column('is_ac', db.Boolean)
    baseTariff = db.Column('base_tariff', db.Float)
    currentTariff = db.Column('current_tariff', db.Float)
    isOccupied = db.Column('is_occupied', db.Boolean)
    reservations = db.relationship("Reservation", back_populates="room")

    def __repr__(self):
        return f'<Room {self.roomNumber}>'

# Reservation
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin_date = db.Column(db.Date)
    checkout_date = db.Column(db.Date)
    advance_paid = db.Column(db.Float)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    guest = db.relationship("Guest", back_populates="reservations")
    room = db.relationship("Room", back_populates="reservations")


# Token
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    value = db.Column(db.String(100), unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Bill
class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    total_amount = db.Column(db.Float)
    is_paid = db.Column(db.Boolean, default=False)
'''
class FoodItem(db.Model):
    __tablename__ = 'food_item'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(120))
    quantity = db.Column(db.Integer)
    price_per_unit = db.Column(db.Float)
'''
# Catering Order
class CateringOrder(db.Model):
    __tablename__ = 'catering_order'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    guest_id  = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    items = db.relationship('CateringOrderItem', backref='order', lazy=True)

# Food Item
class FoodMenuItem(db.Model):
    __tablename__ = 'food_menu_item'
    itemID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)

    @property
    def get_total(self):
        return self.quantity * self.price_per_unit
    
class CateringOrderItem(db.Model):
    __tablename__ = 'catering_order_item'
    id = db.Column(db.Integer, primary_key=True)
    orderID = db.Column(db.Integer, db.ForeignKey('catering_order.id'), nullable=False)
    itemID = db.Column(db.Integer)
    item_name = db.Column(db.String(120))
    quantity = db.Column(db.Integer)
    price_per_unit = db.Column(db.Float)
