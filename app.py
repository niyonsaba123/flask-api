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
# app.config['SECRET_KEY'] = '17lIah6CSZu32PrMAnfxOdNFBLpDnxV4'  # Make sure to set this

# # Initialize extensions
# db.init_app(app)

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



# @app.route('/login_worker', methods=['POST'])
# def login_worker():
#     data = request.get_json()
#     print("Login attempt for email:", data['email'])
    
#     worker = HouseWorker.query.filter_by(email=data['email']).first()
#     print("Worker found:", worker is not None)
    
#     if worker:
#         print("Stored password hash:", worker.password)  # Add this line
#         print("Attempting to verify password")  # Add this line
#         password_check = check_password_hash(worker.password, data['password'])
#         print("Password check result:", password_check)  # Add this line
        
#         if password_check:
#             print("Password check passed")
#             # Generate JWT token
#             token = jwt.encode({
#                 'user_id': worker.id,
#                 'user_type': 'worker',
#                 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
#             }, app.config['SECRET_KEY'], algorithm='HS256')
            
#             return jsonify({
#                 "success": True,
#                 "message": "Login successful",
#                 "userId": str(worker.id),
#                 "token": token,
#                 "userType": "worker"
#             }), 200
    
#     print("Login failed")
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
    
#     # Only update fields that are provided in the request and not empty
#     if 'name' in data and data['name']:
#         worker.name = data['name']
    
#     # Don't update email if it's not provided or empty
#     if 'email' in data and data['email'] and data['email'] != str(worker_id):
#         # Check if the new email is already taken by another worker
#         existing_worker = HouseWorker.query.filter_by(email=data['email']).first()
#         if existing_worker and existing_worker.id != worker_id:
#             return jsonify({
#                 "success": False,
#                 "message": "Email already registered by another user",
#                 "userId": None,
#                 "token": None,
#                 "userType": None
#             }), 400
#         worker.email = data['email']
    
#     # Only update password if provided and not empty
#     if 'password' in data and data['password']:
#         worker.password = generate_sha256_hash(data['password'])
    
#     if 'phone' in data and data['phone']:
#         worker.phone = data['phone']
    
#     if 'address' in data and data['address']:
#         worker.address = data['address']
    
#     if 'expected_salary' in data and data['expected_salary']:
#         worker.expected_salary = data['expected_salary']

#     try:
#         db.session.commit()
#         return jsonify({
#             "success": True,
#             "message": "Worker updated successfully",
#             "userId": str(worker.id),
#             "userType": "worker"
#         }), 200
#     except Exception as e:
#         db.session.rollback()
#         print("Error updating worker:", str(e))  # Add logging
#         return jsonify({
#             "success": False,
#             "message": "Failed to update worker",
#             "userId": None,
#             "token": None,
#             "userType": None
#         }), 500



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






# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# import os
# import jwt
# import datetime
# from hashlib import sha256

# from models import db, HouseWorker, Employer

# app = Flask(__name__)
# CORS(app)

# # Config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_api_5p1g_user:D07HSWCyVbhNGPOxxtEmbMtU1emZyzYJ@dpg-d157g4je5dus739bj2o0-a/flask_api_5p1g'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = '17lIah6CSZu32PrMAnfxOdNFBLpDnxV4'

# # Initialize extensions
# db.init_app(app)

# # SHA-256 hash functions
# def generate_sha256_hash(password):
#     return sha256(password.encode()).hexdigest()

# def verify_sha256_hash(stored_hash, password):
#     return stored_hash == sha256(password.encode()).hexdigest()

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
#         password=generate_sha256_hash(data['password']),  # Using SHA-256
#         phone=data.get('phone', ''),
#         address=data.get('address', ''),
#         expected_salary=data.get('expected_salary', '')
#     )
#     db.session.add(new_worker)
#     db.session.commit()
    
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
#         password=generate_sha256_hash(data['password']),  # Using SHA-256
#         address=data.get('address', '')
#     )
#     db.session.add(new_employer)
#     db.session.commit()
    
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

