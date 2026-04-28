from database import db
from datetime import datetime

class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    in_diet = db.Column(db.Boolean, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)