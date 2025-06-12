# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from werkzeug.security import generate_password_hash, check_password_hash
# import os
# import jwt
# import datetime

# from models import db, HouseWorker, Employer

# app = Flask(__name__)
# CORS(app)

# # Config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_api_5p1g_user:D07HSWCyVbhNGPOxxtEmbMtU1emZyzYJ@dpg-d157g4je5dus739bj2o0-a/flask_api_5p1g'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key

# # Initialize extensions
# db.init_app(app)

# # with app.app_context():
# #     db.create_all()

# @app.route('/')
# def index():
#     return jsonify({"message": "Flask API with Postgres is running!"})

# # Register a house worker
# @app.route('/register_worker', methods=['POST'])
# def register_worker():
#     data = request.get_json()
#     if HouseWorker.query.filter_by(email=data['email']).first():
#         return jsonify({
#             "success": False,
#             "message": "Email already registered",
#             "userId": None,
#             "token": None,
#             "userType": None
#         }), 400

#     new_worker = HouseWorker(
#         name=data['name'],
#         email=data['email'],
#         password=generate_password_hash(data['password']),
#         phone=data.get('phone', ''),
#         address=data.get('address', ''),
#         expected_salary=data.get('expected_salary', '')
#     )
#     db.session.add(new_worker)
#     db.session.commit()
    
#     # Generate token for new worker
#     token = jwt.encode({
#         'user_id': new_worker.id,
#         'user_type': 'worker',
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
#     }, app.config['SECRET_KEY'], algorithm='HS256')
    
#     return jsonify({
#         "success": True,
#         "message": "House worker registered successfully",
#         "userId": str(new_worker.id),
#         "token": token,
#         "userType": "worker"
#     }), 201


# # Register an employer
# @app.route('/register_employer', methods=['POST'])
# def register_employer():
#     data = request.get_json()
#     if Employer.query.filter_by(email=data['email']).first():
#         return jsonify({
#             "success": False,
#             "message": "Email already registered",
#             "userId": None,
#             "token": None,
#             "userType": None
#         }), 400

#     new_employer = Employer(
#         name=data['name'],
#         email=data['email'],
#         password=generate_password_hash(data['password']),
#         address=data.get('address', '')
#     )
#     db.session.add(new_employer)
#     db.session.commit()
    
#     # Generate token for new employer
#     token = jwt.encode({
#         'user_id': new_employer.id,
#         'user_type': 'employer',
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
#     }, app.config['SECRET_KEY'], algorithm='HS256')
    
#     return jsonify({
#         "success": True,
#         "message": "Employer registered successfully",
#         "userId": str(new_employer.id),
#         "token": token,
#         "userType": "employer"
#     }), 201

# # Login for house worker
# @app.route('/login_worker', methods=['POST'])
# def login_worker():
#     data = request.get_json()
#     worker = HouseWorker.query.filter_by(email=data['email']).first()
    
#     if worker and check_password_hash(worker.password, data['password']):
#         # Generate JWT token
#         token = jwt.encode({
#             'user_id': worker.id,
#             'user_type': 'worker',
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
#         }, app.config['SECRET_KEY'], algorithm='HS256')
        
#         return jsonify({
#             "success": True,
#             "message": "Login successful",
#             "userId": str(worker.id),
#             "token": token,
#             "userType": "worker"
#         }), 200
    
#     return jsonify({
#         "success": False,
#         "message": "Invalid credentials",
#         "userId": None,
#         "token": None,
#         "userType": None
#     }), 401

# # Login for employer
# @app.route('/login_employer', methods=['POST'])
# def login_employer():
#     data = request.get_json()
#     employer = Employer.query.filter_by(email=data['email']).first()
    
#     if employer and check_password_hash(employer.password, data['password']):
#         # Generate JWT token
#         token = jwt.encode({
#             'user_id': employer.id,
#             'user_type': 'employer',
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
#         }, app.config['SECRET_KEY'], algorithm='HS256')
        
#         return jsonify({
#             "success": True,
#             "message": "Login successful",
#             "userId": str(employer.id),
#             "token": token,
#             "userType": "employer"
#         }), 200
    
#     return jsonify({
#         "success": False,
#         "message": "Invalid credentials",
#         "userId": None,
#         "token": None,
#         "userType": None
#     }), 401

