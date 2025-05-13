import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
from app.services.data_processor import get_historical_data, preprocess_data

def train_model(region_id):
    """Entraîne un modèle de prédiction pour une région donnée"""
    # Récupération des données historiques
    historical_data = get_historical_data(region_id)
    if historical_data.empty:
        return None
        
    # Prétraitement
    processed_data = preprocess_data(historical_data)
    if processed_data is None:
        return None
        
    # Définition des features et de la cible
    features = ['month', 'day', 'day_of_year', 
               'water_level_lag_1', 'water_level_lag_3', 'water_level_lag_7',
               'precipitation_lag_1', 'precipitation_lag_3',
               'water_level_rolling_7', 'precipitation_rolling_7',
               'temperature', 'humidity']
               
    X = processed_data[features]
    y = processed_data['water_level']
    
    # Entraînement du modèle
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, features

def generate_prediction(region_id, params):
    """Génère une prédiction pour une région donnée avec des paramètres spécifiques"""
    # Récupération et entraînement du modèle
    model_data = train_model(region_id)
    if model_data is None:
        return {'error': 'Insufficient data for prediction'}
        
    model, features = model_data
    
    # Récupération des dernières données
    latest_data = get_historical_data(region_id, 
                                     end_date=datetime.now(), 
                                     start_date=datetime.now() - timedelta(days=30))
    processed_latest = preprocess_data(latest_data)
    
    if processed_latest is None or len(processed_latest) < 1:
        return {'error': 'Insufficient recent data for prediction'}
        
    # Création des données d'entrée pour la prédiction
    last_row = processed_latest.iloc[-1].copy()
    
    # Application des paramètres utilisateur
    if 'precipitation' in params:
        last_row['precipitation'] = params['precipitation']
        
    if 'temperature' in params:
        last_row['temperature'] = params['temperature']
        
    # Prédiction
    prediction_input = last_row[features].values.reshape(1, -1)
    predicted_level = model.predict(prediction_input)[0]
    
    # Calcul de l'intervalle de confiance (simpliste)
    predictions = []
    for _ in range(100):
        # Ajout d'un bruit aléatoire pour simuler l'incertitude
        noisy_input = prediction_input + np.random.normal(0, 0.1, prediction_input.shape)
        predictions.append(model.predict(noisy_input)[0])
        
    confidence_low = np.percentile(predictions, 5)
    confidence_high = np.percentile(predictions, 95)
    
    return {
        'predicted_level': predicted_level,
        'confidence_low': confidence_low,
        'confidence_high': confidence_high
    }