from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Initialize app
app = Flask(__name__)
CORS(app)

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Models
class HouseWorker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float)
    rating = db.Column(db.Float)

class Employer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create all tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return jsonify({"message": "Flask API with SQLite is running!"})

# Register House Worker
@app.route('/register_worker', methods=['POST'])
def register_worker():
    data = request.get_json()
    new_worker = HouseWorker(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        salary=data.get('salary', 0),
        rating=0
    )
    db.session.add(new_worker)
    db.session.commit()
    return jsonify({"message": "House worker registered successfully."}), 201

# Register Employer
@app.route('/register_employer', methods=['POST'])
def register_employer():
    data = request.get_json()
    new_employer = Employer(
        name=data['name'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_employer)
    db.session.commit()
    return jsonify({"message": "Employer registered successfully."}), 201

# Get all house workers
@app.route('/workers', methods=['GET'])
def get_workers():
    workers = HouseWorker.query.all()
    return jsonify([{
        "id": w.id,
        "name": w.name,
        "email": w.email,
        "salary": w.salary,
        "rating": w.rating
    } for w in workers])

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.route('/login_worker', methods=['POST'])
def login_worker():
    data = request.get_json()
    worker = HouseWorker.query.filter_by(email=data['email']).first()
    if worker and worker.check_password(data['password']):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render-assigned port or fallback to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
