"""
Script to export existing MongoDB data from Program Files and prepare for migration
Run this when MongoDB is running to backup your data
"""
import json
from pymongo import MongoClient
from bson import json_util
import os

# Connect to existing MongoDB
try:
    client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=5000)
    client.server_info()  # Verify connection
    print("✓ Connected to MongoDB")
except Exception as e:
    print(f"✗ Could not connect to MongoDB: {e}")
    print("\nPlease ensure MongoDB is running first.")
    print("Start MongoDB from Program Files or run Start-MongoDB.bat")
    exit(1)

db = client['smarthealthcare']

# Create output directory
output_dir = os.path.join(os.path.dirname(__file__), 'backup')
os.makedirs(output_dir, exist_ok=True)

print(f"\nExporting data to: {output_dir}")

# Export users
try:
    users = list(db.users.find())
    with open(os.path.join(output_dir, 'users.json'), 'w') as f:
        json.dump(users, f, indent=2, default=json_util.default)
    print(f"✓ Exported {len(users)} users")
except Exception as e:
    print(f"✗ Error exporting users: {e}")

# Export doctors
try:
    doctors = list(db.doctors.find())
    with open(os.path.join(output_dir, 'doctors.json'), 'w') as f:
        json.dump(doctors, f, indent=2, default=json_util.default)
    print(f"✓ Exported {len(doctors)} doctors")
except Exception as e:
    print(f"✗ Error exporting doctors: {e}")

# Export bookings if they exist
try:
    bookings = list(db.bookings.find())
    if bookings:
        with open(os.path.join(output_dir, 'bookings.json'), 'w') as f:
            json.dump(bookings, f, indent=2, default=json_util.default)
        print(f"✓ Exported {len(bookings)} bookings")
except Exception as e:
    print(f"✗ Error exporting bookings: {e}")

print(f"\n✓ Data exported successfully to {output_dir}")
print("\nNext steps:")
print("1. Copy the data files from db/backup/ to db/data/")
print("2. Or use mongorestore to restore from the exported files")

