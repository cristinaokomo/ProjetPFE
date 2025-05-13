from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models.region import Region
from app.models.groundwater_data import GroundwaterData
from app.models.prediction import Prediction
from app.services.prediction_model import generate_prediction
from app import db
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    #regions = Region.query.all()
    regions = []
    return render_template('dashboard/index.html', regions=regions)

@dashboard_bp.route('/region/<int:region_id>')
@login_required
def region_details(region_id):
    region = Region.query.get_or_404(region_id)
    return render_template('dashboard/region_details.html', region=region)

@dashboard_bp.route('/prediction', methods=['GET', 'POST'])
@login_required
def prediction():
    regions = Region.query.all()
    if request.method == 'POST':
        region_id = request.form.get('region_id', type=int)
        period = request.form.get('period', type=int)
        precipitation = request.form.get('precipitation', type=float)
        temperature = request.form.get('temperature', type=float)
        
        # Paramètres pour le modèle de prédiction
        params = {
            'precipitation': precipitation,
            'temperature': temperature,
            'period': period
        }
        
        prediction_result = generate_prediction(region_id, params)
        
        # Sauvegarder la prédiction
        new_prediction = Prediction(
            region_id=region_id,
            user_id=current_user.id,
            prediction_date=datetime.now(),
            predicted_water_level=prediction_result['predicted_level'],
            confidence_interval_low=prediction_result['confidence_low'],
            confidence_interval_high=prediction_result['confidence_high'],
            prediction_period=period,
            parameters=params
        )
        db.session.add(new_prediction)
        db.session.commit()
        
        return render_template('dashboard/prediction_result.html', 
                               prediction=new_prediction, 
                               region=Region.query.get(region_id))
        
    return render_template('dashboard/prediction_form.html', regions=regions)