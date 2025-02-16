import random
import json
import uuid
import numpy as np
from .quarc_data_generation import get_quarc_satellite_passes

problem_instances_path = './src/input/data/problem_instances.json'


# QUARC Ground Terminal locations in UK
quarc_ground_terminals = {
    0: {"lat": 61, "lon": -1, "alt": 0},
    1: {"lat": 60, "lon": -1, "alt": 0},
    2: {"lat": 59, "lon": -3, "alt": 0},
    3: {"lat": 58, "lon": -4, "alt": 0},
    4: {"lat": 58, "lon": -5, "alt": 0},
    5: {"lat": 58, "lon": -7, "alt": 0},
    6: {"lat": 57, "lon": -3, "alt": 0},
    7: {"lat": 57, "lon": -4, "alt": 0},
    8: {"lat": 57, "lon": -5, "alt": 0},
    9: {"lat": 57, "lon": -6, "alt": 0},
    10: {"lat": 56, "lon": -3, "alt": 0},
    11: {"lat": 56, "lon": -4, "alt": 0},
    12: {"lat": 56, "lon": -5, "alt": 0},
    13: {"lat": 56, "lon": -6, "alt": 0},
    14: {"lat": 55, "lon": -2, "alt": 0},
    15: {"lat": 55, "lon": -3, "alt": 0},
    16: {"lat": 55, "lon": -4, "alt": 0},
    17: {"lat": 55, "lon": -5, "alt": 0},
    18: {"lat": 55, "lon": -6, "alt": 0},
    19: {"lat": 55, "lon": -7, "alt": 0},
    20: {"lat": 55, "lon": -4, "alt": 0},
    21: {"lat": 54, "lon": -1, "alt": 0},
    22: {"lat": 54, "lon": -2, "alt": 0},
    23: {"lat": 54, "lon": -3, "alt": 0},
    24: {"lat": 54, "lon": -6, "alt": 0},
    25: {"lat": 53, "lon": 1, "alt": 0},
    26: {"lat": 53, "lon": 0, "alt": 0},
    27: {"lat": 53, "lon": -1, "alt": 0},
    28: {"lat": 53, "lon": -2, "alt": 0},
    29: {"lat": 53, "lon": -3, "alt": 0},
    30: {"lat": 53, "lon": -4, "alt": 0},
    31: {"lat": 52, "lon": 1, "alt": 0},
    32: {"lat": 52, "lon": 0, "alt": 0},
    33: {"lat": 52, "lon": -1, "alt": 0},
    34: {"lat": 52, "lon": -2, "alt": 0},
    35: {"lat": 52, "lon": -3, "alt": 0},
    36: {"lat": 52, "lon": -4, "alt": 0},
    37: {"lat": 51, "lon": 1, "alt": 0},
    38: {"lat": 51, "lon": 0, "alt": 0},
    39: {"lat": 51, "lon": -1, "alt": 0},
    40: {"lat": 51, "lon": -2, "alt": 0},
    41: {"lat": 51, "lon": -3, "alt": 0},
    42: {"lat": 51, "lon": -4, "alt": 0},

    43: {"lat": 51.5074, "lon": -0.1278, "alt": 0},  # London
    44: {"lat": 52.2053, "lon": 0.1218, "alt": 0},   # Cambridge
    45: {"lat": 52.4862, "lon": -1.8904, "alt": 0},  # Birmingham
    46: {"lat": 53.4808, "lon": -2.2426, "alt": 0},  # Manchester
    47: {"lat": 53.4084, "lon": -2.9916, "alt": 0},  # Liverpool
    48: {"lat": 53.8008, "lon": -1.5491, "alt": 0},  # Leeds
    49: {"lat": 54.9783, "lon": -1.6174, "alt": 0},  # Newcastle
    50: {"lat": 55.9533, "lon": -3.1883, "alt": 0},  # Edinburgh
    51: {"lat": 57.1497, "lon": -2.0943, "alt": 0},  # Aberdeen
    52: {"lat": 56.4907, "lon": -4.2026, "alt": 0},  # Stirling
    53: {"lat": 53.0027, "lon": -2.1794, "alt": 0},  # Stoke-on-Trent
    54: {"lat": 51.7520, "lon": -1.2577, "alt": 0},  # Oxford
    55: {"lat": 50.8225, "lon": -0.1372, "alt": 0},  # Brighton
    56: {"lat": 50.3755, "lon": -4.1427, "alt": 0},  # Plymouth
    57: {"lat": 51.4545, "lon": -2.5879, "alt": 0},  # Bristol
    58: {"lat": 52.9299, "lon": -1.2503, "alt": 0},  # Derby
    59: {"lat": 52.1917, "lon": -2.22, "alt": 0},    # Worcester
    60: {"lat": 50.7192, "lon": -1.8808, "alt": 0},  # Bournemouth
    61: {"lat": 54.8969, "lon": -2.9387, "alt": 0},  # Carlisle
    62: {"lat": 51.5584, "lon": -0.0659, "alt": 0},  # Hackney
    63: {"lat": 50.8467, "lon": -1.3044, "alt": 0},  # Portsmouth
    64: {"lat": 51.3811, "lon": -2.359, "alt": 0},   # Bath
    65: {"lat": 50.7351, "lon": -1.916, "alt": 0},   # Christchurch
    66: {"lat": 52.6289, "lon": 1.2994, "alt": 0},   # Norwich
    67: {"lat": 52.2405, "lon": -0.9027, "alt": 0},  # Northampton
    68: {"lat": 51.8164, "lon": -1.2822, "alt": 0},  # Bicester
    69: {"lat": 53.8008, "lon": -1.5546, "alt": 0},  # Huddersfield
    70: {"lat": 52.4068, "lon": -1.5197, "alt": 0},  # Coventry
    71: {"lat": 52.5852, "lon": -2.1222, "alt": 0},  # Wolverhampton
    72: {"lat": 53.3916, "lon": -2.1193, "alt": 0},  # Stockport
    73: {"lat": 53.2327, "lon": -0.5392, "alt": 0},  # Lincoln
    74: {"lat": 54.2641, "lon": -0.4092, "alt": 0},  # Scarborough
    75: {"lat": 50.9417, "lon": -1.4044, "alt": 0},  # Winchester
    76: {"lat": 53.3417, "lon": -3.4927, "alt": 0},  # Rhyl
    77: {"lat": 53.0959, "lon": -2.2206, "alt": 0},  # Crewe
    78: {"lat": 54.5554, "lon": -1.2532, "alt": 0},  # Middlesbrough
    79: {"lat": 52.6221, "lon": -1.1291, "alt": 0},  # Leicester
    80: {"lat": 51.5842, "lon": -0.3535, "alt": 0},  # Watford
    81: {"lat": 52.4777, "lon": -1.8993, "alt": 0},  # Solihull
    82: {"lat": 51.6244, "lon": -0.4141, "alt": 0},  # Harrow
    83: {"lat": 53.0264, "lon": -1.2516, "alt": 0},  # Mansfield
    84: {"lat": 50.9998, "lon": -2.1086, "alt": 0},  # Salisbury
    85: {"lat": 51.4550, "lon": -0.9691, "alt": 0},  # Reading
    86: {"lat": 53.3762, "lon": -1.4679, "alt": 0},  # Sheffield
    87: {"lat": 52.9122, "lon": -1.4691, "alt": 0},  # Nottingham
    88: {"lat": 53.3944, "lon": -3.0149, "alt": 0},  # Wallasey
    89: {"lat": 52.3736, "lon": 0.1501, "alt": 0},   # Newmarket
    90: {"lat": 54.9067, "lon": -2.9362, "alt": 0},  # Penrith
    91: {"lat": 50.7836, "lon": -1.8315, "alt": 0},  # New Forest
    92: {"lat": 54.5719, "lon": -1.2347, "alt": 0},  # Redcar
    93: {"lat": 54.3503, "lon": -2.9156, "alt": 0},  # Kendal
    94: {"lat": 55.0051, "lon": -1.4216, "alt": 0},  # Tynemouth
    95: {"lat": 51.3365, "lon": -0.2676, "alt": 0},  # Epsom
    96: {"lat": 51.8892, "lon": -0.4203, "alt": 0},  # St Albans
    97: {"lat": 52.0406, "lon": -0.7594, "alt": 0},  # Milton Keynes
    98: {"lat": 53.7974, "lon": -1.4806, "alt": 0},  # Wakefield
    99: {"lat": 50.9106, "lon": -1.4043, "alt": 0},  # Southampton
    100: {"lat": 51.4014, "lon": -0.3349, "alt": 0},  # Kingston upon Thames
}

