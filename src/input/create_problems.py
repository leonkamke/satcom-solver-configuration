import random
import json
import uuid
import numpy as np
from .quarc_data_generation import get_quarc_satellite_passes

problem_instances_path = './src/input/data/problem_instances.json'


class ServiceTarget:
    def __init__(self, id, priority, nodeId, requestedOperation):
        self.id = id
        self.priority = priority
        self.nodeId = nodeId
        self.requestedOperation = requestedOperation

    def __repr__(self):
        return (f"ServiceTarget(id={self.id}, nodeId={self.nodeId}, "
                f"priority={self.priority}, requestedOperation={self.requestedOperation})")

    def to_dict(self):
        return self.__dict__
    

def get_service_targets(number_ground_terminals):
    service_targets_dict_list = []
    serviceTargetId = 1
    for id in range(1, number_ground_terminals+1):
        x = random.randint(1, 100)
        if x <= 80:
            priority = round(random.uniform(0.5, 1), 2)
            x = random.randint(1, 100)
            requestedOperation = None
            if x < 50:
                requestedOperation = "QKD"
            else:
                requestedOperation = "OPTICAL_ONLY"
            service_targets_dict_list.append(ServiceTarget(serviceTargetId, priority, id, requestedOperation).to_dict())
            serviceTargetId += 1
        x = random.randint(1, 100)
        if x <= 80:
            priority = round(random.uniform(0.5, 1), 2)
            x = random.randint(1, 100)
            requestedOperation = None
            if x < 50:
                requestedOperation = "QKD"
            else:
                requestedOperation = "OPTICAL_ONLY"
            service_targets_dict_list.append(ServiceTarget(serviceTargetId, priority, id, requestedOperation).to_dict())
            serviceTargetId += 1

    return service_targets_dict_list

def save_problem_instances_to_json(problem_instances, file_name):
    with open(file_name, 'w') as f:
        json.dump(problem_instances, f, indent=4, default=str)

"""# ----- main ------
parameters = {
    "number_nodes": 100,
    "number_orbits": 24,
    "duration_orbit": 120,  # duration for an orbit in minutes
    "power_threshold": 200
}
save_test_scenarios_to_json(parameters, problem_instances_path, 1)"""


# QUARC Ground Terminal locations in UK
quarc_ground_terminals = {
    1: {"lat": 61, "lon": -1, "alt": 0},
    2: {"lat": 60, "lon": -1, "alt": 0},
    3: {"lat": 59, "lon": -3, "alt": 0},
    4: {"lat": 58, "lon": -4, "alt": 0},
    5: {"lat": 58, "lon": -5, "alt": 0},
    6: {"lat": 58, "lon": -7, "alt": 0},
    7: {"lat": 57, "lon": -3, "alt": 0},
    8: {"lat": 57, "lon": -4, "alt": 0},
    9: {"lat": 57, "lon": -5, "alt": 0},
    10: {"lat": 57, "lon": -6, "alt": 0},
    11: {"lat": 56, "lon": -3, "alt": 0},
    12: {"lat": 56, "lon": -4, "alt": 0},
    13: {"lat": 56, "lon": -5, "alt": 0},
    14: {"lat": 56, "lon": -6, "alt": 0},
    15: {"lat": 55, "lon": -2, "alt": 0},
    16: {"lat": 55, "lon": -3, "alt": 0},
    17: {"lat": 55, "lon": -4, "alt": 0},
    18: {"lat": 55, "lon": -5, "alt": 0},
    19: {"lat": 55, "lon": -6, "alt": 0},
    20: {"lat": 55, "lon": -7, "alt": 0},
    21: {"lat": 55, "lon": -4, "alt": 0},
    22: {"lat": 54, "lon": -1, "alt": 0},
    23: {"lat": 54, "lon": -2, "alt": 0},
    24: {"lat": 54, "lon": -3, "alt": 0},
    25: {"lat": 54, "lon": -6, "alt": 0},
    26: {"lat": 53, "lon": 1, "alt": 0},
    27: {"lat": 53, "lon": 0, "alt": 0},
    28: {"lat": 53, "lon": -1, "alt": 0},
    29: {"lat": 53, "lon": -2, "alt": 0},
    30: {"lat": 53, "lon": -3, "alt": 0},
    31: {"lat": 53, "lon": -4, "alt": 0},
    32: {"lat": 52, "lon": 1, "alt": 0},
    33: {"lat": 52, "lon": 0, "alt": 0},
    34: {"lat": 52, "lon": -1, "alt": 0},
    35: {"lat": 52, "lon": -2, "alt": 0},
    36: {"lat": 52, "lon": -3, "alt": 0},
    37: {"lat": 52, "lon": -4, "alt": 0},
    38: {"lat": 51, "lon": 1, "alt": 0},
    39: {"lat": 51, "lon": 0, "alt": 0},
    40: {"lat": 51, "lon": -1, "alt": 0},
    41: {"lat": 51, "lon": -2, "alt": 0},
    42: {"lat": 51, "lon": -3, "alt": 0},
    43: {"lat": 51, "lon": -4, "alt": 0},
}


test_ground_terminals = {
    1: {"lat": 61, "lon": -1, "alt": 0},
    2: {"lat": 60, "lon": -1, "alt": 0},
}

def generate_problem_instance(coverage_start, coverage_end, ground_terminals, step_duration = 10, min_elevation_angle = 20):
    # Calculate satellite passes over ground terminals for QUARC mission
    satellite_passes_dict_list = get_quarc_satellite_passes(ground_terminals, coverage_start, coverage_end, step_duration, min_elevation_angle)

    # Calculate service targets
    service_targets_dict_list = get_service_targets(len(ground_terminals))

    return {
        "problem_instance_id": str(uuid.uuid4()),
        "coverage_start": str(coverage_start),
        "coverage_end": str(coverage_end),
        "min_elevation_angle": min_elevation_angle,
        "step_duration": step_duration,
        "number_ground_terminals": len(ground_terminals),
        "number_satellite_passes": len(satellite_passes_dict_list),
        "number_service_targets": len(service_targets_dict_list),
        "satellite_passes": satellite_passes_dict_list,
        "service_targets": service_targets_dict_list
    }


coverage_start = np.datetime64('2024-02-12T00:00:00')
coverage_end = np.datetime64('2024-02-13T00:00:00')
step_duration = 20
min_elevation_angle = 20

problem_instances = [generate_problem_instance(coverage_start, coverage_end, quarc_ground_terminals, step_duration, min_elevation_angle)]
save_problem_instances_to_json(problem_instances, problem_instances_path)