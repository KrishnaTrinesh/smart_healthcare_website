from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
import bcrypt
from datetime import datetime
from bson import ObjectId

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ('email', 'password', 'full_name')):
            return jsonify({'message': 'Missing required fields'}), 400
        
        users = current_app.mongo['users']
        # Check if user already exists
        if users.find_one({'email': data['email']}):
            return jsonify({'message': 'User already exists'}), 400
        
        # Hash password
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create new user document
        user_doc = {
            'email': data['email'],
            'password': hashed_password,
            'full_name': data['full_name'],
            'phone': data.get('phone'),
            'date_of_birth': data.get('date_of_birth'),
            'created_at': datetime.utcnow()
        }
        result = users.insert_one(user_doc)
        user_doc['_id'] = str(result.inserted_id)
        
        # Create access token with string subject (email) and role as additional claim
        access_token = create_access_token(identity=user_doc['email'], additional_claims={'role': 'user'})
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user_doc['_id'],
                'email': user_doc['email'],
                'full_name': user_doc['full_name'],
                'phone': user_doc.get('phone'),
                'date_of_birth': user_doc.get('date_of_birth'),
                'created_at': user_doc['created_at'].isoformat()
            },
            'access_token': access_token
        }), 201
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        role = data.get('role', 'user')  # user, doctor, admin
        
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({'message': 'Missing required fields'}), 400
        
        users = current_app.mongo['users']
        doctors = current_app.mongo['doctors']
        if role == 'user':
            user = users.find_one({'email': data['email']})
            if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
                return jsonify({'message': 'Invalid credentials'}), 401
            user_data = {
                'id': str(user['_id']),
                'email': user['email'],
                'full_name': user.get('full_name'),
                'phone': user.get('phone'),
                'date_of_birth': user.get('date_of_birth'),
            }
            user_type = 'user'
        elif role == 'doctor':
            doctor = doctors.find_one({'email': data['email']})
            if not doctor or not bcrypt.checkpw(data['password'].encode('utf-8'), doctor['password'].encode('utf-8')):
                return jsonify({'message': 'Invalid credentials'}), 401
            user_data = {
                'id': str(doctor['_id']),
                'email': doctor['email'],
                'name': doctor.get('name'),
                'specialty': doctor.get('specialty'),
                'phone': doctor.get('phone'),
                'experience': doctor.get('experience'),
                'rating': doctor.get('rating', 0.0),
                'availability': doctor.get('availability'),
            }
            user_type = 'doctor'
        else:
            return jsonify({'message': 'Invalid role'}), 400
        
        # Create access token with string subject (email) and role as additional claim
        access_token = create_access_token(identity=data['email'], additional_claims={'role': user_type})
        
        return jsonify({
            'message': 'Login successful',
            'user': user_data,
            'access_token': access_token,
            'role': user_type
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