# @app.route('/login_worker', methods=['POST'])
# def login_worker():
#     data = request.get_json()
#     print("Login attempt for email:", data['email'])
    
#     worker = HouseWorker.query.filter_by(email=data['email']).first()
#     print("Worker found:", worker is not None)
    
#     if worker:
#         print("Stored password hash:", worker.password)
#         print("Attempting to verify password")
#         password_check = verify_sha256_hash(worker.password, data['password'])  # Using SHA-256
#         print("Password check result:", password_check)
        
#         if password_check:
#             print("Password check passed")
#             token = jwt.encode({
#                 'user_id': worker.id,
#                 'user_type': 'worker',
#                 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
#             }, app.config['SECRET_KEY'], algorithm='HS256')
            
#             return jsonify({
#                 "success": True,
#                 "message": "Login successful",
#                 "userId": str(worker.id),
#                 "token": token,
#                 "userType": "worker"
#             }), 200
    
#     print("Login failed")
#     return jsonify({
#         "success": False,
#         "message": "Invalid credentials",
#         "userId": None,
#         "token": None,
#         "userType": None
#     }), 401

# @app.route('/login_employer', methods=['POST'])
# def login_employer():
#     data = request.get_json()
#     employer = Employer.query.filter_by(email=data['email']).first()
    
#     if employer and verify_sha256_hash(employer.password, data['password']):  # Using SHA-256
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
    
#     if 'name' in data and data['name']:
#         worker.name = data['name']
    
#     if 'email' in data and data['email'] and data['email'] != str(worker_id):
#         existing_worker = HouseWorker.query.filter_by(email=data['email']).first()
#         if existing_worker and existing_worker.id != worker_id:
#             return jsonify({
#                 "success": False,
#                 "message": "Email already registered by another user",
#                 "userId": None,
#                 "token": None,
#                 "userType": None
#             }), 400
#         worker.email = data['email']
    
#     if 'password' in data and data['password']:
#         worker.password = generate_sha256_hash(data['password'])  # Using SHA-256
    
#     if 'phone' in data and data['phone']:
#         worker.phone = data['phone']
    
#     if 'address' in data and data['address']:
#         worker.address = data['address']
    
#     if 'expected_salary' in data and data['expected_salary']:
#         worker.expected_salary = data['expected_salary']

#     try:
#         db.session.commit()
#         return jsonify({
#             "success": True,
#             "message": "Worker updated successfully",
#             "userId": str(worker.id),
#             "userType": "worker"
#         }), 200
#     except Exception as e:
#         db.session.rollback()
#         print("Error updating worker:", str(e))
#         return jsonify({
#             "success": False,
#             "message": "Failed to update worker",
#             "userId": None,
#             "token": None,
#             "userType": None
#         }), 500

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

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=True)










from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import jwt
import datetime
from hashlib import sha256
from functools import wraps

from models import db, HouseWorker, Employer

app = Flask(__name__)
CORS(app)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_api_5p1g_user:D07HSWCyVbhNGPOxxtEmbMtU1emZyzYJ@dpg-d157g4je5dus739bj2o0-a/flask_api_5p1g'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '17lIah6CSZu32PrMAnfxOdNFBLpDnxV4'

# Initialize extensions
db.init_app(app)

# SHA-256 hash functions
def generate_sha256_hash(password):
    return sha256(password.encode()).hexdigest()

def verify_sha256_hash(stored_hash, password):
    return stored_hash == sha256(password.encode()).hexdigest()

# Token verification decorator
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
            if current_user != 'worker':
                return jsonify({
                    "success": False,
                    "message": "Invalid user type",
                    "userId": None,
                    "token": None,
                    "userType": None
                }), 401
        except:
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
        password=generate_sha256_hash(data['password']),
        phone=data.get('phone', ''),
        address=data.get('address', ''),
        expected_salary=data.get('expected_salary', '')
    )
    db.session.add(new_worker)
    db.session.commit()
    
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
        password=generate_sha256_hash(data['password']),
        address=data.get('address', '')
    )
    db.session.add(new_employer)
    db.session.commit()
    
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


