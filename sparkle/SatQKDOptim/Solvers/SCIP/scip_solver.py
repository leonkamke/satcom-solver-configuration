import sys
from pathlib import Path
from datetime import datetime
import re
import uuid
from pyscipopt import Model, quicksum
import json

def parse_args_to_dict(argv):
    args_dict = {}
    i = 1  # skip python scip_solver.py
    while i < len(argv):
        if argv[i].startswith('-'):
            key = argv[i].lstrip('-')
            # Make sure there's a value after the key
            if i + 1 < len(argv) and not argv[i + 1].startswith('-'):
                args_dict[key] = argv[i + 1]
                i += 2
            else: # Else skip
                i += 1
        else: # Else skip
            i += 1
    return args_dict


# Helper function
def read_problem_instance(instance_path):
    with open(instance_path, 'r') as file:
        data = json.load(file)
        return data[0]
    
# Helper function
def calculateObjectiveFunction(contacts):
    result = 0
    for contact in contacts:
        satellitePass = contact["satellitePass"]
        serviceTarget = contact["serviceTarget"]

        priority = serviceTarget["priority"]
        achievableKeyVolume = satellitePass["achievableKeyVolume"]
        operationMode = 1 if serviceTarget["requestedOperation"] == "QKD" else 0
        result += (priority * (1 + achievableKeyVolume * operationMode))
    return result

# Read the arguments
args = parse_args_to_dict(sys.argv)

instance_path_json = Path(args["inst"])
instance_path_mps = instance_path_json.with_suffix(".mps")

seed = args["seed"]
del args["inst"]
del args["seed"]

config = args

# Read problem instance
print("Read problem instance")
problemInstance = read_problem_instance(instance_path_json)
satellitePasses = problemInstance["satellite_passes"]
serviceTargets = problemInstance["service_targets"]

V = list(range(len(satellitePasses)))
S = list(range(len(serviceTargets)))

model = Model("Satellite Optimization")
model.readProblem(instance_path_mps)

# Set parameters for model
for k, v in config.items():
    if v == "TRUE":
        config[k] = True
    elif v == "FALSE":
        config[k] = False
    elif re.fullmatch(r"-?\d+", v):
        config[k] = int(v)
    elif re.fullmatch(r"-?[\d\.]+", v):
        config[k] = float(v)
    try:
        model.setParam(k.replace("_", "/"), config[k])
    except Exception as ex:
        exception_file_name = './Tmp/' + str(uuid.uuid4()) + '.txt'
        with open(exception_file_name, 'w') as file:
            file.write('Setting parameter ' + str(k) + " -> " + str(config[k]) + ' failed with exception:\n')
            file.write(str(ex))
        sys.exit(1)

# Run the SCIP solver
max_runtime = 60
model.setParam("limits/time", max_runtime)
quality = 0
runtime = max_runtime

try:
    # Optimize the model
    model.optimize()
    
    # Rebuild variable dictionary from model if x is not defined
    if 'x' not in locals():
        x = {}
        for var in model.getVars():
            if var.name.startswith("x_"):
                try:
                    _, i_str, j_str = var.name.split("_")
                    i, j = int(i_str), int(j_str)
                    x[i, j] = var
                except ValueError:
                    print(f"Skipping unrecognized variable name: {var.name}")

    contacts = []
    for i in V:
        for j in S:
            if (i, j) in x:
                val = model.getVal(x[i, j])
                if val > 0.5:
                    contacts.append({
                        "satellitePass": satellitePasses[i],
                        "serviceTarget": serviceTargets[j]
                    })
                
    # Compute objectives
    quality = int(calculateObjectiveFunction(contacts))
    runtime = round(model.getSolvingTime(), 4)
    
    # Print result
    result = {"status": "SUCCESS",               
            "quality": quality,
            "runtime": runtime, # If runtume == maxruntime: runtime *= 10 (PAR10)                    
            "solver_call": None}
    print("SCIP solver output is:")
    print(result)

except Exception as ex:
    print(ex)
    exception_file_name = './Tmp/' + str(uuid.uuid4()) + '.txt'
    with open(exception_file_name, 'w') as file:
        file.write('Optimization method failed with exception:\n')
        file.write(str(ex) + "\n")
        file.write("This is the configuration:\n")
        file.write(str(config))