import folium
from folium.plugins import MarkerCluster
import pandas as pd
import os
import webbrowser
import random
import sys


sys.path.insert(0,'..' + os.sep + 'gui')


la=pd.Series([random.uniform(0.1438333,1.021388)+55 for _ in range(100)])
lo=pd.Series([random.uniform(0.80325001, 1.96777778)+ 36 for _ in range(100)])
el=pd.Series([random.uniform(1000, 6000) for _ in range(100)])


dat = {
    'LAT': la,
    'LON': lo,
    'ELEV': el
}

data = pd.DataFrame(dat)

print(data)
lat = data['LAT']
lon = data['LON']
elevation = data['ELEV']

def color_change(elev):
    if(elev < 1500):
        return('green')
    elif(15 <= elev < 3000):
        return('orange')
    else:
        return('red')

map = folium.Map(location=[55.1438333,36.80325001], zoom_start = 5, tiles = "CartoDB dark_matter")

marker_cluster = MarkerCluster().add_to(map)

for lat, lon, elevation in zip(lat, lon, elevation):
    folium.CircleMarker(location=[lat, lon], radius = 9, popup=str(elevation)+" m", fill_color=color_change(elevation), color="gray", fill_opacity = 0.9).add_to(marker_cluster)

map.save(".." + os.sep + "data" + os.sep + "cout" + os.sep + "map0_test.html")
path = os.path.abspath('..' + os.sep + 'data' + os.sep + 'cout' + os.sep + 'map0_test.html')
url = 'file://' + path

webbrowser.open(url)

data.to_csv(".." + os.sep + "data" + os.sep + "cout" + os.sep + "Moscow_cam.csv")
