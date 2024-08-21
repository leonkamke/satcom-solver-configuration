import random
import json
from datetime import datetime, timedelta
from decimal import Decimal
import numpy as np

problem_instances_path = './problem_instances/data/problem_instance.json'


class ServiceTarget:
    def __init__(self, serviceTargetID, priority, keyPolicy, percentageCompleted):
        self.serviceTargetID = serviceTargetID
        self.priority = priority
        self.keyPolicy = keyPolicy
        self.percentageCompleted = percentageCompleted

    def to_dict(self):
        return self.__dict__

class VisibilitySlot:
    def __init__(self, visibilitySlotId, nodeId, orbitId, visibilityStart, visibilityEnd, communicationType, linkAvailabilityPercentage, achievableKeyVolume, requiredPower):
        self.visibilitySlotId = visibilitySlotId
        self.nodeId = nodeId
        self.orbitId = orbitId
        self.visibilityStart = visibilityStart
        self.visibilityEnd = visibilityEnd
        self.communicationType = communicationType
        self.linkAvailabilityPercentage = linkAvailabilityPercentage
        self.achievableKeyVolume = achievableKeyVolume
        self.requiredPower = requiredPower

    def to_dict(self):
        return self.__dict__

def generate_random_service_targets(parameters):
    serviceTargets = []
    for id in range(parameters["number_service_targets"]):
        # Create priority
        x = random.randint(1 , 100)
        priority = 0 if x < 95 else 1
        
        # Create percentageCompleted
        x = random.randint(1, 97)
        percentageCompleted = float(x) / float(100)
        
        # Create KeyPolicy
        x = random.randint(1, 100)
        keyType = None
        if x < 50:
            keyType = "KM"
        elif x < 75:
            keyType = "QK"
        else:
            keyType = "PWK"
        node1 = None
        node2 = None
        if keyType == "PWK":
            indices = random.sample(range(parameters["number_nodes"]), 2)
            node1 = indices[0]
            node2 = indices[1]
        else:
            node1 = -1
            index = random.randint(0, parameters["number_nodes"]-1)
            node2 = index
        keyPolicy = {
            "node1Id": node1,
            "node2Id": node2,
            "keyType": keyType
        }
        serviceTargets.append(ServiceTarget(id, priority, keyPolicy, percentageCompleted).to_dict())
    return serviceTargets
    

def generate_random_visibility_slots(parameters):
    schedule_length_minutes = parameters["number_orbits"] * parameters["duration_orbit"]
    visibilitySlots = []
    
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
    
    # Create visibility slots
    id = 0
    for i in range(schedule_length_minutes):
        # With some given probability create a visibility slot
        x = random.randint(1, 100)
        if x <= 15:
            # Create visibility slot
            # Check which nodes are visible
            x = int(i / 30) % 4
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
            if x < 51:
                communicationType = "QUANTUM_AND_OPTICAL"
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
                
            # Sample link availability
            linkAvailabilityPercentage = None
            if communicationType == "OPTICAL":
                linkAvailabilityPercentage = float(np.random.normal(0.7, 0.1, 1)[0])
                if linkAvailabilityPercentage > 1:
                    linkAvailabilityPercentage = 1.0
                elif linkAvailabilityPercentage < 0.3:
                    linkAvailabilityPercentage = 0.3
            else:   # "QUANTUM_AND_OPTICAL"
                linkAvailabilityPercentage = float(np.random.normal(0.6, 0.1, 1)[0])
                if linkAvailabilityPercentage > 1:
                    linkAvailabilityPercentage = 1.0
                elif linkAvailabilityPercentage < 0.3:
                    linkAvailabilityPercentage = 0.3
            
            # Sample achievableKeyVolume
            achievableKeyVolume = None
            if communicationType == "QUANTUM_AND_OPTICAL":
                keyRate = int(np.random.normal(100, 10, 1)[0])
                if keyRate < 20:
                    keyRate = 20
                achievableKeyVolume = keyRate * duration
            else:
                achievableKeyVolume = 0
            
            # Sample required power (Calc power per second for both channels and multiply with duration)
            requiredPower = 0
            
            vs = VisibilitySlot(id, nodeId, orbitId, startTime, endTime, communicationType, linkAvailabilityPercentage, achievableKeyVolume, requiredPower)
            id += 1
            visibilitySlots.append(vs.to_dict())
            
    return visibilitySlots

def generate_test_scenario(parameters):
    service_targets = generate_random_service_targets(parameters)
    visibility_slots = generate_random_visibility_slots(parameters)
    return {
        # "testScenarioId": str(uuid.uuid4()),
        "serviceTargets": service_targets,
        "visibilitySlots": visibility_slots
    }

def save_test_scenarios_to_json(parameters, filename, number_of_scenarios=10):
    scenarios = [generate_test_scenario(parameters) for _ in range(number_of_scenarios)]
    with open(filename, 'w') as f:
        json.dump(scenarios, f, indent=4, default=str)

if __name__ == "__main__":
    parameters = {
        "number_nodes": 50,
        "number_service_targets": 40, 
        "number_orbits": 4,
        "duration_orbit": 120,  # duration for an orbit in minutes
        "power_threshold": 200
    }
    save_test_scenarios_to_json(parameters, problem_instances_path, 1)