europe_ground_terminals = {
    0: {"lat": 51.5074, "lon": -0.1278, "alt": 35},   # London, England
    1: {"lat": 48.8566, "lon": 2.3522, "alt": 35},    # Paris, France
    2: {"lat": 52.5200, "lon": 13.4050, "alt": 34},   # Berlin, Germany
    3: {"lat": 41.9028, "lon": 12.4964, "alt": 21},   # Rome, Italy
    4: {"lat": 40.4168, "lon": -3.7038, "alt": 667},  # Madrid, Spain
    5: {"lat": 50.0755, "lon": 14.4378, "alt": 200},  # Prague, Czech Republic
    6: {"lat": 47.4979, "lon": 19.0402, "alt": 96},   # Budapest, Hungary
    7: {"lat": 59.3293, "lon": 18.0686, "alt": 28},   # Stockholm, Sweden
    8: {"lat": 60.1695, "lon": 24.9354, "alt": 16},   # Helsinki, Finland
    9: {"lat": 55.6761, "lon": 12.5683, "alt": 1},    # Copenhagen, Denmark
    10: {"lat": 54.6872, "lon": 25.2797, "alt": 112}, # Vilnius, Lithuania
    11: {"lat": 56.9496, "lon": 24.1052, "alt": 6},   # Riga, Latvia
    12: {"lat": 53.9006, "lon": 27.5590, "alt": 220}, # Minsk, Belarus
    13: {"lat": 50.8503, "lon": 4.3517, "alt": 13},   # Brussels, Belgium
    14: {"lat": 48.2082, "lon": 16.3738, "alt": 193}, # Vienna, Austria
    15: {"lat": 46.2044, "lon": 6.1432, "alt": 375},  # Geneva, Switzerland
    16: {"lat": 42.6977, "lon": 23.3219, "alt": 550}, # Sofia, Bulgaria
    17: {"lat": 44.4268, "lon": 26.1025, "alt": 70},  # Bucharest, Romania
    18: {"lat": 45.8150, "lon": 15.9819, "alt": 122}, # Zagreb, Croatia
    19: {"lat": 43.8563, "lon": 18.4131, "alt": 500}, # Sarajevo, Bosnia and Herzegovina
    20: {"lat": 42.4410, "lon": 19.2621, "alt": 107}, # Podgorica, Montenegro
    21: {"lat": 41.9981, "lon": 21.4254, "alt": 240}, # Skopje, North Macedonia
    22: {"lat": 39.9208, "lon": 32.8541, "alt": 938}, # Ankara, Turkey
    23: {"lat": 37.9838, "lon": 23.7275, "alt": 70},  # Athens, Greece
    24: {"lat": 45.4642, "lon": 9.1900, "alt": 120},  # Milan, Italy
    25: {"lat": 44.8381, "lon": -0.5792, "alt": 7},   # Bordeaux, France
    26: {"lat": 41.3851, "lon": 2.1734, "alt": 12},   # Barcelona, Spain
    27: {"lat": 43.7102, "lon": 7.2620, "alt": 10},   # Nice, France
    28: {"lat": 49.6117, "lon": 6.1319, "alt": 289},  # Luxembourg City, Luxembourg
    29: {"lat": 51.2093, "lon": 3.2247, "alt": 8},    # Bruges, Belgium
    30: {"lat": 53.3498, "lon": -6.2603, "alt": 20},  # Dublin, Ireland
    31: {"lat": 55.9533, "lon": -3.1883, "alt": 47},  # Edinburgh, Scotland
    32: {"lat": 54.9783, "lon": -1.6174, "alt": 46},  # Newcastle, England
    33: {"lat": 55.8642, "lon": -4.2518, "alt": 20},  # Glasgow, Scotland
    34: {"lat": 47.3769, "lon": 8.5417, "alt": 408},  # Zurich, Switzerland
    35: {"lat": 47.0707, "lon": 15.4395, "alt": 353}, # Graz, Austria
    36: {"lat": 49.4521, "lon": 11.0767, "alt": 309}, # Nuremberg, Germany
    37: {"lat": 50.1109, "lon": 8.6821, "alt": 112},  # Frankfurt, Germany
    38: {"lat": 45.7607, "lon": 4.8357, "alt": 173},  # Lyon, France
    39: {"lat": 44.4949, "lon": 11.3426, "alt": 54},  # Bologna, Italy
    40: {"lat": 40.8518, "lon": 14.2681, "alt": 17},  # Naples, Italy
    41: {"lat": 43.6047, "lon": 1.4442, "alt": 146},  # Toulouse, France
    42: {"lat": 51.2194, "lon": 4.4025, "alt": 8},    # Antwerp, Belgium
    43: {"lat": 51.5072, "lon": 0.1276, "alt": 10},   # Brighton, England
    44: {"lat": 57.7089, "lon": 11.9746, "alt": 12},  # Gothenburg, Sweden
    45: {"lat": 60.3932, "lon": 5.3242, "alt": 20},   # Bergen, Norway
    46: {"lat": 59.9139, "lon": 10.7522, "alt": 23},  # Oslo, Norway
#    47: {"lat": 63.4305, "lon": 10.3951, "alt": 10},  # Trondheim, Norway
#    48: {"lat": 59.8586, "lon": 17.6389, "alt": 15},  # Uppsala, Sweden
#    49: {"lat": 55.4038, "lon": 10.4024, "alt": 5},   # Odense, Denmark
#    50: {"lat": 54.3520, "lon": 18.6466, "alt": 7},   # Gdansk, Poland
 #   51: {"lat": 52.2297, "lon": 21.0122, "alt": 113}, # Warsaw, Poland
 #   52: {"lat": 50.0647, "lon": 19.9450, "alt": 219}, # Krakow, Poland
 #   53: {"lat": 52.4064, "lon": 16.9252, "alt": 60},  # Poznan, Poland
 #   54: {"lat": 53.0138, "lon": 18.5984, "alt": 67},  # Torun, Poland
 #   55: {"lat": 52.5204, "lon": 4.8952, "alt": 2},    # Amsterdam, Netherlands
 #   56: {"lat": 51.9244, "lon": 4.4777, "alt": 0},    # Rotterdam, Netherlands
 #   57: {"lat": 50.8514, "lon": 5.6909, "alt": 45},   # Maastricht, Netherlands
 #   58: {"lat": 51.2277, "lon": 6.7735, "alt": 45},   # Dusseldorf, Germany
 #   59: {"lat": 51.5136, "lon": 7.4653, "alt": 60},   # Dortmund, Germany
 #   60: {"lat": 53.5511, "lon": 9.9937, "alt": 6},    # Hamburg, Germany
 #   61: {"lat": 53.0758, "lon": 8.8072, "alt": 12},   # Bremen, Germany
 #   62: {"lat": 48.1351, "lon": 11.5820, "alt": 519}, # Munich, Germany
 #   63: {"lat": 47.5677, "lon": 7.5970, "alt": 244},  # Basel, Switzerland
 #   64: {"lat": 45.1885, "lon": 5.7245, "alt": 212},  # Grenoble, France
 #   65: {"lat": 43.2965, "lon": 5.3698, "alt": 10},   # Marseille, France
 #   66: {"lat": 44.8378, "lon": 20.4216, "alt": 117}, # Belgrade, Serbia
 #   67: {"lat": 42.8794, "lon": 20.8756, "alt": 609}, # Prizren, Kosovo
 #   68: {"lat": 41.3275, "lon": 19.8189, "alt": 110}, # Tirana, Albania
 #   69: {"lat": 42.5624, "lon": 1.5333, "alt": 1023}, # Andorra la Vella, Andorra
 #   70: {"lat": 46.0569, "lon": 14.5058, "alt": 298}, # Ljubljana, Slovenia
 #   71: {"lat": 47.5008, "lon": 19.0567, "alt": 104}, # Debrecen, Hungary
 #   72: {"lat": 50.0750, "lon": 19.9030, "alt": 281}, # Katowice, Poland
 #   73: {"lat": 46.7667, "lon": 23.5833, "alt": 360}, # Cluj-Napoca, Romania
 #   74: {"lat": 45.6486, "lon": 25.6062, "alt": 600}, # Brasov, Romania
 #   75: {"lat": 40.1786, "lon": 44.5126, "alt": 989}, # Yerevan, Armenia
 #   76: {"lat": 38.0194, "lon": 23.8439, "alt": 125}, # Kifisia, Greece
 #   77: {"lat": 36.7213, "lon": -4.4214, "alt": 11},  # Malaga, Spain
 #   78: {"lat": 37.9922, "lon": -1.1307, "alt": 43},  # Murcia, Spain
 #   79: {"lat": 43.2627, "lon": -2.9253, "alt": 19},  # Bilbao, Spain
 #   80: {"lat": 39.4699, "lon": -0.3763, "alt": 15},  # Valencia, Spain
 #   81: {"lat": 38.7169, "lon": -9.1390, "alt": 100}, # Lisbon, Portugal
 #   82: {"lat": 41.1496, "lon": -8.6109, "alt": 104}, # Porto, Portugal
 #   83: {"lat": 38.7369, "lon": -9.1390, "alt": 12},  # Faro, Portugal
 #   84: {"lat": 62.2426, "lon": 25.7473, "alt": 117}, # Jyvaskyla, Finland
 #   85: {"lat": 58.3806, "lon": 26.7251, "alt": 57},  # Tartu, Estonia
 #   86: {"lat": 56.3322, "lon": 43.9978, "alt": 171}, # Nizhny Novgorod, Russia
 #   87: {"lat": 55.7558, "lon": 37.6173, "alt": 156}, # Moscow, Russia
 #   88: {"lat": 59.9343, "lon": 30.3351, "alt": 20},  # Saint Petersburg, Russia
 #   89: {"lat": 53.1959, "lon": 50.1007, "alt": 160}, # Samara, Russia
 #   90: {"lat": 48.2920, "lon": 25.9358, "alt": 248}, # Chernivtsi, Ukraine
 #   91: {"lat": 46.4825, "lon": 30.7233, "alt": 50},  # Odessa, Ukraine
 #   92: {"lat": 50.4017, "lon": 30.2525, "alt": 179}, # Kyiv, Ukraine
 #   93: {"lat": 49.5535, "lon": 25.5948, "alt": 320}, # Ternopil, Ukraine
 #   94: {"lat": 45.2631, "lon": 19.8310, "alt": 82},  # Novi Sad, Serbia
 #   95: {"lat": 41.7208, "lon": 44.7831, "alt": 450}, # Tbilisi, Georgia
 #   96: {"lat": 38.2484, "lon": 21.7346, "alt": 15},  # Patras, Greece
 #   97: {"lat": 57.1424, "lon": -2.0927, "alt": 65},  # Aberdeen, Scotland
 #   98: {"lat": 60.4720, "lon": 8.4689, "alt": 140},  # Drammen, Norway
 #   99: {"lat": 51.2195, "lon": 22.5684, "alt": 174}, # Lublin, Poland
 #   100: {"lat": 41.6615, "lon": -0.8949, "alt": 199}, # Zaragoza, Spain
 #   101: {"lat": 64.1355, "lon": -21.8954, "alt": 61}, # Reykjavik, Iceland
 #   102: {"lat": 49.1952, "lon": 16.6070, "alt": 235}, # Brno, Czech Republic
 #   103: {"lat": 52.6298, "lon": -1.1398, "alt": 55},  # Leicester, England
 #   104: {"lat": 47.2228, "lon": 39.7186, "alt": 90},  # Rostov-on-Don, Russia
 #   105: {"lat": 46.057, "lon": 14.5058, "alt": 287},  # Ljubana, Serbia 
 #   106: {"lat": 42.6675, "lon": 21.1662, "alt": 580}, # Pristina, Kosovo
 #   107: {"lat": 51.7519, "lon": -1.2578, "alt": 72},  # Oxford, England
 #   108: {"lat": 54.6862, "lon": -1.2124, "alt": 38},  # Durham, England
 #   109: {"lat": 56.1629, "lon": 10.2039, "alt": 8},   # Aarhus, Denmark
 #   110: {"lat": 51.4502, "lon": 5.4714, "alt": 18},   # Eindhoven, Netherlands
 #   111: {"lat": 42.3489, "lon": -3.6829, "alt": 300}, # Burgos, Spain
 #   112: {"lat": 50.7359, "lon": 7.1007, "alt": 60},   # Bonn, Germany
 #   113: {"lat": 59.437, "lon": 24.7535, "alt": 45},   # Tallinn, Estonia
 #   114: {"lat": 51.1657, "lon": 10.4515, "alt": 180}, # Dresden, Germany
 #   115: {"lat": 40.6401, "lon": 22.9444, "alt": 6},   # Thessaloniki, Greece""
}

