# utils/auth_utils.py
from flask_login import UserMixin

class AdminUser(UserMixin):
    def __init__(self, id):
        self.id = id
        self.role = 'admin'

class GuestUser(UserMixin):
    def __init__(self, id):
        self.id = id
        self.role = 'guest'

# Flask-Login user loader (to be used in db_config or app.py)
# Must be integrated with actual Admin/Guest models
