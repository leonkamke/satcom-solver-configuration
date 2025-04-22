#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import re
import json
from pathlib import Path
from sparkle.tools.solver_wrapper_parsing import parse_solver_wrapper_args
from datetime import datetime
from pyscipopt import Model, quicksum
import time


"""
branching_scorefunc categorical {s, p, q} [p]
branching_scorefac real [0.0, 1.0] [0.167]
branching_preferbinary categorical {TRUE, FALSE} [FALSE]
lp_initalgorithm categorical {s, p, d, b, c} [s]
lp_pricing categorical {l, a, f, q, d} [l]
heuristics_trivial_freq integer [-1, 10] [0]
separating_poolfreq integer [0, 10] [10]
separating_gomory_away real [0.0, 0.01] [0.01]
heuristics_subnlp_presolveemphasis categorical {0, 1, 2, 3} [0]
"""


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
    

# Convert the arguments to a dictionary
args = parse_solver_wrapper_args(sys.argv[1:])

# Extract and delete data that needs specific formatting
solver_dir = Path(args["solver_dir"])
instance_path = Path(args["instance"])
seed = args["seed"]

del args["solver_dir"]
del args["instance"]
del args["cutoff_time"]
del args["seed"]
del args["objectives"]

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

model = Model("SCIP Solver")

# Turn off all output
model.setParam('display/verblevel', 0)   # Suppress display output

# Computation time limit in seconds
# model.setParam("limits/time", 45)

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
    model.setParam(k.replace("_", "/"), config[k])

# Decision variables
x = {}
for i in V:
    for j in S:
        x[i, j] = model.addVar(vtype="B", name=f"x_{i}_{j}")

# Objective function
model.setObjective(
    quicksum(x[i, j] * pj[j] * (1 + bi[i] * mj[j]) for i in V for j in S),
    "maximize"
)

# Each satellite pass has at most one service target
for i in V:
    model.addCons(quicksum(x[i, j] for j in S) <= 1)

# Each service target can be served at most once
for j in S:
    model.addCons(quicksum(x[i, j] for i in V) <= 1)

# Non-overlapping satellite passes
for i1 in V:
    for i2 in V:
        if i1 != i2 and ti[i1] <= ti[i2]:
            model.addCons(
                (ti[i1] + di[i1] + T_min) <= (ti[i2] + (2 - quicksum(x[i1, k] for k in S) - quicksum(x[i2, k] for k in S)) * 99999)
            )

# The node in the service target and satellite pass must match
for i in V:
    for j in S:
        model.addCons(x[i, j] * (ni[i] - sj[j]) == 0)

# The operation mode must match
for i in V:
    for j in S:
        model.addCons(x[i, j] * oi[i] * (oi[i] - mj[j] - 1) == 0)

# For a given application id first do qkd and afterwards qkd post processing
for j1 in S:
    for j2 in S:
        if aj[j1] == aj[j2] and mj[j1] == 1 and mj[j2] == 0:
            model.addCons(quicksum(ti[i] * x[i, j1] for i in V) <= quicksum(ti[i] * x[i, j2] for i in V))


# Run the SCIP solver
max_runtime = 9999
schedule_quality = 0.0
runtime = max_runtime

# Problem is in model.optimize() method for large problem instances

try:
    # Optimize the model
    model.optimize()
    
    contacts = []
    for i in V:
        for j in S:
            if model.getVal(x[i, j]) > 0.5:
                contacts.append({
                "satellitePass": satellitePasses[i],
                "serviceTarget": serviceTargets[j]
            })
                
    # Compute objectives
    schedule_quality = round(calculateObjectiveFunction(contacts))
    runtime = model.getSolvingTime()
    
    # Print the result for sprakle
    """status = "CRASHED"
    if schedule_quality and runtime:
        status = "SUCCESS"
    elif runtime >= max_runtime:
        status = "TIMEOUT"""

    result = {"status": "SUCCESS",               
            "schedule_quality": schedule_quality,
            "runtime": runtime,                   
            "solver_call": None}

    print(result)
    
except Exception as ex:
    result = {"status": "TIMEOUT",               
            "schedule_quality": 0.0,
            "runtime": max_runtime,                   
            "solver_call": None}
    print(result)