world_ground_terminals = {
    0: {"lat": 40.7128, "lon": -74.0060, "alt": 0},  # New York, USA
    1: {"lat": 34.0522, "lon": -118.2437, "alt": 0},  # Los Angeles, USA
    2: {"lat": 48.8566, "lon": 2.3522, "alt": 0},  # Paris, France
    3: {"lat": 51.5074, "lon": -0.1278, "alt": 0},  # London, UK
    4: {"lat": 35.6895, "lon": 139.6917, "alt": 0},  # Tokyo, Japan
    5: {"lat": -33.8688, "lon": 151.2093, "alt": 0},  # Sydney, Australia
    6: {"lat": -22.9068, "lon": -43.1729, "alt": 0},  # Rio de Janeiro, Brazil
    7: {"lat": 55.7558, "lon": 37.6173, "alt": 0},  # Moscow, Russia
    8: {"lat": 28.6139, "lon": 77.2090, "alt": 0},  # New Delhi, India
    9: {"lat": -1.2921, "lon": 36.8219, "alt": 0},  # Nairobi, Kenya
    10: {"lat": -34.6037, "lon": -58.3816, "alt": 0},  # Buenos Aires, Argentina
    11: {"lat": 19.4326, "lon": -99.1332, "alt": 0},  # Mexico City, Mexico
    12: {"lat": 37.7749, "lon": -122.4194, "alt": 0},  # San Francisco, USA
    13: {"lat": 1.3521, "lon": 103.8198, "alt": 0},  # Singapore, Singapore
    14: {"lat": 31.2304, "lon": 121.4737, "alt": 0},  # Shanghai, China
    15: {"lat": 41.9028, "lon": 12.4964, "alt": 0},  # Rome, Italy
    16: {"lat": -26.2041, "lon": 28.0473, "alt": 0},  # Johannesburg, South Africa
    17: {"lat": 39.9042, "lon": 116.4074, "alt": 0},  # Beijing, China
    18: {"lat": -12.0464, "lon": -77.0428, "alt": 0},  # Lima, Peru
    19: {"lat": 43.6511, "lon": -79.3470, "alt": 0},  # Toronto, Canada
    20: {"lat": 35.6897, "lon": 51.3890, "alt": 0},  # Tehran, Iran
    21: {"lat": 59.3293, "lon": 18.0686, "alt": 0},  # Stockholm, Sweden
    22: {"lat": -37.8136, "lon": 144.9631, "alt": 0},  # Melbourne, Australia
    23: {"lat": -6.2088, "lon": 106.8456, "alt": 0},  # Jakarta, Indonesia
    24: {"lat": 3.1390, "lon": 101.6869, "alt": 0},  # Kuala Lumpur, Malaysia
    25: {"lat": -41.2865, "lon": 174.7762, "alt": 0},  # Wellington, New Zealand
    26: {"lat": 40.4168, "lon": -3.7038, "alt": 0},  # Madrid, Spain
    27: {"lat": 52.3676, "lon": 4.9041, "alt": 0},  # Amsterdam, Netherlands
    28: {"lat": -15.7942, "lon": -47.8822, "alt": 0},  # Brasília, Brazil
    29: {"lat": 30.0444, "lon": 31.2357, "alt": 0},  # Cairo, Egypt
    30: {"lat": -29.8587, "lon": 31.0218, "alt": 0},  # Durban, South Africa
    31: {"lat": 34.6937, "lon": 135.5023, "alt": 0},  # Osaka, Japan
    32: {"lat": -4.4419, "lon": 15.2663, "alt": 0},  # Kinshasa, DR Congo
    33: {"lat": 60.1699, "lon": 24.9384, "alt": 0},  # Helsinki, Finland
    34: {"lat": 45.5017, "lon": -73.5673, "alt": 0},  # Montreal, Canada
    35: {"lat": 25.276987, "lon": 55.296249, "alt": 0},  # Dubai, UAE
    36: {"lat": -3.3731, "lon": 29.9189, "alt": 0},  # Bujumbura, Burundi
    37: {"lat": -35.2820, "lon": 149.1287, "alt": 0},  # Canberra, Australia
    38: {"lat": -23.5505, "lon": -46.6333, "alt": 0},  # São Paulo, Brazil
    39: {"lat": 56.1304, "lon": -106.3468, "alt": 0},  # Central Canada
    40: {"lat": 14.5995, "lon": 120.9842, "alt": 0},  # Manila, Philippines
    41: {"lat": 64.1355, "lon": -21.8954, "alt": 0},  # Reykjavik, Iceland
    42: {"lat": 13.7563, "lon": 100.5018, "alt": 0},  # Bangkok, Thailand
    43: {"lat": 50.0755, "lon": 14.4378, "alt": 0},  # Prague, Czech Republic
    44: {"lat": -24.9916, "lon": 135.2254, "alt": 0},  # Alice Springs, Australia
    45: {"lat": -62.4663, "lon": -60.8000, "alt": 0},  # Antarctic Research Base
    46: {"lat": 19.0760, "lon": 72.8777, "alt": 0},  # Mumbai, India
    47: {"lat": 53.3498, "lon": -6.2603, "alt": 0},  # Dublin, Ireland
    48: {"lat": -54.8019, "lon": -68.3029, "alt": 0},  # Ushuaia, Argentina
    49: {"lat": 71.2906, "lon": -156.7886, "alt": 0},  # Utqiaġvik (Barrow), USA
    50: {"lat": -25.6953, "lon": -54.4367, "alt": 0},  # Iguazu, Brazil
    51: {"lat": 55.6761, "lon": 12.5683, "alt": 0},  # Copenhagen, Denmark
    52: {"lat": 54.6872, "lon": 25.2797, "alt": 0},  # Vilnius, Lithuania
    53: {"lat": 64.1814, "lon": -51.7216, "alt": 0},  # Nuuk, Greenland
    54: {"lat": 28.7041, "lon": 77.1025, "alt": 0},  # Delhi, India
    55: {"lat": 27.7172, "lon": 85.3240, "alt": 0},  # Kathmandu, Nepal
    56: {"lat": 6.5244, "lon": 3.3792, "alt": 0},  # Lagos, Nigeria
    57: {"lat": 4.0511, "lon": 9.7679, "alt": 0},  # Douala, Cameroon
    58: {"lat": -53.1638, "lon": -70.9171, "alt": 0},  # Punta Arenas, Chile
    59: {"lat": 25.0343, "lon": -77.3963, "alt": 0},  # Nassau, Bahamas
    60: {"lat": -17.8249, "lon": 31.0532, "alt": 0},  # Harare, Zimbabwe
    61: {"lat": -9.4431, "lon": -40.4305, "alt": 0},  # Bahia, Brazil
    62: {"lat": 66.8390, "lon": -50.7197, "alt": 0},  # Tasiilaq, Greenland
    63: {"lat": 10.6400, "lon": -61.5189, "alt": 0},  # Port of Spain, Trinidad
    64: {"lat": 24.8607, "lon": 67.0011, "alt": 0},  # Karachi, Pakistan
    65: {"lat": 40.1106, "lon": -88.2073, "alt": 0},  # Champaign, USA
    66: {"lat": 47.3769, "lon": 8.5417, "alt": 0},  # Zurich, Switzerland
    67: {"lat": -18.8792, "lon": 47.5079, "alt": 0},  # Antananarivo, Madagascar
    68: {"lat": 35.6892, "lon": 139.6917, "alt": 0},  # Sapporo, Japan
    69: {"lat": -8.4095, "lon": 115.1889, "alt": 0},  # Bali, Indonesia
    70: {"lat": 55.9533, "lon": -3.1883, "alt": 0},  # Edinburgh, Scotland
    71: {"lat": 21.0285, "lon": 105.8542, "alt": 0},  # Hanoi, Vietnam
    72: {"lat": 38.7223, "lon": -9.1393, "alt": 0},  # Lisbon, Portugal
    73: {"lat": 42.3601, "lon": -71.0589, "alt": 0},  # Boston, USA
    74: {"lat": 35.0116, "lon": 135.7681, "alt": 0},  # Kyoto, Japan
    75: {"lat": 25.7617, "lon": -80.1918, "alt": 0},  # Miami, USA
    76: {"lat": 50.8503, "lon": 4.3517, "alt": 0},  # Brussels, Belgium
    77: {"lat": 59.4370, "lon": 24.7536, "alt": 0},  # Tallinn, Estonia
    78: {"lat": 41.0082, "lon": 28.9784, "alt": 0},  # Istanbul, Turkey
    79: {"lat": 34.2257, "lon": -77.9447, "alt": 0},  # Wilmington, USA
    80: {"lat": 35.1167, "lon": -89.9500, "alt": 0},  # Memphis, USA
    81: {"lat": 47.4979, "lon": 19.0402, "alt": 0},  # Budapest, Hungary
    82: {"lat": -3.745, "lon": -38.523, "alt": 0},  # Fortaleza, Brazil
    83: {"lat": 43.7384, "lon": 7.4246, "alt": 0},  # Monaco
    84: {"lat": 13.0827, "lon": 80.2707, "alt": 0},  # Chennai, India
    85: {"lat": 55.8642, "lon": -4.2518, "alt": 0},  # Glasgow, Scotland
    86: {"lat": -12.4634, "lon": 130.8456, "alt": 0},  # Darwin, Australia
    87: {"lat": 37.9838, "lon": 23.7275, "alt": 0},  # Athens, Greece
    88: {"lat": 31.7683, "lon": 35.2137, "alt": 0},  # Jerusalem, Israel
    89: {"lat": 64.9631, "lon": -19.0208, "alt": 0},  # Thingvellir, Iceland
    90: {"lat": 38.5744, "lon": -121.4944, "alt": 0},  # Sacramento, USA
    91: {"lat": 33.7490, "lon": -84.3880, "alt": 0},  # Atlanta, USA
    92: {"lat": 46.2044, "lon": 6.1432, "alt": 0},  # Geneva, Switzerland
    93: {"lat": 15.5007, "lon": 32.5599, "alt": 0},  # Khartoum, Sudan
    94: {"lat": 39.7392, "lon": -104.9903, "alt": 0},  # Denver, USA
    95: {"lat": 36.1699, "lon": -115.1398, "alt": 0},  # Las Vegas, USA
}

