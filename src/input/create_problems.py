import random
import json
import uuid
import numpy as np
from .quarc_data_generation import get_quarc_satellite_passes

problem_instances_path = './src/input/data/problem_instances.json'

# Locations for ground terminals in europe
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
 #   47: {"lat": 63.4305, "lon": 10.3951, "alt": 10},  # Trondheim, Norway
 #   48: {"lat": 59.8586, "lon": 17.6389, "alt": 15},  # Uppsala, Sweden
 #   49: {"lat": 55.4038, "lon": 10.4024, "alt": 5},   # Odense, Denmark
 #   50: {"lat": 54.3520, "lon": 18.6466, "alt": 7},   # Gdansk, Poland
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


coverage_start = np.datetime64('2024-11-01T00:00:00')
coverage_end = np.datetime64('2024-11-01T03:00:00')
step_duration = 2
min_elevation_angle = 10
number_app_contexts_per_node = 15

problem_instances = [generate_problem_instance(coverage_start, coverage_end, europe_ground_terminals, step_duration, min_elevation_angle, number_app_contexts_per_node)]
save_problem_instances_to_json(problem_instances, './src/input/data/problem_instance_europe_jan_3h.json')
