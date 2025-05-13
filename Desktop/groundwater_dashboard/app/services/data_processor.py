import pandas as pd
import numpy as np
from app.models.groundwater_data import GroundwaterData

def get_historical_data(region_id, start_date=None, end_date=None):
    """Récupère les données historiques pour une région donnée"""
    query = GroundwaterData.query.filter_by(region_id=region_id)
    
    if start_date:
        query = query.filter(GroundwaterData.date >= start_date)
    if end_date:
        query = query.filter(GroundwaterData.date <= end_date)
        
    data = query.order_by(GroundwaterData.date).all()
    
    # Conversion en DataFrame pandas
    df = pd.DataFrame([{
        'date': d.date,
        'water_level': d.water_level,
        'precipitation': d.precipitation,
        'temperature': d.temperature,
        'humidity': d.humidity
    } for d in data])
    
    return df

def preprocess_data(df):
    """Prétraitement des données pour le modèle de prédiction"""
    if df.empty:
        return None
        
    # Gestion des valeurs manquantes
    df = df.fillna(method='ffill')
    
    # Extraction de caractéristiques temporelles
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_year'] = df['date'].dt.dayofyear
    
    # Création de lag features
    for lag in [1, 3, 7, 14]:
        df[f'water_level_lag_{lag}'] = df['water_level'].shift(lag)
        df[f'precipitation_lag_{lag}'] = df['precipitation'].shift(lag)
        
    # Moyenne mobile
    df['water_level_rolling_7'] = df['water_level'].rolling(window=7).mean()
    df['precipitation_rolling_7'] = df['precipitation'].rolling(window=7).mean()
    
    # Suppression des lignes avec NaN après création des features
    df = df.dropna()
    
    return df