from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import json
from bson import ObjectId

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/doctors', methods=['GET'])
def get_doctors():
    try:
        specialty = request.args.get('specialty')
        doctors_col = current_app.mongo['doctors']
        query = {}
        if specialty:
            query['specialty'] = specialty
        doctors = list(doctors_col.find(query))
        return jsonify({
            'doctors': [{
                'id': str(doc['_id']),
                'email': doc.get('email'),
                'name': doc.get('name'),
                'specialty': doc.get('specialty'),
                'phone': doc.get('phone'),
                'experience': doc.get('experience'),
                'rating': doc.get('rating', 0.0),
                'availability': doc.get('availability'),
            } for doc in doctors]
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@booking_bp.route('/create', methods=['POST'])
@jwt_required()
def create_booking():
    try:
        data = request.get_json()
        current_user_email = get_jwt_identity()
        users_col = current_app.mongo['users']
        doctors_col = current_app.mongo['doctors']
        bookings_col = current_app.mongo['bookings']

        user = users_col.find_one({'email': current_user_email})
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Validate required fields
        if not all(k in data for k in ('doctor_id', 'appointment_date', 'appointment_time', 'symptoms')):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Ensure doctor exists
        try:
            doctor_obj_id = ObjectId(data['doctor_id'])
        except Exception:
            return jsonify({'message': 'Invalid doctor_id'}), 400
        doctor = doctors_col.find_one({'_id': doctor_obj_id})
        if not doctor:
            return jsonify({'message': 'Doctor not found'}), 404

        # Generate prescription ID
        prescription_id = 'RX-' + datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Create booking document
        booking_doc = {
            'prescription_id': prescription_id,
            'patient_id': user['_id'],
            'doctor_id': doctor_obj_id,
            'appointment_date': data['appointment_date'],
            'appointment_time': data['appointment_time'],
            'symptoms': data['symptoms'],
            'status': 'pending',
            'medicines': [],
            'notes': '',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = bookings_col.insert_one(booking_doc)
        booking_doc['_id'] = result.inserted_id
        
        return jsonify({
            'message': 'Appointment booked successfully',
            'booking': {
                'id': str(booking_doc['_id']),
                'prescription_id': booking_doc['prescription_id'],
                'patient_id': str(booking_doc['patient_id']),
                'doctor_id': str(booking_doc['doctor_id']),
                'doctor_name': doctor.get('name'),
                'appointment_date': booking_doc['appointment_date'],
                'appointment_time': booking_doc['appointment_time'],
                'symptoms': booking_doc['symptoms'],
                'status': booking_doc['status'],
                'medicines': booking_doc['medicines'],
                'notes': booking_doc['notes'],
                'created_at': booking_doc['created_at'].isoformat(),
                'updated_at': booking_doc['updated_at'].isoformat(),
            }
        }), 201
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@booking_bp.route('/my-appointments', methods=['GET'])
@jwt_required()
def get_my_appointments():
    try:
        current_user_email = get_jwt_identity()
        users_col = current_app.mongo['users']
        bookings_col = current_app.mongo['bookings']
        doctors_col = current_app.mongo['doctors']
        user = users_col.find_one({'email': current_user_email})

        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        appointments = list(bookings_col.find({'patient_id': user['_id']}))
        # Optional: sort by date desc
        appointments.sort(key=lambda a: (a.get('appointment_date', ''), a.get('appointment_time', '')), reverse=True)
        
        return jsonify({
            'appointments': [{
                'id': str(app['_id']),
                'prescription_id': app.get('prescription_id'),
                'patient_id': str(app.get('patient_id')) if app.get('patient_id') else None,
                'doctor_id': str(app.get('doctor_id')) if app.get('doctor_id') else None,
                'doctor_name': (doctors_col.find_one({'_id': app.get('doctor_id')}) or {}).get('name') if app.get('doctor_id') else None,
                'appointment_date': app.get('appointment_date'),
                'appointment_time': app.get('appointment_time'),
                'symptoms': app.get('symptoms'),
                'status': app.get('status'),
                'medicines': app.get('medicines', []),
                'notes': app.get('notes'),
                'created_at': app.get('created_at').isoformat() if app.get('created_at') else None,
                'updated_at': app.get('updated_at').isoformat() if app.get('updated_at') else None,
            } for app in appointments]
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
