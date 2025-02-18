#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
from pathlib import Path
from sparkle.types import SolverStatus
from sparkle.tools.solver_wrapper_parsing import parse_solver_wrapper_args
from datetime import datetime
from gurobipy import Model, GRB, quicksum
from .utils import *

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

# Prepare the command to execute the solver
solver_name = "Gurobi"
if solver_dir != Path("."):
    solver_exec = f"{solver_dir / solver_name}"
else:
    f"./{solver_name}"
solver_cmd = [solver_exec,
              "-inst", str(instance_path),
              "-seed", str(seed)]

# Read Gurobi parameter from call
params = []
for key in args:
    if args[key] is not None:
        params.extend(["-" + str(key), str(args[key])])

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

# Set the parameters dependent on params dict
model.setParam("limits/time", 60)

# Run the Gurobi solver
schedule_quality = None
runtime = None
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
    runtime = None # TODO: Set runtime of the solver


except Exception as ex:
    print(f"Solver call failed with exception:\n{ex}")

# Optional: Print original output so the solution can be verified by SATVerifier
print("Performance of the solution is: " + str(schedule_quality))

status = SolverStatus.CRASHED
if schedule_quality and runtime:
    status = SolverStatus.SUCCESS
elif runtime >= max_runtime_par:
    status = SolverStatus.TIMEOUT
    

outdir = {"status": status.value,               
          "schedule_quality": schedule_quality,
          "runtime": runtime,                   
          "solver_call": solver_cmd + params}

print(outdir)