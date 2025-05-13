from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models.region import Region
from app.models.groundwater_data import GroundwaterData
from app.models.prediction import Prediction
from app import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/regions')
@login_required
def get_regions():
    regions = Region.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'latitude': r.latitude,
        'longitude': r.longitude
    } for r in regions])

@api_bp.route('/groundwater/<int:region_id>')
@login_required
def get_groundwater_data(region_id):
    data = GroundwaterData.query.filter_by(region_id=region_id).all()
    return jsonify([{
        'date': d.date.strftime('%Y-%m-%d'),
        'water_level': d.water_level,
        'precipitation': d.precipitation,
        'temperature': d.temperature
    } for d in data])

@api_bp.route('/predictions/<int:region_id>')
@login_required
def get_predictions(region_id):
    predictions = Prediction.query.filter_by(region_id=region_id).all()
    return jsonify([{
        'date': p.prediction_date.strftime('%Y-%m-%d'),
        'predicted_level': p.predicted_water_level,
        'confidence_low': p.confidence_interval_low,
        'confidence_high': p.confidence_interval_high,
        'period': p.prediction_period
    } for p in predictions])