from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config import db, login_manager

from routes.guest import guest_bp
from routes.admin import admin_bp
from routes.billing import billing_bp
#from routes import reservation
from routes.catering import catering_bp
from routes.admin import admin_bp

from models import *

app = Flask(__name__)
CORS(app,
     supports_credentials=True,
     resources={
         r"/admin/*": {"origins": "http://localhost:5173"},
         r"/api/*":   {"origins": "http://localhost:5173"},
         r"/guest/*": {"origins": "http://localhost:5173"}
     })

# Config
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hotel_user:your_password@localhost/hotel_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize with app
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# Register blueprints
app.register_blueprint(guest_bp, url_prefix="/guest")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(billing_bp, url_prefix="/guest")
#app.register_blueprint(reservation.guest_bp, url_prefix="/guest")
app.register_blueprint(catering_bp)

@app.route('/login', methods=['POST', 'OPTIONS'])
def universal_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if role == "guest":
        user = Guest.query.filter_by(email=email).first()
    else:
        return jsonify({"success": False}), 401

    if user and user.password == password:
        return jsonify({"success": True, "role": role})
    else:
        return jsonify({"success": False}), 401

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
