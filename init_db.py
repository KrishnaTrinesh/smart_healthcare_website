# kbn/backend/init_db.py
from backend.app import app
from models import db
from models.doctor import Doctor
import bcrypt
import os

def init_db():
    with app.app_context():
        try:
            db.create_all()
            print("✅ Tables created successfully in the configured DB.")
        except Exception as e:
            print("⚠️ Error creating tables:", e)
            return

        # Example: seed a default doctor (modify as necessary)
        seed_email = os.getenv('SEED_DOCTOR_EMAIL', 'james.wilson@smarthealthcare.com')
        existing = Doctor.query.filter_by(email=seed_email).first()
        if existing:
            print("ℹ️ Seed doctor already exists, skipping.")
            return

        try:
            plain_pw = os.getenv('SEED_DOCTOR_PW', 'doc123')
            hashed = bcrypt.hashpw(plain_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            doctor = Doctor(
                id=os.getenv('SEED_DOCTOR_ID', 'DOC005'),
                name=os.getenv('SEED_DOCTOR_NAME', 'Dr. James Wilson'),
                email=seed_email,
                password=hashed,
                specialty=os.getenv('SEED_DOCTOR_SPECIALTY', 'Neurology'),
                experience=os.getenv('SEED_DOCTOR_EXPERIENCE', '18 years'),
                phone=os.getenv('SEED_DOCTOR_PHONE', '+1-555-0105'),
                availability=os.getenv('SEED_DOCTOR_AVAILABILITY', 'Mon-Fri 7AM-3PM')
            )
            db.session.add(doctor)
            db.session.commit()
            print("✅ Initial doctor account added.")
        except Exception as e:
            db.session.rollback()
            print("⚠️ Error adding seed doctor:", e)

if __name__ == '__main__':
    init_db()
    print("✅ Database initialization completed.")
