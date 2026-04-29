# Smart Healthcare Backend API

Flask-based backend API for the Smart Healthcare Appointment System.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. API Endpoints

#### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login (user or doctor)

#### Doctor Routes
- `GET /api/doctor/profile` - Get doctor profile
- `GET /api/doctor/queue` - Get patient queue
- `POST /api/doctor/prescribe/<booking_id>` - Prescribe medicines

#### Booking Routes
- `GET /api/booking/doctors` - Get list of doctors
- `POST /api/booking/create` - Create an appointment
- `GET /api/booking/my-appointments` - Get user's appointments

## Database

The application now uses MongoDB. Configure your Mongo connection via environment variables.

## Environment Variables

Create a `.env` file in the backend directory with the following:

```
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=jwt-secret-string
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=smarthealthcare
```
