from app import db
from datetime import datetime

class GroundwaterData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    water_level = db.Column(db.Float)  # niveau en mètres par rapport à un point de référence
    precipitation = db.Column(db.Float)  # précipitations en mm
    temperature = db.Column(db.Float)  # température moyenne en °C
    humidity = db.Column(db.Float)  # humidité en %
    created_at = db.Column(db.DateTime, default=datetime.utcnow)