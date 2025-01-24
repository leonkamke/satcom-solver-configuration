from skyfield.api import Topos, load, EarthSatellite, wgs84
from datetime import datetime, timedelta

tle_lines = [
    "1 00001U 23001A   23020.00000000  .00000000  00000-0  00000-0 0  0000",
    "2 00001 097.6800 000.0000 0000000 000.0000 000.0000 15.19940000    00"
]

# Load timescale
ts = load.timescale()

# Load the satellite from TLE
satellite = EarthSatellite(tle_lines[0], tle_lines[1], 'QUARC', ts)
satellite_name = satellite.name

start_time = ts.utc(2014, 1, 23)
end_time = start_time + timedelta(days=3) # ts.utc(datetime.utcnow() + timedelta(days=1))  # Compute passes for the next 1 day

my_location = wgs84.latlon(latitude_degrees=37.7749, longitude_degrees=-122.4194)  # San Francisco, CA

# Calculate visibility times
time_of_interest = ts.now()
t, events = satellite.find_events(my_location, start_time, end_time)
event_names = 'rise above 10°', 'culminate', 'set below 10°'
for ti, event in zip(t, events):
    name = event_names[event]
    print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)