class ServiceTarget:
    def __init__(self, id, applicationId, priority, nodeId, requestedOperation):
        self.id = id
        self.applicationId = applicationId
        self.priority = priority
        self.nodeId = nodeId
        self.requestedOperation = requestedOperation

    def __repr__(self):
        return (f"ServiceTarget(id={self.id}, applicationId={self.applicationId}, nodeId={self.nodeId}, "
                f"priority={self.priority}, requestedOperation={self.requestedOperation})")

    def to_dict(self):
        return self.__dict__
    

def get_service_targets(number_ground_terminals, number_application_contexts_per_node):
    service_targets_dict_list = []
    serviceTargetId = 0
    applicationId = 0
    for id in range(number_ground_terminals):
        for _ in range(number_application_contexts_per_node):
            priority = round(random.uniform(0.5, 1), 2)

            requestedOperation = "QKD"
            service_targets_dict_list.append(ServiceTarget(serviceTargetId, applicationId, priority, id, requestedOperation).to_dict())
            serviceTargetId += 1

            requestedOperation = "OPTICAL_ONLY"
            service_targets_dict_list.append(ServiceTarget(serviceTargetId, applicationId, priority, id, requestedOperation).to_dict())
            serviceTargetId += 1

            applicationId += 1

    return service_targets_dict_list

