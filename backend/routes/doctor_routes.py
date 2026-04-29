from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import bcrypt
import json
from bson import ObjectId
from datetime import datetime

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user_email = get_jwt_identity()
        doctors = current_app.mongo['doctors']
        doctor = doctors.find_one({'email': current_user_email})
        
        if not doctor:
            return jsonify({'message': 'Doctor not found'}), 404
        
        return jsonify({'doctor': {
            'id': str(doctor['_id']),
            'email': doctor.get('email'),
            'name': doctor.get('name'),
            'specialty': doctor.get('specialty'),
            'phone': doctor.get('phone'),
            'experience': doctor.get('experience'),
            'rating': doctor.get('rating', 0.0),
            'availability': doctor.get('availability'),
        }}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@doctor_bp.route('/queue', methods=['GET'])
@jwt_required()
def get_patient_queue():
    try:
        current_user_email = get_jwt_identity()
        doctors = current_app.mongo['doctors']
        bookings = current_app.mongo['bookings']
        doctor = doctors.find_one({'email': current_user_email})
        
        if not doctor:
            return jsonify({'message': 'Doctor not found'}), 404
        
        # Get all appointments for this doctor
        appointments = list(bookings.find({'doctor_id': doctor['_id']}))
        appointments.sort(key=lambda a: (a.get('appointment_date', ''), a.get('appointment_time', '')))
        
        return jsonify({
            'appointments': [{
                'id': str(app['_id']),
                'prescription_id': app.get('prescription_id'),
                'patient_id': str(app.get('patient_id')) if app.get('patient_id') else None,
                'doctor_id': str(app.get('doctor_id')) if app.get('doctor_id') else None,
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

@doctor_bp.route('/prescribe/<booking_id>', methods=['POST'])
@jwt_required()
def prescribe_medicines(booking_id):
    try:
        data = request.get_json()
        bookings = current_app.mongo['bookings']
        try:
            booking_obj_id = ObjectId(booking_id)
        except Exception:
            return jsonify({'message': 'Invalid booking_id'}), 400
        booking = bookings.find_one({'_id': booking_obj_id})
        if not booking:
            return jsonify({'message': 'Booking not found'}), 404
        
        # Update booking with medicines
        update_doc = {
            '$set': {
                'medicines': data.get('medicines', []),
                'notes': data.get('notes', ''),
                'status': 'completed',
                'updated_at': datetime.utcnow()
            }
        }
        bookings.update_one({'_id': booking_obj_id}, update_doc)
        updated = bookings.find_one({'_id': booking_obj_id})
        
        return jsonify({
            'message': 'Prescription completed successfully',
            'booking': {
                'id': str(updated['_id']),
                'prescription_id': updated.get('prescription_id'),
                'patient_id': str(updated.get('patient_id')) if updated.get('patient_id') else None,
                'doctor_id': str(updated.get('doctor_id')) if updated.get('doctor_id') else None,
                'appointment_date': updated.get('appointment_date'),
                'appointment_time': updated.get('appointment_time'),
                'symptoms': updated.get('symptoms'),
                'status': updated.get('status'),
                'medicines': updated.get('medicines', []),
                'notes': updated.get('notes'),
                'created_at': updated.get('created_at').isoformat() if updated.get('created_at') else None,
                'updated_at': updated.get('updated_at').isoformat() if updated.get('updated_at') else None,
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