@app.route('/employer/profile/<int:id>', methods=['GET'])
def get_employer_profile(id):
    employer = Employer.query.get(id)
    if not employer:
        return jsonify({
            "message": "Employer not found",
            "success": False
        }), 404
    return jsonify({
        "employer": {
            "id": employer.id,
            "name": employer.name,
            "email": employer.email,
            # "phone": employer.phone
        },
        "success": True
    }), 200



@app.route('/employer/workers', methods=['GET'])
def get_all_workers_for_employer():
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
            "rating": getattr(worker, 'rating', None)  # Use getattr in case some workers don't have a rating yet
        })
    return jsonify(worker_list), 200


@app.route('/hire_worker/<int:worker_id>', methods=['POST'])
def hire_worker(worker_id):
    data = request.get_json()
    employer_email = data.get('employer_email')
    worker = HouseWorker.query.get(worker_id)
    if not worker:
        return jsonify({"success": False, "message": "Worker not found"}), 404
    if worker.status == "hired":
        return jsonify({"success": False, "message": "Worker already hired"}), 400
    worker.status = "hired"
    worker.boss = employer_email
    db.session.commit()
    return jsonify({"success": True, "message": "Worker hired successfully"}), 200





@app.route('/login_worker', methods=['POST'])
def login_worker():
    data = request.get_json()
    print("Login attempt for email:", data['email'])
    
    worker = HouseWorker.query.filter_by(email=data['email']).first()
    print("Worker found:", worker is not None)
    
    if worker:
        print("Stored password hash:", worker.password)
        print("Attempting to verify password")
        password_check = verify_sha256_hash(worker.password, data['password'])
        print("Password check result:", password_check)
        
        if password_check:
            print("Password check passed")
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

@app.route('/login_employer', methods=['POST'])
def login_employer():
    data = request.get_json()
    employer = Employer.query.filter_by(email=data['email']).first()
    
    if employer and verify_sha256_hash(employer.password, data['password']):
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

# @app.route('/workers', methods=['GET'])
# @token_required
# def get_workers():
#     workers = HouseWorker.query.all()
#     return jsonify([{
#         "id": w.id,
#         "name": w.name,
#         "email": w.email,
#         "phone": w.phone,
#         "address": w.address,
#         "expected_salary": w.expected_salary,
#         "userType": "worker"
#     } for w in workers]), 200


@app.route('/workers', methods=['GET'])
@token_required
def get_workers():
    workers = HouseWorker.query.all()
    return jsonify([{
        "id": w.id,
        "name": w.name,
        "email": w.email,
        "phone": w.phone,
        "address": w.address,
        "expected_salary": w.expected_salary,
        "status": w.status,
        "boss": w.boss,
        "userType": "worker"
    } for w in workers]), 200



@app.route('/worker/<id>', methods=['GET'])
@token_required
def get_worker_by_id(id):
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
        "id": worker.id,
        "name": worker.name,
        "email": worker.email,
        "phone": worker.phone,
        "address": worker.address,
        "expected_salary": worker.expected_salary,
        "userType": "worker"
    }), 200

@app.route('/workers/<int:worker_id>', methods=['PUT'])
@token_required
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
    
    if 'name' in data and data['name']:
        worker.name = data['name']
    
    if 'email' in data and data['email'] and data['email'] != str(worker_id):
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
    
    if 'password' in data and data['password']:
        worker.password = generate_sha256_hash(data['password'])
    
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
            "userType": "worker",
            "token": None
        }), 200
    except Exception as e:
        db.session.rollback()
        print("Error updating worker:", str(e))
        return jsonify({
            "success": False,
            "message": "Failed to update worker",
            "userId": None,
            "token": None,
            "userType": None
        }), 500

