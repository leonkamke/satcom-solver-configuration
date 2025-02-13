"""
Creation of problem instances based on the article:
'QUARC: Quantum Research Cubesat—A Constellation for Quantum Communication'
Link: https://www.mdpi.com/2410-387X/4/1/7
"""

from skyfield.api import Topos, load, EarthSatellite
from skyfield.elementslib import osculating_elements_of
import numpy as np
import pandas as pd
from datetime import datetime
import requests

# QUARC Ground Terminal locations in UK
quarc_ground_terminals = {
    "Station1": {"lat": 61, "lon": -1, "alt": 0},
    "Station2": {"lat": 60, "lon": -1, "alt": 0},
    "Station3": {"lat": 59, "lon": -3, "alt": 0},
    "Station4": {"lat": 58, "lon": -4, "alt": 0},
    "Station5": {"lat": 58, "lon": -5, "alt": 0},
    "Station6": {"lat": 58, "lon": -7, "alt": 0},
    "Station7": {"lat": 57, "lon": -3, "alt": 0},
    "Station8": {"lat": 57, "lon": -4, "alt": 0},
    "Station9": {"lat": 57, "lon": -5, "alt": 0},
    "Station10": {"lat": 57, "lon": -6, "alt": 0},
    "Station11": {"lat": 56, "lon": -3, "alt": 0},
    "Station12": {"lat": 56, "lon": -4, "alt": 0},
    "Station13": {"lat": 56, "lon": -5, "alt": 0},
    "Station14": {"lat": 56, "lon": -6, "alt": 0},
    "Station15": {"lat": 55, "lon": -2, "alt": 0},
    "Station16": {"lat": 55, "lon": -3, "alt": 0},
    "Station17": {"lat": 55, "lon": -4, "alt": 0},
    "Station18": {"lat": 55, "lon": -5, "alt": 0},
    "Station19": {"lat": 55, "lon": -6, "alt": 0},
    "Station20": {"lat": 55, "lon": -7, "alt": 0},
    "Station21": {"lat": 55, "lon": -4, "alt": 0},
    "Station22": {"lat": 54, "lon": -1, "alt": 0},
    "Station23": {"lat": 54, "lon": -2, "alt": 0},
    "Station24": {"lat": 54, "lon": -3, "alt": 0},
    "Station25": {"lat": 54, "lon": -6, "alt": 0},
    "Station26": {"lat": 53, "lon": 1, "alt": 0},
    "Station27": {"lat": 53, "lon": 0, "alt": 0},
    "Station28": {"lat": 53, "lon": -1, "alt": 0},
    "Station29": {"lat": 53, "lon": -2, "alt": 0},
    "Station30": {"lat": 53, "lon": -3, "alt": 0},
    "Station31": {"lat": 53, "lon": -4, "alt": 0},
    "Station32": {"lat": 52, "lon": 1, "alt": 0},
    "Station33": {"lat": 52, "lon": 0, "alt": 0},
    "Station34": {"lat": 52, "lon": -1, "alt": 0},
    "Station35": {"lat": 52, "lon": -2, "alt": 0},
    "Station36": {"lat": 52, "lon": -3, "alt": 0},
    "Station37": {"lat": 52, "lon": -4, "alt": 0},
    "Station38": {"lat": 51, "lon": 1, "alt": 0},
    "Station39": {"lat": 51, "lon": 0, "alt": 0},
    "Station40": {"lat": 51, "lon": -1, "alt": 0},
    "Station41": {"lat": 51, "lon": -2, "alt": 0},
    "Station42": {"lat": 51, "lon": -3, "alt": 0},
    "Station43": {"lat": 51, "lon": -4, "alt": 0},
}

ground_terminals = {
    "Station1": {"lat": 61, "lon": -1, "alt": 0}
}

# Load TLE Data for the Satellite
ts = load.timescale()

# UK-DMC 2
tle_lines = [
    "1 35683U 09041C   25042.20210648  .00000023  00000+0  12345-4 0  9991",
    "2 35683  97.9500 123.4567 0001234  98.7654 261.2345 14.12345678901234",
]

