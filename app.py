from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

from models import db, HouseWorker, Employer

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return jsonify({"message": "Flask API with SQLite is running!"})

# Register a house worker
@app.route('/register_worker', methods=['POST'])
def register_worker():
    data = request.get_json()
    if HouseWorker.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    new_worker = HouseWorker(
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        phone=data.get('phone', ''),
        address=data.get('address', ''),
        expected_salary=data.get('expected_salary', '')
    )
    db.session.add(new_worker)
    db.session.commit()
    return jsonify({"message": "House worker registered successfully."}), 201

# Register an employer
@app.route('/register_employer', methods=['POST'])
def register_employer():
    data = request.get_json()
    if Employer.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    new_employer = Employer(
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        address=data.get('address', '')
    )
    db.session.add(new_employer)
    db.session.commit()
    return jsonify({"message": "Employer registered successfully."}), 201

# Login for house worker
@app.route('/login_worker', methods=['POST'])
def login_worker():
    data = request.get_json()
    worker = HouseWorker.query.filter_by(email=data['email']).first()
    if worker and check_password_hash(worker.password, data['password']):
        return jsonify({"message": "Login successful", "worker_id": worker.id}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Login for employer
@app.route('/login_employer', methods=['POST'])
def login_employer():
    data = request.get_json()
    employer = Employer.query.filter_by(email=data['email']).first()
    if employer and check_password_hash(employer.password, data['password']):
        return jsonify({"message": "Login successful", "employer_id": employer.id}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Get list of all house workers
@app.route('/workers', methods=['GET'])
def get_workers():
    workers = HouseWorker.query.all()
    return jsonify([{
        "id": w.id,
        "name": w.name,
        "email": w.email,
        "phone": w.phone,
        "address": w.address,
        "expected_salary": w.expected_salary
    } for w in workers]), 200

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404
# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render-assigned port or fallback to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