@app.route('/workers/<int:worker_id>', methods=['DELETE'])
@token_required
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
        "userType": "worker",
        "token": None
    }), 200


@app.route('/employer/profile/<int:id>', methods=['PUT', 'POST'])
def update_employer_profile(id):
    employer = Employer.query.get(id)
    if not employer:
        return jsonify({
            "success": False,
            "message": "Employer not found"
        }), 404

    data = request.get_json()
    # Update fields if present in the request
    if 'name' in data and data['name']:
        employer.name = data['name']
    if 'email' in data and data['email']:
        # Optional: check for duplicate email
        existing = Employer.query.filter_by(email=data['email']).first()
        if existing and existing.id != id:
            return jsonify({
                "success": False,
                "message": "Email already registered by another employer"
            }), 400
        employer.email = data['email']
    if 'address' in data and data['address']:
        employer.address = data['address']
    # Add more fields as needed (e.g., phone) if your Employer model supports them

    try:
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Employer updated successfully",
            "employer": {
                "id": employer.id,
                "name": employer.name,
                "email": employer.email,
                "address": employer.address
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Failed to update employer"
        }), 500


@app.route('/employer/profile/<int:id>', methods=['DELETE'])
def delete_employer_profile(id):
    employer = Employer.query.get(id)
    if not employer:
        return jsonify({
            "success": False,
            "message": "Employer not found"
        }), 404

    try:
        db.session.delete(employer)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Employer deleted successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Failed to delete employer"
        }), 500




@app.route('/api/employers/<int:employer_id>/available_workers', methods=['GET'])
def get_available_workers(employer_id):
    workers = HouseWorker.query.filter_by(status='available').all()
    return jsonify([w.to_dict() for w in workers])


@app.route('/api/employers/<int:employer_id>/hired_workers', methods=['GET'])
def get_hired_workers(employer_id):
    offers = JobOffer.query.filter_by(employer_id=employer_id, status='accepted').all()
    workers = [offer.worker.to_dict() for offer in offers]
    return jsonify(workers)


@app.route('/api/employers/<int:employer_id>/offer', methods=['POST'])
def create_job_offer(employer_id):
    data = request.json
    worker_id = data.get('worker_id')
    offer = JobOffer(employer_id=employer_id, worker_id=worker_id)
    db.session.add(offer)
    db.session.commit()
    return jsonify({'success': True, 'offer_id': offer.id})


@app.route('/api/workers/<int:worker_id>/offers', methods=['GET'])
def get_worker_offers(worker_id):
    offers = JobOffer.query.filter_by(worker_id=worker_id).all()
    return jsonify([o.to_dict() for o in offers])


@app.route('/api/workers/<int:worker_id>/accept_offer', methods=['POST'])
def accept_offer(worker_id):
    data = request.json
    offer_id = data.get('offer_id')
    offer = JobOffer.query.get(offer_id)
    if offer and offer.worker_id == worker_id:
        offer.status = 'accepted'
        offer.updated_at = datetime.utcnow()
        # Optionally update worker status
        worker = HouseWorker.query.get(worker_id)
        worker.status = 'hired'
        worker.boss = offer.employer_id
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Offer not found or unauthorized'}), 404


@app.route('/api/workers/<int:worker_id>/leave_job', methods=['POST'])
def leave_job(worker_id):
    data = request.json
    offer_id = data.get('offer_id')
    rating = data.get('rating')
    offer = JobOffer.query.get(offer_id)
    if offer and offer.worker_id == worker_id and offer.status == 'accepted':
        offer.status = 'completed'
        offer.rating = rating
        offer.updated_at = datetime.utcnow()
        # Update worker status and rating
        worker = HouseWorker.query.get(worker_id)
        worker.status = 'available'
        # Optionally, update worker's average rating
        ratings = [o.rating for o in worker.job_offers if o.rating is not None]
        if ratings:
            worker.rating = sum(ratings) / len(ratings)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Offer not found or unauthorized'}), 404





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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