# Function for getting weather data for a specific day and position
def fetch_weather_data_with_cloud_coverage(latitude, longitude, date):
    # Base URL for the Open-Meteo API
    url = "https://archive-api.open-meteo.com/v1/era5"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": date,
        "end_date": date,
        "daily": "sunshine_duration,sunrise,sunset",
        "timezone": "auto"
    }
    
    # Make the request
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")
    
    # Parse the JSON response
    data = response.json()
    
    # Extract relevant data
    sunrise = data["daily"]["sunrise"][0]
    sunset = data["daily"]["sunset"][0]
    sunshine_duration = data["daily"]["sunshine_duration"][0]  # In seconds

    # Convert sunrise and sunset to datetime objects
    sunrise_time = datetime.fromisoformat(sunrise)
    sunset_time = datetime.fromisoformat(sunset)

    # Calculate the duration between sunrise and sunset in seconds
    daylight_duration_seconds = (sunset_time - sunrise_time).seconds

    # Calculate cloud coverage (1 - sunshine_duration / daylight_duration)
    cloud_coverage = 1 - (sunshine_duration / daylight_duration_seconds)
    
    # Convert sunshine duration to hours for easier interpretation
    sunshine_duration_hours = sunshine_duration / 3600

    return {
        "date": date,
        "latitude": latitude,
        "longitude": longitude,
        "sunrise": sunrise,
        "sunset": sunset,
        "sunshine_duration_hours": sunshine_duration_hours,
        "daylight_duration_hours": daylight_duration_seconds / 3600,  # Convert seconds to hours
        "cloud_coverage_fraction": cloud_coverage  # Value between 0 (clear) and 1 (fully cloudy)
    }

# Calculate key volume using QUARC approximation
def calculate_key_volume(row):
    # Approximated key rate depending on elevation angle of satellite
    def quarc_key_rate_approximation(elevation):
        return -0.0145 * (elevation**3) + 2.04 * (elevation**2) - 20.65 * elevation + 88.42
    
    elevation_angles = row["Elevations"]
    key_rates = [quarc_key_rate_approximation(e) for e in elevation_angles]
    key_volume = sum(rate * step_duration for rate in key_rates)  # Volume in bits

    # Adjust key volume depending on cloud coverage
    terminal = row["Station"]
    lat = quarc_ground_terminals[terminal]["lat"]
    lon = quarc_ground_terminals[terminal]["lon"]
    date = row["Start"]
    # Parse the string into a datetime object
    date_object = datetime.strptime(row["Start"], "%Y-%m-%dT%H:%M:%S")
    # Format the datetime object to 'YYYY-MM-DD'
    date = date_object.strftime("%Y-%m-%d")

    # Fetch weather data
    cloud_coverage_fraction = fetch_weather_data_with_cloud_coverage(lat, lon, date)["cloud_coverage_fraction"]

    # Use cloud coverage to adjust key volume
    return key_volume * (1 - cloud_coverage_fraction)

def get_problem_instance(start_time, end_time, step_duration, min_elevation_angle):
    # Load the satellite from TLE
    satellite = EarthSatellite(tle_lines[0], tle_lines[1], 'QUARC', ts)

    # Compute orbital period in seconds
    earth = satellite.at(ts.now())
    elements = osculating_elements_of(earth)
    orbit_duration = elements.period_in_days * 24 * 60 * 60

    # Function that assigns a satellite pass to an orbit
    def assign_orbit(row):
        # Calculate the time difference between the start of the pass and the orbit start time
        orbit_start_time = start_time
        pass_start_time = pd.to_datetime(row['Start'])
        time_difference = (pass_start_time - orbit_start_time).total_seconds()
        # Calculate orbit ID
        orbit_id = int(time_difference // orbit_duration)
        return orbit_id

    # Calculate Passes for Each Ground Terminal
    print("Calculating satellite passes ...")

    passes_data = []
    for terminal, position in ground_terminals.items():
        ground_station = Topos(latitude_degrees=position["lat"], 
                            longitude_degrees=position["lon"], 
                            elevation_m=position["alt"])
        observer = satellite - ground_station

        # Create evenly spaced time steps
        time_steps = np.arange(start_time, end_time, np.timedelta64(step_duration, 's'))

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
                    passes_data.append({"station": terminal, "pass": current_pass})
                current_pass = [(t, e)]
        if current_pass:
            passes_data.append({"station": terminal, "pass": current_pass})

    # Convert to DataFrame
    satellite_passes = []
    for pass_info in passes_data:
        station = pass_info["station"]
        times, elevations = zip(*pass_info["pass"])
        satellite_passes.append({"Station": station, "Start": times[0], "End": times[-1], "Elevations": elevations})
    df_satellite_passes = pd.DataFrame(satellite_passes)

    # Calculate approximated key volume
    print("Calculating key volumes ...")
    df_satellite_passes["Key Volume"] = df_satellite_passes.apply(calculate_key_volume, axis=1)
    df_satellite_passes = df_satellite_passes.drop('Elevations', axis=1)

    # Calculate orbits
    print("Calculate orbits")
    df_satellite_passes["Orbit"] = df_satellite_passes.apply(assign_orbit, axis=1)

    return df_satellite_passes


# Observation Time Period
start_time = np.datetime64('2024-02-12T00:00:00')
end_time = np.datetime64('2024-02-13T00:00:00')

# Step duration in seconds for elevation angles
step_duration = 10

# Minimum elevation angle in degrees
min_elevation_angle = 20

satellite_passes_df = get_problem_instance(start_time, end_time, step_duration, min_elevation_angle)
print(satellite_passes_df)