"""
Creation of satellite passes over ground terminals
"""

from skyfield.api import Topos, load, EarthSatellite
from skyfield.elementslib import osculating_elements_of
import numpy as np
import pandas as pd
from datetime import datetime
import requests

class SatellitePass:
    def __init__(self, id, nodeId, startTime, endTime, achievableKeyVolume, orbitId):
        self.id = id
        self.nodeId = nodeId
        self.startTime = startTime
        self.endTime = endTime
        self.achievableKeyVolume = achievableKeyVolume
        self.orbitId = orbitId
    
    def __repr__(self):
        return (f"SatellitePass(id={self.id}, nodeId={self.nodeId}, startTime={self.startTime}, "
                f"endTime={self.endTime}, achievableKeyVolume={self.achievableKeyVolume}, orbitId={self.orbitId})")

    def to_dict(self):
        return self.__dict__
    
# Load TLE Data for the Satellite
ts = load.timescale()

# UK-DMC 2
tle_lines = [
    "1 35683U 09041C   25045.14309186  .00001921  00000-0  29495-3 0  9992",
    "2 35683  97.8105 189.5655 0001400  83.0116 277.1253 14.74670943834658",
]

# Store weather data to reduce amount of api requests
request_answer_dict = dict()

# Function for getting weather data for a specific day and position
def fetch_weather_data_with_cloud_coverage(latitude, longitude, date):
    response = None

    # If data was already fetched return from set
    if ((latitude, longitude, date) in request_answer_dict):
        response = request_answer_dict[(latitude, longitude, date)]
    else:
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
        request_answer_dict[(latitude, longitude, date)] = response
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
    if daylight_duration_seconds == 0:
        cloud_coverage = 0.5
    else:  
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

def convert_and_sort_dataframe_to_satellite_passes(df_satellite_passes):
    # Convert DataFrame rows to SatellitePass objects
    satellite_passes = []
    for idx, row in df_satellite_passes.iterrows():
        satellite_pass = SatellitePass(
            id=idx,
            nodeId=row['Station'],
            startTime=row['Start'],
            endTime=row['End'],
            achievableKeyVolume=row['Key Volume'],
            orbitId=row['Orbit']
        )
        satellite_passes.append(satellite_pass.to_dict())

    # Sort the SatellitePass objects by startTime
    satellite_passes.sort(key=lambda sp: sp["startTime"])
    return satellite_passes

def get_quarc_satellite_passes(ground_terminals, start_time, end_time, step_duration, min_elevation_angle):
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
        lat = ground_terminals[terminal]["lat"]
        lon = ground_terminals[terminal]["lon"]
        date = row["Start"]
        # Parse the string into a datetime object
        date_object = datetime.strptime(row["Start"], "%Y-%m-%dT%H:%M:%S")
        # Format the datetime object to 'YYYY-MM-DD'
        date = date_object.strftime("%Y-%m-%d")

        # Fetch weather data
        cloud_coverage_fraction = fetch_weather_data_with_cloud_coverage(lat, lon, date)["cloud_coverage_fraction"]

        # Use cloud coverage to adjust key volume
        return key_volume * (1 - cloud_coverage_fraction)

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
    print("Calculating orbits ...")
    df_satellite_passes["Orbit"] = df_satellite_passes.apply(assign_orbit, axis=1)
    print(df_satellite_passes)

    # Convert satellite passes dataframe to list of satellite pass objects
    satellite_passes_dict_list = convert_and_sort_dataframe_to_satellite_passes(df_satellite_passes)

    return satellite_passes_dict_list