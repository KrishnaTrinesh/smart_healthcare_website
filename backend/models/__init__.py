from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .doctor import Doctor
from .booking import Booking

__all__ = ['db', 'User', 'Doctor', 'Booking']