# # Get list of all house workers
# @app.route('/workers', methods=['GET'])
# def get_workers():
#     workers = HouseWorker.query.all()
#     return jsonify([{
#         "id": w.id,
#         "name": w.name,
#         "email": w.email,
#         "phone": w.phone,
#         "address": w.address,
#         "expected_salary": w.expected_salary
#     } for w in workers]), 200

# # Update a house worker
# @app.route('/workers/<int:worker_id>', methods=['PUT'])
# def update_worker(worker_id):
#     data = request.get_json()
#     worker = HouseWorker.query.get(worker_id)
#     if not worker:
#         return jsonify({
#             "success": False,
#             "message": "Worker not found",
#             "userId": None,
#             "token": None,
#             "userType": None
#         }), 404
        
#     worker.name = data.get('name', worker.name)
#     worker.email = data.get('email', worker.email)
#     if 'password' in data:
#         worker.password = generate_password_hash(data['password'])
#     worker.phone = data.get('phone', worker.phone)
#     worker.address = data.get('address', worker.address)
#     worker.expected_salary = data.get('expected_salary', worker.expected_salary)

#     db.session.commit()
#     return jsonify({
#         "success": True,
#         "message": "Worker updated successfully",
#         "userId": str(worker.id),
#         "userType": "worker"
#     }), 200

# # Delete a house worker
# @app.route('/workers/<int:worker_id>', methods=['DELETE'])
# def delete_worker(worker_id):
#     worker = HouseWorker.query.get(worker_id)
#     if not worker:
#         return jsonify({
#             "success": False,
#             "message": "Worker not found",
#             "userId": None,
#             "token": None,
#             "userType": None
#         }), 404
    
#     db.session.delete(worker)
#     db.session.commit()
#     return jsonify({
#         "success": True,
#         "message": "Worker deleted successfully",
#         "userId": str(worker_id),
#         "userType": "worker"
#     }), 200


# # Get a specific worker by ID
# @app.route('/worker/<id>', methods=['GET'])
# def get_worker_by_id(id):
#     worker = HouseWorker.query.get(id)
#     if not worker:
#         return jsonify({
#             "success": False,
#             "message": "Worker not found"
#         }), 404
    
#     return jsonify({
#         "id": worker.id,
#         "name": worker.name,
#         "email": worker.email,
#         "phone": worker.phone,
#         "address": worker.address,
#         "expected_salary": worker.expected_salary
#     }), 200


# # Error handlers
# @app.errorhandler(400)
# def bad_request(error):
#     return jsonify({
#         "success": False,
#         "message": "Bad request",
#         "userId": None,
#         "token": None,
#         "userType": None
#     }), 400

# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({
#         "success": False,
#         "message": "Resource not found",
#         "userId": None,
#         "token": None,
#         "userType": None
#     }), 404
    
# # Run the app
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))  # Use Render-assigned port or fallback to 5000
#     app.run(host='0.0.0.0', port=port, debug=True)



from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import jwt
import datetime

from models import db, HouseWorker, Employer

app = Flask(__name__)
CORS(app)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_api_5p1g_user:D07HSWCyVbhNGPOxxtEmbMtU1emZyzYJ@dpg-d157g4je5dus739bj2o0-a/flask_api_5p1g'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '17lIah6CSZu32PrMAnfxOdNFBLpDnxV4'  # Make sure to set this

# Initialize extensions
db.init_app(app)

@app.route('/')
def index():
    return jsonify({"message": "Flask API with Postgres is running!"})

# Register a house worker
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
        password=generate_password_hash(data['password']),
        phone=data.get('phone', ''),
        address=data.get('address', ''),
        expected_salary=data.get('expected_salary', '')
    )
    db.session.add(new_worker)
    db.session.commit()
    
    # Generate token for new worker
    token = jwt.encode({
        'user_id': new_worker.id,
        'user_type': 'worker',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        "success": True,
        "message": "House worker registered successfully",
        "userId": str(new_worker.id),
        "token": token,
        "userType": "worker"
    }), 201

