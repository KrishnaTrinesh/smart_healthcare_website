from . import db
from datetime import datetime

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    experience = db.Column(db.String(50))
    rating = db.Column(db.Float, default=0.0)
    availability = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='doctor', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'specialty': self.specialty,
            'phone': self.phone,
            'experience': self.experience,
            'rating': self.rating,
            'availability': self.availability,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