def save_problem_instances_to_json(problem_instances, file_name):
    with open(file_name, 'w') as f:
        json.dump(problem_instances, f, indent=4, default=str)

def generate_problem_instance(coverage_start, coverage_end, ground_terminals, step_duration = 10, min_elevation_angle = 20, number_app_contexts_per_node = 10):
    # Calculate satellite passes over ground terminals for QUARC mission
    satellite_passes_dict_list = get_quarc_satellite_passes(ground_terminals, coverage_start, coverage_end, step_duration, min_elevation_angle)

    # Calculate service targets
    service_targets_dict_list = get_service_targets(len(ground_terminals), number_app_contexts_per_node)

    return {
        "problem_instance_id": str(uuid.uuid4()),
        "coverage_start": str(coverage_start),
        "coverage_end": str(coverage_end),
        "min_elevation_angle": min_elevation_angle,
        "step_duration": step_duration,
        "number_ground_terminals": len(ground_terminals),
        "number_application_contexts_per_node": number_app_contexts_per_node,
        "number_satellite_passes": len(satellite_passes_dict_list),
        "number_service_targets": len(service_targets_dict_list),
        "satellite_passes": satellite_passes_dict_list,
        "service_targets": service_targets_dict_list
    }


coverage_start = np.datetime64('2024-07-12T00:00:00')
coverage_end = np.datetime64('2024-07-13T00:00:00')
step_duration = 10
min_elevation_angle = 10
number_app_contexts_per_node = 10

problem_instances = [generate_problem_instance(coverage_start, coverage_end, europe_ground_terminals, step_duration, min_elevation_angle, number_app_contexts_per_node)]
save_problem_instances_to_json(problem_instances, './src/input/data/problem_instance_europe_1day.json')
