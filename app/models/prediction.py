from app import db
from datetime import datetime

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prediction_date = db.Column(db.DateTime, nullable=False)
    predicted_water_level = db.Column(db.Float)
    confidence_interval_low = db.Column(db.Float)
    confidence_interval_high = db.Column(db.Float)
    prediction_period = db.Column(db.Integer)  # période en jours
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    parameters = db.Column(db.JSON)  # stockage des paramètres utilisés