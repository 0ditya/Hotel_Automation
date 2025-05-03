import unittest
from flask import session
from backend.db_config import create_app, db
from backend.models import Guest, Room, FoodItem, Reservation, CateringOrder, CateringOrderItem

class HotelAutomationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SECRET_KEY'] = 'testkey'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Seed database
            guest = Guest(name="Test User", contact="1234567890", email="test@example.com", password="hashedpass")
            room = Room(room_number="101", room_type="Single", is_ac=True, base_tariff=1500.0, current_tariff=1500.0, is_occupied=False)
            food = FoodItem(item_name="Pizza", price_per_unit=250.0)

            db.session.add_all([guest, room, food])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_guest_creation(self):
        with self.app.app_context():
            guest = Guest.query.filter_by(email="test@example.com").first()
            self.assertIsNotNone(guest)
            self.assertEqual(guest.name, "Test User")

    def test_room_availability(self):
        with self.app.app_context():
            room = Room.query.first()
            self.assertFalse(room.is_occupied)

    def test_food_menu_item(self):
        with self.app.app_context():
            item = FoodItem.query.first()
            self.assertEqual(item.item_name, "Pizza")

    def test_reservation_creation(self):
        with self.app.app_context():
            guest = Guest.query.first()
            room = Room.query.first()
            reservation = Reservation(
                guest_id=guest.id,
                room_id=room.id,
                checkin_date="2025-04-20",
                checkout_date="2025-04-22",
                advance_paid=500
            )
            db.session.add(reservation)
            db.session.commit()

            self.assertEqual(Reservation.query.count(), 1)
            self.assertEqual(reservation.advance_paid, 500)

    def test_catering_order(self):
        with self.app.app_context():
            guest = Guest.query.first()
            order = CateringOrder(guest_id=guest.id)
            db.session.add(order)
            db.session.commit()

            item = FoodItem.query.first()
            order_item = CateringOrderItem(
                orderID=order.id,
                itemID=item.id,
                item_name=item.item_name,
                quantity=2,
                price_per_unit=item.price_per_unit
            )
            db.session.add(order_item)
            db.session.commit()

            self.assertEqual(CateringOrder.query.count(), 1)
            self.assertEqual(CateringOrderItem.query.first().quantity, 2)

if __name__ == '__main__':
    unittest.main()
