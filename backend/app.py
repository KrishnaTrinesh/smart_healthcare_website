# kbn/backend/app.py
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import routes
# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__,
           instance_relative_config=True,
           static_url_path='',
           static_folder='../')  # serve static files from parent folder (kbn/)

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path, exist_ok=True)
except OSError:
    pass

# Basic config
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me-in-prod')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv('JWT_EXPIRES_HOURS', '24')))

# =========================================================
# MongoDB configuration
# - Provide MONGO_URI and MONGO_DB_NAME in .env like:
#   MONGO_URI=mongodb://localhost:27017
#   MONGO_DB_NAME=smarthealthcare
# =========================================================
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
app.config['MONGO_DB_NAME'] = os.getenv('MONGO_DB_NAME', 'smarthealthcare')

# Initialize Mongo client
mongo_client = MongoClient(app.config['MONGO_URI'])
app.mongo = mongo_client[app.config['MONGO_DB_NAME']]

# Initialize extensions
CORS(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGINS", "http://localhost:8000")}}, supports_credentials=True)
jwt = JWTManager(app)

# Add CORS headers to all responses (optional - keep for cross origin)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', os.getenv("CORS_ORIGINS", "http://localhost:8000"))
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Import and register blueprints (keep your existing route files)
from routes.auth_routes import auth_bp
from routes.doctor_routes import doctor_bp
from routes.booking_routes import booking_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
app.register_blueprint(booking_bp, url_prefix='/api/booking')

# Serve static files
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # ping the server to ensure connectivity
        mongo_client.admin.command('ping')
        db_status = 'OK'
    except Exception as e:
        db_status = f'ERROR: {str(e)}'
    return jsonify({'status': 'OK', 'db': db_status, 'message': 'Smart Healthcare API running'}), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Flask app starting. Mongo DB:", app.config['MONGO_DB_NAME'], "URI:", app.config['MONGO_URI'])
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
