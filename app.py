from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import jwt
import datetime
from hashlib import sha256
from functools import wraps

app = Flask(__name__)
CORS(app)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_api_5p1g_user:D07HSWCyVbhNGPOxxtEmbMtU1emZyzYJ@dpg-d157g4je5dus739bj2o0-a/flask_api_5p1g'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '17lIah6CSZu32PrMAnfxOdNFBLpDnxV4'

db = SQLAlchemy(app)

# Models matching your database tables exactly
class Employer(db.Model):
    __tablename__ = 'employers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    address = db.Column(db.String(200))

class HouseWorker(db.Model):
    __tablename__ = 'house_workers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    expected_salary = db.Column(db.String(50))
    rating = db.Column(db.Float)
    status = db.Column(db.String(32), default='available')
    boss = db.Column(db.String(128))

# Helper Functions
def generate_sha256_hash(password):
    return sha256(password.encode()).hexdigest()

def verify_sha256_hash(stored_hash, password):
    return stored_hash == sha256(password.encode()).hexdigest()

def generate_token(user_id, user_type):
    return jwt.encode({
        'user_id': user_id,
        'user_type': user_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({
                "success": False,
                "message": "Token is missing",
                "userId": None,
                "token": None,
                "userType": None
            }), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user_type']
            if current_user not in ['worker', 'employer']:
                return jsonify({
                    "success": False,
                    "message": "Invalid user type",
                    "userId": None,
                    "token": None,
                    "userType": None
                }), 401
            kwargs['user_id'] = data['user_id']
            kwargs['user_type'] = data['user_type']
        except Exception as e:
            return jsonify({
                "success": False,
                "message": "Token is invalid",
                "userId": None,
                "token": None,
                "userType": None
            }), 401
            
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return jsonify({"message": "Flask API with Postgres is running!"})

# Auth Routes
@app.route('/register_worker', methods=['POST'])
def register_worker():
    data = request.get_json()
    if HouseWorker.query.filter_by(email=data['email']).first():
        return jsonify({
            "success": False,
            "message": "Email already registered",
            "userId": None,
            "token": None,
            "userType": None
        }), 400

    new_worker = HouseWorker(
        name=data['name'],
        email=data['email'],
        password=generate_sha256_hash(data['password']),
        phone=data.get('phone', ''),
        address=data.get('address', ''),
        expected_salary=data.get('expected_salary', '')
    )
    db.session.add(new_worker)
    db.session.commit()
    
    token = generate_token(new_worker.id, 'worker')
    return jsonify({
        "success": True,
        "message": "House worker registered successfully",
        "userId": str(new_worker.id),
        "token": token,
        "userType": "worker"
    }), 201

@app.route('/register_employer', methods=['POST'])
def register_employer():
    data = request.get_json()
    if Employer.query.filter_by(email=data['email']).first():
        return jsonify({
            "success": False,
            "message": "Email already registered",
            "userId": None,
            "token": None,
            "userType": None
        }), 400

    new_employer = Employer(
        name=data['name'],
        email=data['email'],
        password=generate_sha256_hash(data['password']),
        address=data.get('address', '')
    )
    db.session.add(new_employer)
    db.session.commit()
    
    token = generate_token(new_employer.id, 'employer')
    return jsonify({
        "success": True,
        "message": "Employer registered successfully",
        "userId": str(new_employer.id),
        "token": token,
        "userType": "employer"
    }), 201

@app.route('/login_worker', methods=['POST'])
def login_worker():
    data = request.get_json()
    worker = HouseWorker.query.filter_by(email=data['email']).first()
    
    if worker and verify_sha256_hash(worker.password, data['password']):
        token = generate_token(worker.id, 'worker')
        return jsonify({
            "success": True,
            "message": "Login successful",
            "userId": str(worker.id),
            "token": token,
            "userType": "worker"
        }), 200
    
    return jsonify({
        "success": False,
        "message": "Invalid credentials",
        "userId": None,
        "token": None,
        "userType": None
    }), 401

@app.route('/login_employer', methods=['POST'])
def login_employer():
    data = request.get_json()
    employer = Employer.query.filter_by(email=data['email']).first()
    
    if employer and verify_sha256_hash(employer.password, data['password']):
        token = generate_token(employer.id, 'employer')
        return jsonify({
            "success": True,
            "message": "Login successful",
            "userId": str(employer.id),
            "token": token,
            "userType": "employer"
        }), 200
    
    return jsonify({
        "success": False,
        "message": "Invalid credentials",
        "userId": None,
        "token": None,
        "userType": None
    }), 401

# Profile Routes
@app.route('/employer/profile/<int:id>', methods=['GET'])
@token_required
def get_employer_profile(id, user_id, user_type):
    if user_type != 'employer' or str(id) != str(user_id):
        return jsonify({
            "success": False,
            "message": "Unauthorized",
            "userId": None,
            "token": None,
            "userType": None
        }), 401
    
    employer = Employer.query.get(id)
    if not employer:
        return jsonify({
            "success": False,
            "message": "Employer not found",
            "userId": None,
            "token": None,
            "userType": None
        }), 404
    
    return jsonify({
        "success": True,
        "employer": {
            "id": employer.id,
            "name": employer.name,
            "email": employer.email,
            "address": employer.address
        }
    }), 200

@app.route('/worker/profile/<int:id>', methods=['GET'])
@token_required
def get_worker_profile(id, user_id, user_type):
    if user_type != 'worker' or str(id) != str(user_id):
        return jsonify({
            "success": False,
            "message": "Unauthorized",
            "userId": None,
            "token": None,
            "userType": None
        }), 401
    
    worker = HouseWorker.query.get(id)
    if not worker:
        return jsonify({
            "success": False,
            "message": "Worker not found",
            "userId": None,
            "token": None,
            "userType": None
        }), 404
    
    return jsonify({
        "success": True,
        "worker": {
            "id": worker.id,
            "name": worker.name,
            "email": worker.email,
            "phone": worker.phone,
            "address": worker.address,
            "expected_salary": worker.expected_salary,
            "status": worker.status,
            "boss": worker.boss,
            "rating": worker.rating
        }
    }), 200

# Worker Management Routes
@app.route('/workers', methods=['GET'])
@token_required
def get_all_workers(user_id, user_type):
    workers = HouseWorker.query.all()
    worker_list = []
    for worker in workers:
        worker_list.append({
            "id": worker.id,
            "name": worker.name,
            "email": worker.email,
            "phone": worker.phone,
            "address": worker.address,
            "expected_salary": worker.expected_salary,
            "status": worker.status,
            "boss": worker.boss,
            "rating": worker.rating
        })
    return jsonify(worker_list), 200

@app.route('/workers/available', methods=['GET'])
@token_required
def get_available_workers(user_id, user_type):
    if user_type != 'employer':
        return jsonify({
            "success": False,
            "message": "Unauthorized",
            "userId": None,
            "token": None,
            "userType": None
        }), 401
    
    workers = HouseWorker.query.filter_by(status='available').all()
    return jsonify([w.to_dict() for w in workers]), 200

@app.route('/workers/hired', methods=['GET'])
@token_required
def get_hired_workers(user_id, user_type):
    if user_type != 'employer':
        return jsonify({
            "success": False,
            "message": "Unauthorized",
            "userId": None,
            "token": None,
            "userType": None
        }), 401
    
    employer = Employer.query.get(user_id)
    if not employer:
        return jsonify({
            "success": False,
            "message": "Employer not found",
            "userId": None,
            "token": None,
            "userType": None
        }), 404
    
    workers = HouseWorker.query.filter_by(boss=employer.email, status='hired').all()
    return jsonify([w.to_dict() for w in workers]), 200

@app.route('/hire_worker/<int:worker_id>', methods=['POST'])
@token_required
def hire_worker(worker_id, user_id, user_type):
    if user_type != 'employer':
        return jsonify({
            "success": False,
            "message": "Unauthorized",
            "userId": None,
            "token": None,
            "userType": None
        }), 401
    
    employer = Employer.query.get(user_id)
    if not employer:
        return jsonify({
            "success": False,
            "message": "Employer not found",
            "userId": None,
            "token": None,
            "userType": None
        }), 404
    
    worker = HouseWorker.query.get(worker_id)
    if not worker:
        return jsonify({
            "success": False,
            "message": "Worker not found",
            "userId": None,
            "token": None,
            "userType": None
        }), 404
    
    if worker.status == "hired":
        return jsonify({
            "success": False,
            "message": "Worker already hired",
            "userId": None,
            "token": None,
            "userType": None
        }), 400
    
    worker.status = "hired"
    worker.boss = employer.email
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Worker hired successfully"
    }), 200

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
