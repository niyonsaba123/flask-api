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

# Models
class Employer(db.Model):
    __tablename__ = 'employers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    address = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address
        }

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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "expected_salary": self.expected_salary,
            "rating": self.rating,
            "status": self.status,
            "boss": self.boss
        }

class JobOffer(db.Model):
    __tablename__ = 'job_offers'
    
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'))
    worker_id = db.Column(db.Integer, db.ForeignKey('house_workers.id'))
    status = db.Column(db.String(20), default='pending')
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    employer = db.relationship('Employer', backref='offers')
    worker = db.relationship('HouseWorker', backref='offers')

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

def make_response(success=True, message="", data=None, status_code=200, token=None, user_type=None):
    response = {
        "success": success,
        "message": message,
        "userType": user_type,
        "token": token
    }
    if data:
        response.update(data)
    return jsonify(response), status_code

def make_error_response(message="", status_code=400):
    return make_response(False, message, None, status_code)

def get_user_from_token():
    token = None
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
    if not token:
        return None
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if data['user_type'] == 'worker':
            return HouseWorker.query.get(data['user_id'])
        else:
            return Employer.query.get(data['user_id'])
    except:
        return None

# Auth Routes
@app.route('/register/<user_type>', methods=['POST'])
def register(user_type):
    data = request.get_json()
    
    if user_type == 'worker':
        model = HouseWorker
    elif user_type == 'employer':
        model = Employer
    else:
        return make_error_response("Invalid user type", 400)

    if model.query.filter_by(email=data['email']).first():
        return make_error_response("Email already registered", 400)

    new_user = model(
        name=data['name'],
        email=data['email'],
        password=generate_sha256_hash(data['password']),
        address=data.get('address', '')
    )
    
    if user_type == 'worker':
        new_user.phone = data.get('phone', '')
        new_user.expected_salary = data.get('expected_salary', '')

    db.session.add(new_user)
    db.session.commit()
    
    token = generate_token(new_user.id, user_type)
    return make_response(
        message=f"{user_type.capitalize()} registered successfully",
        data={"userId": new_user.id},
        token=token,
        user_type=user_type,
        status_code=201
    )

@app.route('/login/<user_type>', methods=['POST'])
def login(user_type):
    data = request.get_json()
    
    if user_type == 'worker':
        user = HouseWorker.query.filter_by(email=data['email']).first()
    elif user_type == 'employer':
        user = Employer.query.filter_by(email=data['email']).first()
    else:
        return make_error_response("Invalid user type", 400)
    
    if user and verify_sha256_hash(user.password, data['password']):
        token = generate_token(user.id, user_type)
        return make_response(
            message="Login successful",
            data={"userId": user.id},
            token=token,
            user_type=user_type
        )
    
    return make_error_response("Invalid credentials", 401)

# Profile Routes
@app.route('/<user_type>/profile', methods=['GET', 'PUT', 'DELETE'])
def profile_operations(user_type):
    user = get_user_from_token()
    if not user:
        return make_error_response("Unauthorized", 401)
    
    if request.method == 'GET':
        return make_response(data={"profile": user.to_dict()})
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            if user_type == 'worker' and HouseWorker.query.filter_by(email=data['email']).first():
                return make_error_response("Email already in use", 400)
            elif user_type == 'employer' and Employer.query.filter_by(email=data['email']).first():
                return make_error_response("Email already in use", 400)
            user.email = data['email']
        if 'password' in data:
            user.password = generate_sha256_hash(data['password'])
        if 'address' in data:
            user.address = data['address']
        if user_type == 'worker':
            if 'phone' in data:
                user.phone = data['phone']
            if 'expected_salary' in data:
                user.expected_salary = data['expected_salary']
        
        db.session.commit()
        return make_response(message="Profile updated successfully")
    
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return make_response(message="Account deleted successfully")

# Worker Management Routes
@app.route('/workers/available', methods=['GET'])
def available_workers():
    user = get_user_from_token()
    if not user or not isinstance(user, Employer):
        return make_error_response("Unauthorized", 401)
    
    workers = HouseWorker.query.filter_by(status='available').all()
    return make_response(data={"workers": [w.to_dict() for w in workers]})

@app.route('/workers/hired', methods=['GET'])
def hired_workers():
    user = get_user_from_token()
    if not user or not isinstance(user, Employer):
        return make_error_response("Unauthorized", 401)
    
    workers = HouseWorker.query.filter_by(boss=user.email, status='hired').all()
    return make_response(data={"workers": [w.to_dict() for w in workers]})

@app.route('/workers/hire/<int:worker_id>', methods=['POST'])
def hire_worker(worker_id):
    employer = get_user_from_token()
    if not employer or not isinstance(employer, Employer):
        return make_error_response("Unauthorized", 401)
    
    worker = HouseWorker.query.get(worker_id)
    if not worker:
        return make_error_response("Worker not found", 404)
    if worker.status == "hired":
        return make_error_response("Worker already hired", 400)
    
    # Create job offer
    offer = JobOffer(
        employer_id=employer.id,
        worker_id=worker.id,
        status='accepted'
    )
    
    # Update worker status
    worker.status = "hired"
    worker.boss = employer.email
    
    db.session.add(offer)
    db.session.commit()
    
    return make_response(message="Worker hired successfully")

@app.route('/workers/offers', methods=['GET'])
def get_worker_offers():
    worker = get_user_from_token()
    if not worker or not isinstance(worker, HouseWorker):
        return make_error_response("Unauthorized", 401)
    
    offers = JobOffer.query.filter_by(worker_id=worker.id).all()
    return make_response(data={"offers": [{
        "id": o.id,
        "employer": o.employer.to_dict(),
        "status": o.status,
        "created_at": o.created_at.isoformat() if o.created_at else None
    } for o in offers]})

@app.route('/workers/accept_offer/<int:offer_id>', methods=['POST'])
def accept_offer(offer_id):
    worker = get_user_from_token()
    if not worker or not isinstance(worker, HouseWorker):
        return make_error_response("Unauthorized", 401)
    
    offer = JobOffer.query.get(offer_id)
    if not offer or offer.worker_id != worker.id:
        return make_error_response("Offer not found", 404)
    
    offer.status = 'accepted'
    worker.status = 'hired'
    worker.boss = offer.employer.email
    db.session.commit()
    
    return make_response(message="Offer accepted successfully")

@app.route('/workers/complete_job', methods=['POST'])
def complete_job():
    worker = get_user_from_token()
    if not worker or not isinstance(worker, HouseWorker) or worker.status != 'hired':
        return make_error_response("Unauthorized", 401)
    
    data = request.get_json()
    rating = data.get('rating')
    
    # Find the active job offer
    offer = JobOffer.query.filter_by(
        worker_id=worker.id,
        status='accepted'
    ).first()
    
    if not offer:
        return make_error_response("No active job found", 400)
    
    # Update offer and worker status
    offer.status = 'completed'
    offer.rating = rating
    offer.updated_at = datetime.datetime.utcnow()
    
    worker.status = 'available'
    worker.boss = None
    
    # Update worker rating
    if rating:
        completed_offers = JobOffer.query.filter_by(
            worker_id=worker.id,
            status='completed'
        ).all()
        ratings = [o.rating for o in completed_offers if o.rating]
        if ratings:
            worker.rating = sum(ratings) / len(ratings)
    
    db.session.commit()
    return make_response(message="Job completed successfully")

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
