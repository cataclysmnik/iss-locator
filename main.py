import requests
import json
import time
import plotly.graph_objects as go
import plotly.io as pio
from geopy.distance import geodesic

place = ''
country = ''

# Fetch current ISS data
response = requests.get('https://api.wheretheiss.at/v1/satellites/25544/')
data = response.json()

latitude = data["latitude"]
longitude = data["longitude"]
visibility = data["visibility"]
v = "daylight" if visibility == "daylight" else "Earth's shadow"

altitude = round(data["altitude"], 2)
velocity = round(data["velocity"], 2)
timestamp = time.ctime(data["timestamp"])
ts = data["timestamp"]
t = timestamp.split()

# Generate past and future timestamps (14 past and 14 future positions)
past_timestamps = ','.join([str(ts - i * 100) for i in range(1, 21)])  # 14 past timestamps
future_timestamps = ','.join([str(ts + i * 100) for i in range(1, 21)])  # 14 future timestamps

# Fetch past positions
past_url = f'https://api.wheretheiss.at/v1/satellites/25544/positions?timestamps={past_timestamps}'
past_response = requests.get(past_url)
past_data = past_response.json()

# Fetch future positions
future_url = f'https://api.wheretheiss.at/v1/satellites/25544/positions?timestamps={future_timestamps}'
future_response = requests.get(future_url)
future_data = future_response.json()

# Extract past and future latitudes and longitudes
past_latitudes = [pos['latitude'] for pos in past_data]
past_longitudes = [pos['longitude'] for pos in past_data]
future_latitudes = [pos['latitude'] for pos in future_data]
future_longitudes = [pos['longitude'] for pos in future_data]

print(f"Latitude: {latitude}")
print(f"Longitude: {longitude}")

# Fetch the closest location to the current ISS coordinates
try:
    url = f'http://api.geonames.org/findNearbyPlaceNameJSON?lat={latitude}&lng={longitude}&username=sagniksingha'
    geo = requests.get(url)
    data2 = geo.json()

    place = data2['geonames'][0]['toponymName']
    country = data2['geonames'][0]['countryName']
except:
    place = "ocean"
    country = "none"

if place != "ocean":
    print(f"Closest Location: {place}, {country}")
else:
    print("The ISS is over an ocean.")
print(f"ISS is in {v} at an altitude of {altitude} km and is travelling at a velocity of {velocity} km/h")
print(f"Updated {t[1]} {t[2]}, {t[3]} local time.")

# Add the current position to the list of past and future positions for plotting
all_latitudes = past_latitudes + [latitude] + future_latitudes
all_longitudes = past_longitudes + [longitude] + future_longitudes

# Calculate the distances of all points from the current position
current_position = (latitude, longitude)
distances = [geodesic(current_position, (lat, lon)).km for lat, lon in zip(all_latitudes, all_longitudes)]

# Normalize the distances to calculate marker sizes (closer points get larger markers)
max_distance = max(distances)
marker_sizes = [20 * (1 - (dist / max_distance)) + 2 for dist in distances]  # Marker size decreases with distance

# Normalize distances to calculate the opacity (closer points are more opaque)
opacities = [1 - (dist / max_distance) for dist in distances]

# Create map plot with all positions (past in blue, current in red, future in green)
fig = go.Figure()

# Generate a list of RGBA color strings with decreasing opacity for past positions (blue)
past_colors = [f'rgba(0, 0, 255, {opacity})' for opacity in opacities[:len(past_latitudes)]]

# Plot past positions with a blue line and dimming opacity
fig.add_trace(go.Scattermapbox(
    mode="markers+lines",
    lon=past_longitudes,
    lat=past_latitudes,
    marker={'size': marker_sizes[:len(past_latitudes)], 'color': past_colors},
    line={'color': 'blue', 'width': 2},
    name='Past Positions',
    text=[f'Past: {lat},{lon}' for lat, lon in zip(past_latitudes, past_longitudes)]
))

# Plot current position with a red marker (no line connecting to it)
fig.add_trace(go.Scattermapbox(
    mode="markers",
    lon=[longitude],
    lat=[latitude],
    marker={'size': marker_sizes[len(past_latitudes)], 'color': 'red'},
    name='Current Position',
    text=[f'Current: {place},{country}']
))

# Generate a list of RGBA color strings with decreasing opacity for future positions (green)
future_colors = [f'rgba(0, 255, 0, {opacity})' for opacity in opacities[len(past_latitudes)+1:]]

# Plot future positions with a green line and dimming opacity
fig.add_trace(go.Scattermapbox(
    mode="markers+lines",
    lon=future_longitudes,
    lat=future_latitudes,
    marker={'size': marker_sizes[len(past_latitudes)+1:], 'color': future_colors},
    line={'color': 'green', 'width': 2},
    name='Future Positions',
    text=[f'Future: {lat},{lon}' for lat, lon in zip(future_latitudes, future_longitudes)]
))

# Set map layout
fig.update_layout(
    margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
    ],
    mapbox={
        'center': {'lon': longitude, 'lat': latitude},
        'style': "open-street-map",
        'zoom': 2
    }
)

# Save plot as HTML and open
pio.write_html(fig, file='location.html', auto_open=True)