# Register an employer
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
        password=generate_password_hash(data['password']),
        address=data.get('address', '')
    )
    db.session.add(new_employer)
    db.session.commit()
    
    # Generate token for new employer
    token = jwt.encode({
        'user_id': new_employer.id,
        'user_type': 'employer',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
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
    print("Login attempt for email:", data['email'])
    
    worker = HouseWorker.query.filter_by(email=data['email']).first()
    print("Worker found:", worker is not None)
    
    if worker:
        print("Stored password hash:", worker.password)  # Add this line
        print("Attempting to verify password")  # Add this line
        password_check = check_password_hash(worker.password, data['password'])
        print("Password check result:", password_check)  # Add this line
        
        if password_check:
            print("Password check passed")
            # Generate JWT token
            token = jwt.encode({
                'user_id': worker.id,
                'user_type': 'worker',
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            return jsonify({
                "success": True,
                "message": "Login successful",
                "userId": str(worker.id),
                "token": token,
                "userType": "worker"
            }), 200
    
    print("Login failed")
    return jsonify({
        "success": False,
        "message": "Invalid credentials",
        "userId": None,
        "token": None,
        "userType": None
    }), 401




# Login for employer
@app.route('/login_employer', methods=['POST'])
def login_employer():
    data = request.get_json()
    employer = Employer.query.filter_by(email=data['email']).first()
    
    if employer and check_password_hash(employer.password, data['password']):
        # Generate JWT token
        token = jwt.encode({
            'user_id': employer.id,
            'user_type': 'employer',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
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

# Update a house worker

@app.route('/workers/<int:worker_id>', methods=['PUT'])
def update_worker(worker_id):
    data = request.get_json()
    worker = HouseWorker.query.get(worker_id)
    if not worker:
        return jsonify({
            "success": False,
            "message": "Worker not found",
            "userId": None,
            "token": None,
            "userType": None
        }), 404
    
    # Only update fields that are provided in the request and not empty
    if 'name' in data and data['name']:
        worker.name = data['name']
    
    # Don't update email if it's not provided or empty
    if 'email' in data and data['email'] and data['email'] != str(worker_id):
        # Check if the new email is already taken by another worker
        existing_worker = HouseWorker.query.filter_by(email=data['email']).first()
        if existing_worker and existing_worker.id != worker_id:
            return jsonify({
                "success": False,
                "message": "Email already registered by another user",
                "userId": None,
                "token": None,
                "userType": None
            }), 400
        worker.email = data['email']
    
    # Only update password if provided and not empty
    if 'password' in data and data['password']:
        worker.password = generate_password_hash(data['password'])
    
    if 'phone' in data and data['phone']:
        worker.phone = data['phone']
    
    if 'address' in data and data['address']:
        worker.address = data['address']
    
    if 'expected_salary' in data and data['expected_salary']:
        worker.expected_salary = data['expected_salary']

    try:
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Worker updated successfully",
            "userId": str(worker.id),
            "userType": "worker"
        }), 200
    except Exception as e:
        db.session.rollback()
        print("Error updating worker:", str(e))  # Add logging
        return jsonify({
            "success": False,
            "message": "Failed to update worker",
            "userId": None,
            "token": None,
            "userType": None
        }), 500



# Delete a house worker
@app.route('/workers/<int:worker_id>', methods=['DELETE'])
def delete_worker(worker_id):
    worker = HouseWorker.query.get(worker_id)
    if not worker:
        return jsonify({
            "success": False,
            "message": "Worker not found",
            "userId": None,
            "token": None,
            "userType": None
        }), 404
    
    db.session.delete(worker)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Worker deleted successfully",
        "userId": str(worker_id),
        "userType": "worker"
    }), 200

# Get a specific worker by ID
@app.route('/worker/<id>', methods=['GET'])
def get_worker_by_id(id):
    worker = HouseWorker.query.get(id)
    if not worker:
        return jsonify({
            "success": False,
            "message": "Worker not found"
        }), 404
    
    return jsonify({
        "id": worker.id,
        "name": worker.name,
        "email": worker.email,
        "phone": worker.phone,
        "address": worker.address,
        "expected_salary": worker.expected_salary
    }), 200

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "message": "Bad request",
        "userId": None,
        "token": None,
        "userType": None
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "message": "Resource not found",
        "userId": None,
        "token": None,
        "userType": None
    }), 404
    
# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render-assigned port or fallback to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
