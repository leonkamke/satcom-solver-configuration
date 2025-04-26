import sys
from pathlib import Path
from datetime import datetime
from gurobipy import Model, GRB, quicksum
import re
import json

def parse_args_to_dict(argv):
    args_dict = {}
    i = 1  # skip python gurobi_solver.py
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

# raise Exception("Something went wrong")

# Read the arguments
args = parse_args_to_dict(sys.argv)

# Extract and delete data that needs specific formatting
instance_path = Path(args["inst"])
seed = args["seed"]

del args["inst"]
del args["seed"]

config = args

# Read the problem instance
problemInstance = read_problem_instance(instance_path)
satellitePasses = problemInstance["satellite_passes"]
serviceTargets = problemInstance["service_targets"]

# Define the optimization problem
V = list(range(len(satellitePasses)))
S = list(range(len(serviceTargets)))

di = {}
ti = {}
bi = {}
ni = {}
fi = {}
oi = {}

reference_time = datetime.fromisoformat(problemInstance["coverage_start"])
for idx, satellitePass in enumerate(satellitePasses):
    start_time = datetime.fromisoformat(satellitePass["startTime"])
    end_time = datetime.fromisoformat(satellitePass["endTime"])

    start_seconds = (start_time - reference_time).total_seconds()
    end_seconds =   (end_time - reference_time).total_seconds()

    ti[idx] = start_seconds

    duration_seconds = end_seconds - start_seconds
    di[idx] = duration_seconds
    bi[idx] = satellitePass["achievableKeyVolume"]
    oi[idx] = 1 if satellitePass["achievableKeyVolume"] == 0.0 else 0
    ni[idx] = satellitePass["nodeId"]
    fi[idx] = satellitePass["orbitId"]

pj = {}
sj = {}
mj = {}
aj = {}
for idx, serviceTarget in enumerate(serviceTargets):
    pj[idx] = serviceTarget["priority"]
    sj[idx] = serviceTarget["nodeId"]
    mj[idx] = 1 if serviceTarget["requestedOperation"] == "QKD" else 0
    aj[idx] = serviceTarget["applicationId"]

# Minimum time between consecutive contacts in seconds
T_min = 60 

# Create Gurobi model
model = Model("Gurobi Solver")

# Suppress all solver output
model.setParam('OutputFlag', 0)

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
    # model.setParam(k, config[k])


# Decision variables
x = model.addVars(V, S, vtype=GRB.BINARY, name="x")

# Objective function
model.setObjective(
    quicksum(x[i, j] * pj[j] * (1 + bi[i] * mj[j]) for i in V for j in S),
    GRB.MAXIMIZE
)

# Each satellite pass has at most one service target
for i in V:
    model.addConstr(quicksum(x[i, j] for j in S) <= 1)

# Each service target can be served at most once
for j in S:
    model.addConstr(quicksum(x[i, j] for i in V) <= 1)

# Non-overlapping satellite passes
for i1 in V:
    for i2 in V:
        if i1 != i2 and ti[i1] <= ti[i2]:
            model.addConstr(
                (ti[i1] + di[i1] + T_min) <= (
                    ti[i2] + (2 - quicksum(x[i1, k] for k in S) - quicksum(x[i2, k] for k in S)) * 99999
                )
            )

# The node in the service target and satellite pass must match
for i in V:
    for j in S:
        model.addConstr(x[i, j] * (ni[i] - sj[j]) == 0)

# The operation mode must match
for i in V:
    for j in S:
        model.addConstr(x[i, j] * oi[i] * (oi[i] - mj[j] - 1) == 0)

# For a given application id, first do QKD and afterwards QKD post-processing
for j1 in S:
    for j2 in S:
        if aj[j1] == aj[j2] and mj[j1] == 1 and mj[j2] == 0:
            model.addConstr(
                quicksum(ti[i] * x[i, j1] for i in V) <= quicksum(ti[i] * x[i, j2] for i in V)
            )


# Run the Gurobi solver
max_runtime = 9999
quality = 0
runtime = max_runtime

try:
    # Optimize the model
    model.optimize()

    contacts = []
    for i in V:
        for j in S:
            if x[i, j].x > 0.5:
                contacts.append({
                "satellitePass": satellitePasses[i],
                "serviceTarget": serviceTargets[j]
            })
                
    # Compute objectives
    quality = int(calculateObjectiveFunction(contacts))
    runtime = round(model.Runtime, 4)
    
    # Print result
    result = {"status": "SUCCESS",               
            "quality": quality,
            "runtime": runtime,                   
            "solver_call": None}
    print("Gurobi solver output is:")
    print(result)

except Exception as ex:
    print(ex)
    
    
    