from . import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.String(50), unique=True, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    symptoms = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    medicines = db.Column(db.Text)  # JSON string of medicines
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        import json
        medicines = json.loads(self.medicines) if self.medicines else []
        return {
            'id': self.id,
            'prescription_id': self.prescription_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'appointment_date': str(self.appointment_date),
            'appointment_time': str(self.appointment_time),
            'symptoms': self.symptoms,
            'status': self.status,
            'medicines': medicines,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
