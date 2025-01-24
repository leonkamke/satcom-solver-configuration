import random
import json
from datetime import datetime, timedelta
import numpy as np

problem_instances_path = './src/input/data/problem_instance.json'


class ServiceTarget:
    def __init__(self, id, priority, nodeId, requestedOperation):
        self.id = id
        self.priority = priority
        self.nodeId = nodeId
        self.requestedOperation = requestedOperation

    def to_dict(self):
        return self.__dict__
    

class SatellitePass:
    def __init__(self, id, nodeId, startTime, endTime, possibleOperation, achievableKeyVolume, orbitId):
        self.id = id
        self.nodeId = nodeId
        self.startTime = startTime
        self.endTime = endTime
        self.possibleOperation = possibleOperation
        self.achievableKeyVolume = achievableKeyVolume
        self.orbitId = orbitId

    def to_dict(self):
        return self.__dict__

def generate_random_service_targets(parameters):
    serviceTargets = []
    number_nodes = parameters["number_nodes"]
    serviceTargetId = 0
    for id in range(number_nodes):
        x = random.randint(1, 100)
        if x <= 80:
            priority = round(random.uniform(0.5, 1), 2)
            x = random.randint(1, 100)
            requestedOperation = None
            if x < 50:
                requestedOperation = "QKD"
            else:
                requestedOperation = "OPTICAL_ONLY"
            serviceTargets.append(ServiceTarget(serviceTargetId, priority, id, requestedOperation).to_dict())
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
            serviceTargets.append(ServiceTarget(serviceTargetId, priority, id, requestedOperation).to_dict())
            serviceTargetId += 1

    return serviceTargets


def generate_random_satellite_passes(parameters):
    schedule_length_minutes = parameters["number_orbits"] * parameters["duration_orbit"]
    satellitePasses = []
    
    # Divide the nodes into 4 parts
    nodes1, nodes2, nodes3, nodes4 = [], [], [], []
    number_nodes = parameters["number_nodes"]
    for i in range(number_nodes):
        if i < number_nodes / 4:
            nodes1.append(i)
        elif i < 2 * number_nodes / 4:
            nodes2.append(i)
        elif i < 3 * number_nodes / 4:
            nodes3.append(i)
        else:
            nodes4.append(i)
    
    # Create satellite passes
    id = 0
    for i in range(schedule_length_minutes):
        # With some given probability create a satellite pass
        x = random.randint(1, 100)
        if x <= 20:
            # Create satellite pass
            # Check which nodes are visible
            x = int(i / (parameters["duration_orbit"] / 4)) % 4
            visibleNodes = None
            
            if x == 0:
                visibleNodes = nodes1
            elif x == 1:
                visibleNodes = nodes2
            elif x == 2:
                visibleNodes = nodes3
            else:
                visibleNodes = nodes4
            
            # Get nodeId and orbitId
            nodeId = random.sample(visibleNodes, 1)[0]
            orbitId = i // parameters["duration_orbit"]
            
            # Create communicationType
            communicationType = None
            x = random.randint(1, 100)
            if x < 80:
                communicationType = "QKD"
            else:
                communicationType = "OPTICAL_ONLY"
            
            # Sample duration of normal distribution
            duration = int(np.random.normal(7, 1.8, 1)[0])
            if duration < 4:    
                duration = 4
                
            # Create start and end time
            startTime = datetime(2023, 1, 14)
            startTime += timedelta(minutes=i)
            endTime = startTime + timedelta(minutes=duration)
            startTime = startTime.isoformat()
            endTime = endTime.isoformat()
            
            # Sample achievableKeyVolume
            achievableKeyVolume = 0
            if communicationType == "QKD":
                keyRate = random.uniform(3, 6.5)    # range in kbit per second for melicius SatQKD
                achievableKeyVolume = int(keyRate * duration * 60)
                # achievableKeyVolume = int(np.random.normal(100, 10, 1)[0])

            # Sample required power (Calc power per second for both channels and multiply with duration)
            # requiredPower = 0

            sp = SatellitePass(id, nodeId, startTime, endTime, communicationType, achievableKeyVolume, orbitId)
            id += 1
            satellitePasses.append(sp.to_dict())
            
    return satellitePasses

def generate_test_scenario(parameters):
    serviceTargets = generate_random_service_targets(parameters)
    satellitePasses = generate_random_satellite_passes(parameters)
    return {
        # "testScenarioId": str(uuid.uuid4()),
        "serviceTargets": serviceTargets,
        "satellitePasses": satellitePasses
    }

def save_test_scenarios_to_json(parameters, filename, number_of_scenarios=10):
    scenarios = [generate_test_scenario(parameters) for _ in range(number_of_scenarios)]
    with open(filename, 'w') as f:
        json.dump(scenarios, f, indent=4, default=str)

# ----- main ------
parameters = {
    "number_nodes": 100,
    "number_orbits": 24,
    "duration_orbit": 120,  # duration for an orbit in minutes
    "power_threshold": 200
}
save_test_scenarios_to_json(parameters, problem_instances_path, 1)