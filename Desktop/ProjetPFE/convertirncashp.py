import netCDF4 as nc
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import numpy as np

# === 1. Charger le fichier NetCDF ===
ds = nc.Dataset("sud_afrique_tws.nc")  # Remplace par ton propre fichier

# === 2. Extraire les variables ===
lat = ds.variables['lat'][:]
lon = ds.variables['lon'][:]
tws = ds.variables['lwe_thickness'][:]  # Exemple de variable (surface water equivalent)

# === 3. Choisir un pas de temps (ex: première date) ===
tws_snapshot = tws[0, :, :]  # 2D array : lat x lon

# === 4. Créer des points (lat, lon, valeur) ===
data = []
for i in range(len(lat)):
    for j in range(len(lon)):
        value = tws_snapshot[i, j]
        if not np.isnan(value):
            point = Point(lon[j], lat[i])
            data.append({"geometry": point, "value": value})

# === 5. Créer un GeoDataFrame ===
gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")  # WGS84

# === 6. Exporter en fichier shapefile ===
gdf.to_file("output_tws_snapshot.shp")
print("✅ Shapefile exporté : output_tws_snapshot.shp")