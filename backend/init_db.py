from backend.app import app
from models import db
from models.doctor import Doctor
import bcrypt

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if we need to add initial doctor
        if not Doctor.query.filter_by(email='james.wilson@smarthealthcare.com').first():
            # Create initial doctor
            password = bcrypt.hashpw('doc123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            doctor = Doctor(
                id='DOC005',
                name='Dr. James Wilson',
                email='james.wilson@smarthealthcare.com',
                password=password,
                specialty='Neurology',
                experience='18 years',
                phone='+1-555-0105',
                availability='Mon-Fri 7AM-3PM'
            )
            db.session.add(doctor)
            db.session.commit()
            print("Added initial doctor account")

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")