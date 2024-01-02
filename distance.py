import pandas as pd
import numpy as np

from pyproj import Proj, transform

def latlon_to_utm_zone_28N(latitude, longitude):
    # UTM zone 28N for the given area
    utm_proj = Proj('+proj=utm +zone=28 +north +ellps=WGS84')
    wgs84_proj = Proj(proj='latlong', datum='WGS84')

    utm_x, utm_y = transform(wgs84_proj, utm_proj, longitude, latitude)
    return utm_x, utm_y

# Function to calculate Euclidean distance (vectorized for performance)
def euclidean_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def process_chunk(chunk, point_x, point_y):
    chunk['LONGITUDE'] = pd.to_numeric(chunk['LONGITUDE'], errors='coerce', downcast='float') # convertit en float
    chunk['LATITUDE'] = pd.to_numeric(chunk['LATITUDE'], errors='coerce', downcast='float')
    chunk['distance'] = euclidean_distance(point_x, point_y, chunk['LONGITUDE'], chunk['LATITUDE']) # rajoute un colonne distance correspondant a la distance du point donne avec le point "en cours"
    return chunk

# convertit le fichier xlsx en csv d'abord, le format sera beaucoup plus clean
# df = pd.read_excel('Base localites_senegal_2023(1).xlsx')
# df.to_csv("Base localites_senegal_2023(1).csv")

file_path = 'Base localites_senegal_2023(1).csv'

# point_x = 241579.092567
# point_y = 1622974.33196

# # Test ngor
# point_x = 229390.262541940785013
# point_y = 1631310.526640818454325

# Test malika
point_x = 250675.231264704605564
point_y = 1637933.475530221825466

chunk_size = 1000  


closest_points = pd.DataFrame()
for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    processed_chunk = process_chunk(chunk, point_x, point_y)
    closest_points = pd.concat([closest_points, processed_chunk.nsmallest(5, 'distance')])

# Renvoi les 5 points les plus proches
closest_points = closest_points.nsmallest(5, 'distance')
print(closest_points)

closest_points.to_csv("voisinage.csv")




