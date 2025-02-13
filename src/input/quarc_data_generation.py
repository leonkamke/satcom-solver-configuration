"""
Creation of problem instances based on the article:
'QUARC: Quantum Research Cubesat—A Constellation for Quantum Communication'
Link: https://www.mdpi.com/2410-387X/4/1/7
"""


from skyfield.api import Topos, load, EarthSatellite
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# Step duration in seconds for elevation angles
step_duration = 5

# Minimum elevation angle in degrees
min_elevation_angle = 20

# Calculate key volume
def calculate_key_volume(row):
    # Approximated key rate depending on elevation angle of satellite
    def quarcKeyRateApproximation(elevation):
        return -0.0145 * (elevation**3) + 2.04 * (elevation**2) - 20.65 * elevation + 88.42
    elevation_angles = row["Elevations"]
    key_rates = [quarcKeyRateApproximation(e) for e in elevation_angles]
    key_volume = sum(rate * step_duration for rate in key_rates)  # Volume in bits
    return key_volume

# Load TLE Data for the Satellite
ts = load.timescale()
# UK-DMC 2
tle_lines = [
    "1 35683U 09041C   25042.20210648  .00000023  00000+0  12345-4 0  9991",
    "2 35683  97.9500 123.4567 0001234  98.7654 261.2345 14.12345678901234",
]

# Load the satellite from TLE
satellite = EarthSatellite(tle_lines[0], tle_lines[1], 'QUARC', ts)
satellite_name = satellite.name

# QUARC Ground Terminal locations UK
quarc_ground_terminals = [
    {"name": "Station1", "lat": 61, "lon": -1, "alt": 0},
    {"name": "Station2", "lat": 60, "lon": -1, "alt": 0},
    {"name": "Station3", "lat": 59, "lon": -3, "alt": 0},
    {"name": "Station4", "lat": 58, "lon": -4, "alt": 0},
    {"name": "Station5", "lat": 58, "lon": -5, "alt": 0},
    {"name": "Station6", "lat": 58, "lon": -7, "alt": 0},
    {"name": "Station7", "lat": 57, "lon": -3, "alt": 0},
    {"name": "Station8", "lat": 57, "lon": -4, "alt": 0},
    {"name": "Station9", "lat": 57, "lon": -5, "alt": 0},
    {"name": "Station10", "lat": 57, "lon": -6, "alt": 0},
    {"name": "Station11", "lat": 56, "lon": -3, "alt": 0},
    {"name": "Station12", "lat": 56, "lon": -4, "alt": 0},
    {"name": "Station13", "lat": 56, "lon": -5, "alt": 0},
    {"name": "Station14", "lat": 56, "lon": -6, "alt": 0},
    {"name": "Station15", "lat": 55, "lon": -2, "alt": 0},
    {"name": "Station16", "lat": 55, "lon": -3, "alt": 0},
    {"name": "Station17", "lat": 55, "lon": -4, "alt": 0},
    {"name": "Station18", "lat": 55, "lon": -5, "alt": 0},
    {"name": "Station19", "lat": 55, "lon": -6, "alt": 0},
    {"name": "Station20", "lat": 55, "lon": -7, "alt": 0},
    {"name": "Station21", "lat": 55, "lon": -4, "alt": 0},
    {"name": "Station22", "lat": 54, "lon": -1, "alt": 0},
    {"name": "Station23", "lat": 54, "lon": -2, "alt": 0},
    {"name": "Station24", "lat": 54, "lon": -3, "alt": 0},
    {"name": "Station25", "lat": 54, "lon": -6, "alt": 0},
    {"name": "Station26", "lat": 53, "lon": 1, "alt": 0},
    {"name": "Station27", "lat": 53, "lon": 0, "alt": 0},
    {"name": "Station28", "lat": 53, "lon": -1, "alt": 0},
    {"name": "Station29", "lat": 53, "lon": -2, "alt": 0},
    {"name": "Station30", "lat": 53, "lon": -3, "alt": 0},
    {"name": "Station31", "lat": 53, "lon": -4, "alt": 0},
    {"name": "Station32", "lat": 52, "lon": 1, "alt": 0},
    {"name": "Station33", "lat": 52, "lon": 0, "alt": 0},
    {"name": "Station34", "lat": 52, "lon": -1, "alt": 0},
    {"name": "Station35", "lat": 52, "lon": -2, "alt": 0},
    {"name": "Station36", "lat": 52, "lon": -3, "alt": 0},
    {"name": "Station37", "lat": 52, "lon": -4, "alt": 0},
    {"name": "Station38", "lat": 51, "lon": 1, "alt": 0},
    {"name": "Station39", "lat": 51, "lon": 0, "alt": 0},
    {"name": "Station40", "lat": 51, "lon": -1, "alt": 0},
    {"name": "Station41", "lat": 51, "lon": -2, "alt": 0},
    {"name": "Station42", "lat": 51, "lon": -3, "alt": 0},
    {"name": "Station43", "lat": 51, "lon": -4, "alt": 0},
]

ground_terminals = [
    {"name": "Station1", "lat": 61, "lon": -1, "alt": 0}
]


# Observation Time Period
start_time_np = np.datetime64('2025-02-12T00:00:00')
end_time_np = np.datetime64('2025-02-13T00:00:00')

# Calculate Passes for Each Ground Terminal
passes_data = []

print("Calculating satellite passes ...")

for terminal in ground_terminals:
    ground_station = Topos(latitude_degrees=terminal["lat"], 
                           longitude_degrees=terminal["lon"], 
                           elevation_m=terminal["alt"])
    observer = satellite - ground_station

    # Create evenly spaced time steps
    time_steps = np.arange(start_time_np, end_time_np, np.timedelta64(step_duration, 's'))

    # Convert numpy datetime64 to datetime and then to Skyfield time objects
    skyfield_times = ts.utc(
        [t.astype(datetime).year for t in time_steps],
        [t.astype(datetime).month for t in time_steps],
        [t.astype(datetime).day for t in time_steps],
        [t.astype(datetime).hour for t in time_steps],
        [t.astype(datetime).minute for t in time_steps],
        [t.astype(datetime).second for t in time_steps]
    )
    elevation_angles = []
    for time in skyfield_times:
        alt, az, distance = observer.at(time).altaz()
        elevation_angles.append((time.utc_iso().replace('Z', ''), alt.degrees))
    
    # Filter for Above Horizon Passes
    elevation_angles = [(t, e) for t, e in elevation_angles if e >= min_elevation_angle]
    
    # Group into Passes
    current_pass = []
    for t, e in elevation_angles:
        if not current_pass or (datetime.fromisoformat(t) - datetime.fromisoformat(current_pass[-1][0])).seconds <= 30:
            current_pass.append((t, e))
        else:
            if current_pass:
                passes_data.append({"station": terminal["name"], "pass": current_pass})
            current_pass = [(t, e)]
    if current_pass:
        passes_data.append({"station": terminal["name"], "pass": current_pass})


# Convert to DataFrame
pass_windows = []
for pass_info in passes_data:
    station = pass_info["station"]
    times, elevations = zip(*pass_info["pass"])
    pass_windows.append({"Station": station, "Start": times[0], "End": times[-1], "Elevations": elevations})
df_pass_windows = pd.DataFrame(pass_windows)

print("Calculating key volumes ...")

# Calculate approximated key volume
df_pass_windows["Key Volume"] = df_pass_windows.apply(calculate_key_volume, axis=1)
df_pass_windows = df_pass_windows.drop('Elevations', axis=1)

df_pass_windows.to_csv("testcsv.csv")
print(df_pass_windows)
